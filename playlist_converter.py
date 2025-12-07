#!/usr/bin/env python3
"""
Music Playlist Converter
Easy tool to download, trim, and package YouTube songs for events

Features:
- Download songs from YouTube as MP3
- Trim to specific timestamps
- Automatic ZIP file creation
- Songs are numbered in order
- Easy JSON configuration file
"""

import subprocess
import os
import sys
import json
import zipfile
from pathlib import Path
from typing import List, Dict, Optional

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a styled header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def check_dependencies() -> bool:
    """Check if required tools are installed"""
    print_info("Checking dependencies...")

    missing = []

    # Check yt-dlp
    try:
        subprocess.run(["yt-dlp", "--version"],
                      capture_output=True, check=True, timeout=5)
        print_success("yt-dlp found")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        missing.append("yt-dlp")
        print_error("yt-dlp not found")

    # Check ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"],
                      capture_output=True, check=True, timeout=5)
        print_success("ffmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        missing.append("ffmpeg")
        print_error("ffmpeg not found")

    if missing:
        print_error("\nMissing dependencies!")
        print("\nTo install missing tools:")
        if "yt-dlp" in missing:
            print(f"  {Colors.YELLOW}yt-dlp:{Colors.END} pip install yt-dlp")
        if "ffmpeg" in missing:
            print(f"  {Colors.YELLOW}ffmpeg:{Colors.END}")
            print("    - Ubuntu/Debian: sudo apt install ffmpeg")
            print("    - macOS: brew install ffmpeg")
            print("    - Windows: https://ffmpeg.org/download.html")
        return False

    print_success("All dependencies found!\n")
    return True

def time_to_seconds(time_str: str) -> int:
    """Convert time string (MM:SS or H:MM:SS) to seconds"""
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

def sanitize_filename(name: str) -> str:
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

def load_config(config_file: str) -> Optional[Dict]:
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Validate config
        if 'songs' not in config:
            print_error("Config file must contain 'songs' array")
            return None

        if not isinstance(config['songs'], list) or len(config['songs']) == 0:
            print_error("'songs' must be a non-empty array")
            return None

        # Validate each song
        for i, song in enumerate(config['songs'], 1):
            required = ['name', 'url', 'start', 'end']
            for field in required:
                if field not in song:
                    print_error(f"Song {i} is missing required field: {field}")
                    return None

        return config

    except FileNotFoundError:
        print_error(f"Configuration file not found: {config_file}")
        return None
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in config file: {e}")
        return None
    except Exception as e:
        print_error(f"Error loading config: {e}")
        return None

def download_and_trim_song(song: Dict, index: int, total: int, output_dir: Path) -> Optional[Path]:
    """
    Download and trim a single song
    Returns the path to the trimmed file, or None on failure
    """
    print(f"\n{Colors.BOLD}[{index}/{total}] Processing: {song['name']}{Colors.END}")
    print(f"  URL: {song['url']}")
    print(f"  Trim: {song['start']} → {song['end']}")

    try:
        # Calculate duration
        start_sec = time_to_seconds(song['start'])
        end_sec = time_to_seconds(song['end'])
        duration = end_sec - start_sec

        if duration <= 0:
            print_error(f"Invalid time range: end time must be after start time")
            return None

        print_info(f"Duration: {duration} seconds")

        # Create safe filename
        safe_name = sanitize_filename(song['name'])
        output_file = output_dir / f"{index:02d}_{safe_name}.mp3"

        # Download and trim using yt-dlp with ffmpeg
        # This downloads, extracts audio, and trims in one efficient operation
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",  # Best quality
            "--postprocessor-args", f"ffmpeg:-ss {start_sec} -t {duration}",
            "--no-playlist",  # Only download single video
            "-o", str(output_file),
            song['url']
        ]

        print_info("Downloading and trimming...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout per song
        )

        if result.returncode == 0 and output_file.exists():
            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print_success(f"Saved: {output_file.name} ({file_size:.2f} MB)")
            return output_file
        else:
            print_error(f"Download failed")
            if result.stderr:
                print(f"  Error details: {result.stderr[:200]}")
            return None

    except subprocess.TimeoutExpired:
        print_error("Download timed out (max 10 minutes per song)")
        return None
    except ValueError as e:
        print_error(str(e))
        return None
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return None

def create_zip(files: List[Path], output_dir: Path, zip_name: str) -> Optional[Path]:
    """Create a ZIP file containing all the trimmed songs"""
    try:
        zip_path = output_dir / zip_name

        print_info(f"Creating ZIP file: {zip_name}")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                if file.exists():
                    zipf.write(file, file.name)
                    print(f"  Added: {file.name}")

        zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB
        print_success(f"ZIP created: {zip_path} ({zip_size:.2f} MB)")
        return zip_path

    except Exception as e:
        print_error(f"Failed to create ZIP: {e}")
        return None

def create_example_config(filename: str = "playlist_songs.json"):
    """Create an example configuration file"""
    example_config = {
        "playlist_name": "My Custom Playlist 2024",
        "output_dir": "my_playlist",
        "create_zip": True,
        "zip_name": "playlist_songs.zip",
        "songs": [
            {
                "name": "Opening Song",
                "url": "https://www.youtube.com/watch?v=REPLACE_WITH_VIDEO_ID",
                "start": "0:30",
                "end": "3:45",
                "notes": "Opening song - keep the energy high!"
            },
            {
                "name": "Dance Track",
                "url": "https://www.youtube.com/watch?v=REPLACE_WITH_VIDEO_ID",
                "start": "0:15",
                "end": "2:30",
                "notes": "Great for dance performances"
            },
            {
                "name": "Party Anthem",
                "url": "https://www.youtube.com/watch?v=REPLACE_WITH_VIDEO_ID",
                "start": "1:00",
                "end": "4:00"
            }
        ]
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print_error(f"Could not create example config: {e}")
        return False

def main():
    """Main function"""
    print_header("🎵 Music Playlist Converter 🎵")

    # Parse command line arguments
    if len(sys.argv) < 2:
        print_info("Usage: python playlist_converter.py <config_file.json>")
        print_info("\nTo create an example configuration file:")
        print(f"  python playlist_converter.py --create-example")

        # Ask if user wants to create example
        try:
            response = input(f"\n{Colors.YELLOW}Create example config? (y/n): {Colors.END}").lower()
            if response == 'y':
                if create_example_config():
                    print_success("\nExample config created: playlist_songs.json")
                    print_info("Edit this file with your YouTube URLs and timestamps, then run:")
                    print(f"  python playlist_converter.py playlist_songs.json")
                sys.exit(0)
            else:
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)

    # Handle --create-example flag
    if sys.argv[1] == "--create-example":
        filename = sys.argv[2] if len(sys.argv) > 2 else "playlist_songs.json"
        if create_example_config(filename):
            print_success(f"Example config created: {filename}")
            print_info("Edit this file with your YouTube URLs and timestamps, then run:")
            print(f"  python playlist_converter.py {filename}")
        sys.exit(0)

    config_file = sys.argv[1]

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Load configuration
    print_info(f"Loading configuration from: {config_file}")
    config = load_config(config_file)
    if not config:
        sys.exit(1)

    # Display playlist info
    playlist_name = config.get('playlist_name', 'My Playlist')
    print_success(f"Playlist: {playlist_name}")
    print_info(f"Total songs: {len(config['songs'])}")

    # Create output directory
    output_dir = Path(config.get('output_dir', 'my_playlist'))
    output_dir.mkdir(exist_ok=True)
    print_info(f"Output directory: {output_dir.absolute()}")

    # Process all songs
    print_header("Processing Songs")
    successful_files = []
    failed_songs = []

    for i, song in enumerate(config['songs'], 1):
        result = download_and_trim_song(song, i, len(config['songs']), output_dir)
        if result:
            successful_files.append(result)
        else:
            failed_songs.append(song['name'])

    # Create ZIP if requested
    zip_path = None
    if config.get('create_zip', True) and successful_files:
        print_header("Creating ZIP Archive")
        zip_name = config.get('zip_name', 'playlist_songs.zip')
        zip_path = create_zip(successful_files, output_dir, zip_name)

    # Print summary
    print_header("Summary")
    print(f"  Processed: {Colors.BOLD}{len(successful_files)}/{len(config['songs'])}{Colors.END} songs")

    if successful_files:
        print_success(f"Successfully trimmed {len(successful_files)} songs")
        print(f"  Location: {output_dir.absolute()}")

    if failed_songs:
        print_warning(f"\nFailed songs ({len(failed_songs)}):")
        for name in failed_songs:
            print(f"  - {name}")

    if zip_path:
        print(f"\n{Colors.BOLD}{Colors.GREEN}📦 ZIP file ready: {zip_path.name}{Colors.END}")
        print(f"  Full path: {zip_path.absolute()}")

    print(f"\n{Colors.BOLD}{Colors.CYAN}🎉 All done! Enjoy your playlist! 🎉{Colors.END}\n")

    # Final status
    if len(successful_files) == len(config['songs']):
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Partial failure

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
