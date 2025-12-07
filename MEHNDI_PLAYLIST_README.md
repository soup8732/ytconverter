# 🎵 Mehndi Playlist Converter

**Easy-to-use tool for creating custom trimmed song playlists from YouTube**

Perfect for wedding events, parties, and celebrations where you need specific portions of songs downloaded and ready to play in order!

## ✨ Features

- 📥 Download songs from YouTube as high-quality MP3
- ✂️ Automatically trim to your specified timestamps
- 📦 Creates a ZIP file with all songs ready to go
- 🔢 Songs are numbered in the order you want them played
- 📝 Simple JSON configuration file - just copy/paste your YouTube links!
- 🎨 Colorful progress indicators so you know what's happening
- ⚡ Efficient - downloads and trims in a single operation

## 🚀 Quick Start

### Step 1: Install Dependencies

**Install yt-dlp:**
```bash
pip install yt-dlp
```

**Install ffmpeg:**
- **Ubuntu/Debian:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Step 2: Create Your Song List

Create a configuration file (or use the example):

```bash
python mehndi_playlist.py --create-example my_songs.json
```

This creates a file like:
```json
{
  "playlist_name": "Mehndi Celebration 2024",
  "output_dir": "mehndi_playlist",
  "create_zip": true,
  "zip_name": "mehndi_songs.zip",
  "songs": [
    {
      "name": "Song Name 1",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "start": "0:30",
      "end": "3:45",
      "notes": "Optional notes about this song"
    },
    {
      "name": "Song Name 2",
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "start": "1:00",
      "end": "2:30"
    }
  ]
}
```

### Step 3: Edit Your Configuration

Open `my_songs.json` and:

1. **Replace the YouTube URLs** with your actual song links
2. **Set the timestamps** where you want each song to start and end
3. **Name your songs** (this will be the filename)
4. Add as many songs as you want!

**Time Format:**
- `MM:SS` (e.g., "2:30" = 2 minutes 30 seconds)
- `H:MM:SS` (e.g., "1:15:30" = 1 hour 15 minutes 30 seconds)

### Step 4: Run the Tool

```bash
python mehndi_playlist.py my_songs.json
```

That's it! Your trimmed songs will be in the `mehndi_playlist` folder, and you'll have a `mehndi_songs.zip` file ready to share or upload!

## 📖 Detailed Usage

### Configuration File Options

| Field | Required | Description | Default |
|-------|----------|-------------|---------|
| `playlist_name` | No | Name of your playlist | "Mehndi Playlist" |
| `output_dir` | No | Where to save the files | "mehndi_playlist" |
| `create_zip` | No | Create a ZIP file? | `true` |
| `zip_name` | No | Name of the ZIP file | "mehndi_songs.zip" |
| `songs` | **Yes** | Array of song objects | - |

### Song Object Format

| Field | Required | Description |
|-------|----------|-------------|
| `name` | **Yes** | Song name (used for filename) |
| `url` | **Yes** | Full YouTube URL |
| `start` | **Yes** | Start timestamp (MM:SS or H:MM:SS) |
| `end` | **Yes** | End timestamp (MM:SS or H:MM:SS) |
| `notes` | No | Optional notes (not used in processing) |

### Example: Real Mehndi Playlist

```json
{
  "playlist_name": "Priya's Mehndi - December 2024",
  "output_dir": "priya_mehndi",
  "create_zip": true,
  "zip_name": "priya_mehndi_songs.zip",
  "songs": [
    {
      "name": "Mehendi_Opening",
      "url": "https://www.youtube.com/watch?v=ABC123",
      "start": "0:15",
      "end": "3:30",
      "notes": "Entrance song - start when bride enters"
    },
    {
      "name": "Dholida_Dance",
      "url": "https://www.youtube.com/watch?v=XYZ789",
      "start": "0:30",
      "end": "2:45",
      "notes": "First group dance"
    },
    {
      "name": "Gal_Mitthi_Solo",
      "url": "https://www.youtube.com/watch?v=DEF456",
      "start": "1:00",
      "end": "3:15",
      "notes": "Sister's solo performance"
    }
  ]
}
```

## 📋 Tips & Best Practices

### Finding the Right Timestamps

1. Open the YouTube video
2. Play it and note the times you want
3. Use YouTube's timestamp format (shown in the player)
4. Test with one song first to make sure it works!

### Song Naming

- Use descriptive names: "Mehendi_Opening", "Cousins_Dance", etc.
- Avoid special characters: `/\:*?"<>|`
- Songs will be numbered automatically (01_, 02_, 03_...)

### Quality Tips

- The tool downloads at highest quality available
- MP3 format is compatible with all devices/players
- Typical song: 2-3 MB per minute

### Organizing Multiple Events

Create separate config files:
- `mehndi_songs.json`
- `sangeet_songs.json`
- `reception_songs.json`

Run each separately:
```bash
python mehndi_playlist.py mehndi_songs.json
python mehndi_playlist.py sangeet_songs.json
```

## 🛠️ Troubleshooting

### "yt-dlp not found"
```bash
pip install yt-dlp
# or
pip install --user yt-dlp
```

### "ffmpeg not found"
- **Linux:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from ffmpeg.org and add to PATH

### "Invalid JSON"
- Use a JSON validator: [jsonlint.com](https://jsonlint.com)
- Common issues:
  - Missing commas between songs
  - Unclosed quotes `"`
  - Unclosed brackets `}` or `]`

### Song Download Fails
- Check if the YouTube URL is correct
- Make sure the video is not private or age-restricted
- Try the URL in your browser first

### Wrong Timestamps
- Double-check your start/end times
- Remember: `MM:SS` format (2:30 = 2 min 30 sec)
- End time must be after start time!

## 📂 Output Structure

After running, you'll have:

```
mehndi_playlist/
├── 01_Song_Name_1.mp3
├── 02_Song_Name_2.mp3
├── 03_Song_Name_3.mp3
├── ...
└── mehndi_songs.zip  (contains all the MP3s)
```

The ZIP file is ready to:
- Share via email/WhatsApp
- Upload to Google Drive/Dropbox
- Give to your DJ
- Load onto your phone/laptop

## 🎯 Common Use Cases

### Wedding Mehndi
Create a perfectly timed playlist with all the best parts of songs - no awkward intros or long outros!

### Dance Performances
Trim songs to exactly the length you rehearsed - no more, no less.

### Event Planning
Prepare multiple playlists for different segments (welcome, games, dinner, etc.)

### DJ Sets
Give your DJ a USB drive with pre-trimmed songs in the exact order.

## ⚡ Advanced Usage

### Custom Output Directory
```json
{
  "output_dir": "/path/to/my/music/mehndi",
  "songs": [...]
}
```

### Skip ZIP Creation
```json
{
  "create_zip": false,
  "songs": [...]
}
```

### Process Specific Songs
Just remove or comment out songs you don't want in the JSON file.

## 📞 Need Help?

Common questions:

**Q: Can I use Spotify links?**
A: No, only YouTube URLs are supported.

**Q: How long does it take?**
A: About 30-60 seconds per song depending on your internet speed.

**Q: Can I pause and resume?**
A: Not currently - the tool processes all songs in one run.

**Q: What if I want the whole song?**
A: Set `start: "0:00"` and `end` to the full length (or longer, it will auto-trim).

**Q: Can I use this for other events?**
A: Absolutely! Works for any playlist - birthday parties, workouts, study music, etc.

## 🌟 Example Workflow

1. **Collect your songs:** Browse YouTube, save links
2. **Note timestamps:** Watch each video, write down start/end times
3. **Create config:** Use the example as a template
4. **Run tool:** `python mehndi_playlist.py my_songs.json`
5. **Get ZIP:** Share the ZIP file or copy individual MP3s
6. **Enjoy:** Play at your event in perfect order!

## 📝 Sample Timeline

For a 2-hour mehndi event:
- 10-15 songs (4-6 minutes each)
- Mix of energy levels (fast/slow)
- Start with welcoming songs
- Peak energy in the middle
- Wind down towards the end

Your config file becomes your setlist - easy to adjust and share!

---

**Happy celebrating! 🎉**

*Made with ❤️ for easy event planning*
