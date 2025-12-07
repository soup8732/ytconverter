# 🎵 Custom Playlist Maker

> **Create custom trimmed song playlists from YouTube videos with an easy-to-use web interface!**

Perfect for events, parties, performances, and any occasion where you need specific portions of songs in a specific order.

---

## ✨ What Can You Do?

- 🎬 **Download from YouTube** - Fetch audio from any YouTube video
- ✂️ **Smart Trimming** - Automatically trim songs to your specified timestamps
- 📦 **ZIP Export** - Creates a ready-to-use ZIP file with all your songs
- 🔢 **Numbered Playlist** - Songs are automatically numbered in your preferred order
- 🌐 **Web Interface** - Beautiful, modern web UI - no command line needed!
- ⚡ **Efficient Processing** - Downloads and trims in a single operation
- 🎯 **Flexible Timing** - Full control over start and end times (or leave them empty!)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

**Python 3.9+ is required**

**Install Python packages:**
```bash
pip install -r requirements-web.txt
```

**Install ffmpeg:**

| Platform | Command |
|----------|---------|
| **macOS** | `brew install ffmpeg` |
| **Linux (Ubuntu/Debian)** | `sudo apt install ffmpeg` |
| **Linux (Fedora)** | `sudo dnf install ffmpeg` |
| **Windows** | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |

### Step 2: Run the Application

```bash
python3 app.py
```

You'll see output like:
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Open your browser and go to: **http://localhost:5000**

That's it! You're ready to create playlists! 🎉

---

## 📖 How to Use (Step-by-Step)

### 1. Add Your Songs

Click the **"+ Add Song"** button to add a new song to your playlist. You can add as many songs as you want!

### 2. Fill in Song Details

For each song, you'll need:

- **Song Name** (required): Give your track a name (e.g., "Opening Song")
- **YouTube URL** (required): Paste the full YouTube video URL
- **Start Time** (optional): When to start the song (format: `MM:SS` or `H:MM:SS`)
- **End Time** (optional): When to end the song (format: `MM:SS` or `H:MM:SS`)

### 3. Understanding Time Formats

**Time format examples:**
- `0:30` = 30 seconds
- `1:15` = 1 minute 15 seconds  
- `2:45` = 2 minutes 45 seconds
- `1:05:30` = 1 hour 5 minutes 30 seconds

**Trimming options:**

| What You Want | Start Time | End Time |
|---------------|-----------|----------|
| **Full song** | Leave empty | Leave empty |
| **From start to 2:30** | Leave empty | `2:30` |
| **From 1:00 to end** | `1:00` | Leave empty |
| **Specific segment** | `0:30` | `3:45` |

### 4. Create Your Playlist

1. Click **"🎵 Create Playlist"**
2. Wait for processing (you'll see a progress bar)
3. Download your ZIP file when complete!

---

## 💡 Real-World Examples

### Example 1: Full Songs Playlist
```
Song 1: "Party Anthem" - https://youtube.com/watch?v=...
  Start: (empty)
  End: (empty)
  
Song 2: "Dance Track" - https://youtube.com/watch?v=...
  Start: (empty)
  End: (empty)
```
**Result:** Full versions of both songs

### Example 2: Trimmed Segments
```
Song 1: "Opening" - https://youtube.com/watch?v=...
  Start: 0:30
  End: 2:00
  
Song 2: "Main Track" - https://youtube.com/watch?v=...
  Start: 1:15
  End: 4:30
```
**Result:** Only the specified portions of each song

### Example 3: Mixed (Some Full, Some Trimmed)
```
Song 1: "Intro" - https://youtube.com/watch?v=...
  Start: (empty)
  End: 0:45
  
Song 2: "Main Song" - https://youtube.com/watch?v=...
  Start: (empty)
  End: (empty)
```
**Result:** First 45 seconds of intro, then full main song

---

## 🎯 Common Use Cases

- 🎉 **Event Playlists** - Create custom music for parties and celebrations
- 💃 **Dance Performances** - Extract specific portions for choreography
- 🎤 **Podcast Clips** - Extract segments from long videos
- 🎵 **Music Mixes** - Create custom compilations with precise timing
- 🎬 **Video Editing** - Get audio clips for video projects

---

## 🔧 Troubleshooting

### ❌ "Missing dependencies: yt-dlp, ffmpeg"

**Solution:**
```bash
# Install yt-dlp
pip install yt-dlp

# Install ffmpeg (choose your platform)
brew install ffmpeg          # macOS
sudo apt install ffmpeg     # Linux
```

### ❌ "HTTP Error 403: Forbidden"

YouTube may be blocking the request. Try:
- ✅ Wait a few minutes and retry (rate limiting)
- ✅ Try a different video
- ✅ Update yt-dlp: `pip install --upgrade yt-dlp`
- ✅ The app automatically tries multiple methods to bypass restrictions

### ❌ Download Fails

**Check these:**
- ✅ YouTube URL is valid and accessible
- ✅ Video is not private or age-restricted
- ✅ Internet connection is working
- ✅ Check the browser console or server logs for details

### ❌ Port Already in Use

If port 5000 is busy, the app will use a different port. Check the terminal output for the actual port number, or set it manually:

```bash
PORT=5001 python3 app.py
```

---

## 🛠️ Advanced Usage

### Running on a Different Port

```bash
PORT=8080 python3 app.py
```

### Running in Production

For production deployment, use gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with environment variables:

```bash
export PORT=5000
gunicorn app:app
```

### Project Structure

```
ytconverter/
├── app.py                    # Main Flask web application
├── templates/
│   └── index.html            # Web interface
├── requirements-web.txt      # Python dependencies
├── playlist_converter.py      # CLI version (optional)
└── README.md                 # This file
```

---

## 📋 Requirements

- **Python**: 3.9 or higher
- **Flask**: 3.0.0
- **yt-dlp**: Latest version (installed automatically)
- **ffmpeg**: For audio processing
- **gunicorn**: For production deployment (optional)

---

## 🆘 Need Help?

- 📖 Check the [PLAYLIST_README.md](PLAYLIST_README.md) for CLI usage
- 🐛 Found a bug? [Open an issue](https://github.com/kaifcodec/ytconverter/issues)
- 💬 Have questions? [Open a discussion](https://github.com/kaifcodec/ytconverter/discussions)

---

## 📝 License

See [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⭐ Show Your Support

If you find this tool helpful, please consider giving it a star on GitHub!

---

**Made with ❤️ for creating perfect playlists**

---

## 🎬 Quick Demo

1. **Start the app**: `python3 app.py`
2. **Open browser**: http://localhost:5000
3. **Add songs**: Click "+ Add Song"
4. **Paste YouTube URLs**: Copy/paste your video links
5. **Set times** (optional): Add start/end times if needed
6. **Create playlist**: Click "🎵 Create Playlist"
7. **Download**: Get your ZIP file with all songs!

**That's it! No complicated setup, no command line needed - just a simple web interface!** 🚀
