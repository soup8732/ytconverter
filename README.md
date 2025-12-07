# 🎵 Custom Playlist Maker

Create custom trimmed song playlists from YouTube videos with an easy-to-use web interface!

Perfect for events, parties, performances, and any occasion where you need specific portions of songs in a specific order.

---

## ✨ Features

- 🎬 **Download from YouTube**: Fetch audio from any YouTube video
- ✂️ **Smart Trimming**: Automatically trim songs to your specified timestamps
- 📦 **ZIP Export**: Creates a ready-to-use ZIP file with all your songs
- 🔢 **Numbered Playlist**: Songs are automatically numbered in your preferred order
- 🌐 **Web Interface**: Beautiful, modern web UI - no command line needed!
- ⚡ **Efficient Processing**: Downloads and trims in a single operation
- 🎯 **Flexible Timing**: 
  - Leave start time empty to begin from the start
  - Leave end time empty to go to the end
  - Specify both for precise trimming
  - Specify only one for partial trimming

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- `ffmpeg` installed on your system
- `yt-dlp` (will be installed automatically)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/kaifcodec/ytconverter.git
cd ytconverter
```

2. **Install dependencies:**
```bash
pip install -r requirements-web.txt
```

3. **Install system dependencies:**

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install ffmpeg
```

**Linux (Fedora):**
```bash
sudo dnf install ffmpeg
```

**Windows:**
Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your PATH.

4. **Run the application:**
```bash
python3 app.py
```

5. **Open your browser:**
Navigate to `http://localhost:5000` (or the port shown in the terminal)

---

## 📖 How to Use

1. **Add Songs**: Click "+ Add Song" to add YouTube videos to your playlist
2. **Enter Details**: For each song, provide:
   - **Song Name**: A name for the track
   - **YouTube URL**: The full YouTube video URL
   - **Start Time** (optional): When to start trimming (format: MM:SS or H:MM:SS)
   - **End Time** (optional): When to stop trimming (format: MM:SS or H:MM:SS)
3. **Create Playlist**: Click "🎵 Create Playlist" and wait for processing
4. **Download**: Once complete, download your ZIP file with all trimmed songs!

### Time Format Examples

- `0:30` - 30 seconds
- `1:15` - 1 minute 15 seconds
- `2:45` - 2 minutes 45 seconds
- `1:05:30` - 1 hour 5 minutes 30 seconds

### Trimming Examples

- **Full song**: Leave both start and end empty
- **From start to 2:30**: Leave start empty, set end to `2:30`
- **From 1:00 to end**: Set start to `1:00`, leave end empty
- **Specific segment**: Set start to `0:30`, end to `3:45`

---

## 🎯 Use Cases

- **Wedding Playlists**: Create custom trimmed songs for ceremonies
- **Dance Performances**: Extract specific portions for choreography
- **Event Music**: Build playlists with perfect timing
- **Podcast Clips**: Extract specific segments from long videos
- **Music Mixes**: Create custom compilations with precise timing

---

## 🛠️ Technical Details

### Requirements

- Python 3.9+
- Flask 3.0.0
- yt-dlp (latest version)
- ffmpeg
- gunicorn (for production)

### Project Structure

```
ytconverter/
├── app.py                 # Main Flask web application
├── templates/
│   └── index.html        # Web interface
├── requirements-web.txt   # Python dependencies
└── README.md             # This file
```

### Running in Production

For production deployment, use gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or set environment variables:

```bash
export PORT=5000
gunicorn app:app
```

---

## 🔧 Troubleshooting

### "Missing dependencies: yt-dlp, ffmpeg"

Make sure both are installed:
- **yt-dlp**: `pip install yt-dlp` or `pip install -r requirements-web.txt`
- **ffmpeg**: Install using your system's package manager (see Installation section)

### "HTTP Error 403: Forbidden"

YouTube may be blocking the request. The app automatically tries multiple methods to bypass restrictions. If it persists:
- Try a different video
- Wait a few minutes and retry (rate limiting)
- Ensure yt-dlp is up to date: `pip install --upgrade yt-dlp`

### Download Fails

- Check that the YouTube URL is valid and accessible
- Ensure the video is not private or age-restricted
- Verify your internet connection
- Check server logs for detailed error messages

---

## 📝 License

See [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions, issues, or feedback, please open an issue on GitHub.

---

## ⭐ Star History

If you find this tool helpful, please consider giving it a star!

---

**Made with ❤️ for creating perfect playlists**
