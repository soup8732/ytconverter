#!/usr/bin/env python3
"""
Music Playlist Converter - Web Application
Flask web app for creating custom trimmed song playlists
"""

from flask import Flask, render_template, request, send_file, jsonify, session
import subprocess
import os
import json
import zipfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import uuid
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'music-playlist-converter-secret-key-change-this')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / 'playlist_uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    try:
        current_time = datetime.now().timestamp()
        for item in UPLOAD_FOLDER.iterdir():
            if item.is_dir():
                # Check if directory is older than 1 hour
                if current_time - item.stat().st_mtime > 3600:
                    shutil.rmtree(item, ignore_errors=True)
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

def get_yt_dlp_command():
    """Get the yt-dlp command - try direct command first, then python module"""
    try:
        subprocess.run(["yt-dlp", "--version"],
                      capture_output=True, check=True, timeout=5)
        return ["yt-dlp"]
    except:
        try:
            subprocess.run(["python3", "-m", "yt_dlp", "--version"],
                          capture_output=True, check=True, timeout=5)
            return ["python3", "-m", "yt_dlp"]
        except:
            return None

def check_dependencies():
    """Check if required tools are installed"""
    missing = []

    if get_yt_dlp_command() is None:
        missing.append("yt-dlp")

    # Check for ffmpeg - try common paths
    ffmpeg_found = False
    ffmpeg_paths = ["ffmpeg", "/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg"]
    for ffmpeg_path in ffmpeg_paths:
        try:
            subprocess.run([ffmpeg_path, "-version"],
                          capture_output=True, check=True, timeout=5)
            ffmpeg_found = True
            break
        except:
            continue
    
    if not ffmpeg_found:
        missing.append("ffmpeg")

    return missing

def time_to_seconds(time_str):
    """Convert time string to seconds"""
    try:
        parts = [int(p) for p in time_str.split(':')]
        if len(parts) == 2:  # MM:SS
            return parts[0] * 60 + parts[1]
        elif len(parts) == 3:  # H:MM:SS
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        else:
            raise ValueError(f"Invalid time format: {time_str}")
    except Exception as e:
        raise ValueError(f"Could not parse time '{time_str}': {e}")

def sanitize_filename(name):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

def download_with_web_client(song, index, total, output_dir, safe_name, postprocessor_args, yt_dlp_cmd):
    """Fallback download using web client if android client fails"""
    try:
        output_file = output_dir / f"{index:02d}_{safe_name}.mp3"
        
        cmd = yt_dlp_cmd + [
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--no-playlist",
            "--no-warnings",
            "--no-progress",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--referer", "https://www.youtube.com/",
            # Try web client
            "--extractor-args", "youtube:player_client=web",
            "--retries", "2",
            "-o", str(output_file),
            song['url']
        ]
        
        if postprocessor_args:
            cmd.extend(["--postprocessor-args", f"ffmpeg:{' '.join(postprocessor_args)}"])
        
        logger.info(f"Retrying with web client: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0 and output_file.exists():
            logger.info(f"Successfully downloaded with web client: {output_file}")
            return str(output_file)
        else:
            logger.error(f"Web client also failed: {result.stderr[:200] if result.stderr else 'Unknown error'}")
            return None
    except Exception as e:
        logger.error(f"Error in web client fallback: {e}")
        return None

def download_and_trim_song(song, index, total, output_dir):
    """Download and trim a single song"""
    try:
        logger.info(f"Processing [{index}/{total}]: {song['name']}")

        # Handle optional start and end times
        start_sec = None
        end_sec = None
        
        if song.get('start') and song['start'].strip():
            start_sec = time_to_seconds(song['start'])
        
        if song.get('end') and song['end'].strip():
            end_sec = time_to_seconds(song['end'])
        
        # If only end is provided, start from beginning (0)
        if start_sec is None and end_sec is not None:
            start_sec = 0
        
        # Validate time range if both are provided
        if start_sec is not None and end_sec is not None:
            duration = end_sec - start_sec
            if duration <= 0:
                raise ValueError("Invalid time range: end time must be after start time")

        safe_name = sanitize_filename(song['name'])
        output_file = output_dir / f"{index:02d}_{safe_name}.mp3"

        # Build ffmpeg postprocessor args based on what's provided
        postprocessor_args = []
        
        if start_sec is not None:
            postprocessor_args.append(f"-ss {start_sec}")
        
        if start_sec is not None and end_sec is not None:
            # If both start and end are provided, use duration
            duration = end_sec - start_sec
            postprocessor_args.append(f"-t {duration}")
        # If only start is provided (no end), no -t flag means go to end
        # If neither is provided, download full video (no postprocessor args)
        
        # Get yt-dlp command (try direct command, fallback to python module)
        yt_dlp_cmd = get_yt_dlp_command()
        if yt_dlp_cmd is None:
            raise RuntimeError("yt-dlp is not available")
        
        # Build command with options to bypass YouTube restrictions
        # Try android client first (often bypasses restrictions better)
        cmd = yt_dlp_cmd + [
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--no-playlist",
            "--no-warnings",
            "--no-progress",
            # Options to help bypass YouTube restrictions
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "--referer", "https://www.youtube.com/",
            # Try different extraction methods (android client often works better)
            "--extractor-args", "youtube:player_client=android",
            # Retry on failures
            "--retries", "3",
            "--fragment-retries", "3",
            "-o", str(output_file),
            song['url']
        ]
        
        # Add postprocessor args only if we need trimming
        if postprocessor_args:
            cmd.extend(["--postprocessor-args", f"ffmpeg:{' '.join(postprocessor_args)}"])

        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0 and output_file.exists():
            logger.info(f"Successfully downloaded: {output_file}")
            return str(output_file)
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            logger.error(f"Download failed for {song['name']}:")
            logger.error(f"Return code: {result.returncode}")
            logger.error(f"Error output: {error_msg[:500]}")
            if result.stdout:
                logger.error(f"Stdout: {result.stdout[:500]}")
            
            # Try to provide a more user-friendly error message
            error_lower = error_msg.lower()
            if "403" in error_msg or "forbidden" in error_lower:
                logger.warning("YouTube returned 403 Forbidden - trying with web client...")
                # Retry with web client instead of android
                return download_with_web_client(song, index, total, output_dir, safe_name, postprocessor_args, yt_dlp_cmd)
            elif "private" in error_lower or "unavailable" in error_lower:
                logger.warning("Video appears to be private or unavailable")
            elif "not found" in error_lower or "404" in error_msg:
                logger.warning("Video not found - check URL")
            
            return None

    except subprocess.TimeoutExpired:
        logger.error(f"Download timed out for {song.get('name', 'unknown')}")
        return None
    except Exception as e:
        import traceback
        logger.error(f"Error processing song {song.get('name', 'unknown')}: {e}")
        logger.error(traceback.format_exc())
        return None

def create_zip(files, output_dir, zip_name):
    """Create ZIP file from song list"""
    try:
        zip_path = output_dir / zip_name

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                file_path = Path(file)
                if file_path.exists():
                    zipf.write(file_path, file_path.name)

        return str(zip_path)
    except Exception as e:
        logger.error(f"Failed to create ZIP: {e}")
        return None

@app.route('/')
def index():
    """Main page"""
    cleanup_old_files()
    return render_template('index.html')

@app.route('/check_dependencies')
def check_deps():
    """Check if dependencies are installed"""
    missing = check_dependencies()
    return jsonify({
        'ok': len(missing) == 0,
        'missing': missing
    })

@app.route('/process', methods=['POST'])
def process_playlist():
    """Process the playlist"""
    try:
        # Get JSON data from request
        data = request.get_json()

        if not data or 'songs' not in data:
            return jsonify({'error': 'Invalid request'}), 400

        songs = data['songs']
        if not songs or len(songs) == 0:
            return jsonify({'error': 'No songs provided'}), 400

        # Validate songs
        for i, song in enumerate(songs, 1):
            required = ['name', 'url']
            for field in required:
                if field not in song or not song[field]:
                    return jsonify({'error': f'Song {i} missing field: {field}'}), 400

        # Check dependencies
        missing = check_dependencies()
        if missing:
            return jsonify({
                'error': f'Missing dependencies: {", ".join(missing)}'
            }), 500

        # Create unique output directory
        session_id = str(uuid.uuid4())[:8]
        output_dir = UPLOAD_FOLDER / f"playlist_{session_id}"
        output_dir.mkdir(exist_ok=True)

        # Process songs
        successful_files = []
        failed_songs = []

        for i, song in enumerate(songs, 1):
            result = download_and_trim_song(song, i, len(songs), output_dir)
            if result:
                successful_files.append(result)
            else:
                failed_songs.append(song['name'])

        if not successful_files:
            return jsonify({
                'error': 'All songs failed to download. This may be due to YouTube restrictions, network issues, or invalid URLs. Please check the URLs and try again.',
                'failed': failed_songs,
                'hint': 'Try updating yt-dlp or check if the videos are accessible'
            }), 500

        # Create ZIP
        zip_name = data.get('zip_name', 'playlist_songs.zip')
        zip_path = create_zip(successful_files, output_dir, zip_name)

        if not zip_path:
            return jsonify({'error': 'Failed to create ZIP file'}), 500

        return jsonify({
            'success': True,
            'total': len(songs),
            'successful': len(successful_files),
            'failed': len(failed_songs),
            'failed_songs': failed_songs,
            'download_url': f'/download/{session_id}/{zip_name}'
        })

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Processing error: {e}\n{error_trace}")
        return jsonify({'error': str(e), 'traceback': error_trace if app.debug else None}), 500

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Download the ZIP file"""
    try:
        file_path = UPLOAD_FOLDER / f"playlist_{session_id}" / filename

        if not file_path.exists():
            return "File not found", 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/zip'
        )

    except Exception as e:
        logger.error(f"Download error: {e}")
        return "Download failed", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
