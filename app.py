#!/usr/bin/env python3
"""
Mehndi Playlist Converter - Web Application
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
app.secret_key = os.environ.get('SECRET_KEY', 'mehndi-playlist-secret-key-change-this')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload folder
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / 'mehndi_uploads'
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

def check_dependencies():
    """Check if required tools are installed"""
    missing = []

    try:
        subprocess.run(["yt-dlp", "--version"],
                      capture_output=True, check=True, timeout=5)
    except:
        missing.append("yt-dlp")

    try:
        subprocess.run(["ffmpeg", "-version"],
                      capture_output=True, check=True, timeout=5)
    except:
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

def download_and_trim_song(song, index, total, output_dir):
    """Download and trim a single song"""
    try:
        logger.info(f"Processing [{index}/{total}]: {song['name']}")

        start_sec = time_to_seconds(song['start'])
        end_sec = time_to_seconds(song['end'])
        duration = end_sec - start_sec

        if duration <= 0:
            raise ValueError("Invalid time range")

        safe_name = sanitize_filename(song['name'])
        output_file = output_dir / f"{index:02d}_{safe_name}.mp3"

        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--postprocessor-args", f"ffmpeg:-ss {start_sec} -t {duration}",
            "--no-playlist",
            "-o", str(output_file),
            song['url']
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0 and output_file.exists():
            return str(output_file)
        else:
            logger.error(f"Download failed: {result.stderr[:200]}")
            return None

    except Exception as e:
        logger.error(f"Error processing song: {e}")
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
            required = ['name', 'url', 'start', 'end']
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
                'error': 'All songs failed to download',
                'failed': failed_songs
            }), 500

        # Create ZIP
        zip_name = data.get('zip_name', 'mehndi_songs.zip')
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
        logger.error(f"Processing error: {e}")
        return jsonify({'error': str(e)}), 500

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
    app.run(host='0.0.0.0', port=port, debug=False)
