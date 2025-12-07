# 🚀 Deploy Music Playlist Converter to Render

This guide will help you deploy the Music Playlist Converter as a web application on Render.

## 📋 What You'll Get

- 🌐 A live web interface accessible from anywhere
- 📱 Mobile-friendly design
- 🎵 Easy song management - just paste YouTube links
- 📦 Automatic ZIP file creation
- ⚡ Fast processing with progress indicators

## 🔧 Prerequisites

1. **GitHub Account** - Your code needs to be on GitHub
2. **Render Account** - Sign up at [render.com](https://render.com) (free)

## 🚀 Quick Deploy (Method 1: Using render.yaml)

This is the **easiest** method!

### Step 1: Push to GitHub

Make sure all the web app files are in your repository:
```bash
git add app.py templates/ requirements-web.txt render.yaml
git commit -m "Add web application for Render deployment"
git push origin main
```

### Step 2: Connect to Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select your `ytconverter` repository
5. Render will auto-detect the `render.yaml` file
6. Click **"Apply"**

### Step 3: Wait for Build

- Render will automatically:
  - Install Python dependencies
  - Install ffmpeg
  - Deploy your app
- Build time: ~5-10 minutes (first time)

### Step 4: Access Your App

- Once deployed, Render will give you a URL like: `https://music-playlist-converter.onrender.com`
- Share this URL with anyone who needs to create playlists!

## 🛠️ Manual Deploy (Method 2: Web Dashboard)

If render.yaml doesn't work, use manual setup:

### Step 1: Create New Web Service

1. Go to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository

### Step 2: Configure Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `music-playlist-converter` |
| **Region** | Oregon (US West) or your preferred region |
| **Branch** | `main` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements-web.txt && apt-get update && apt-get install -y ffmpeg` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | Free |

### Step 3: Add Environment Variables

Click **"Advanced"** and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SECRET_KEY` | (click "Generate" for random value) |

### Step 4: Deploy

- Click **"Create Web Service"**
- Wait for deployment (~5-10 minutes)
- Your app will be live!

## 🔍 Troubleshooting

### Build Fails - ffmpeg Not Found

**Solution:** Add this to your Build Command:
```bash
apt-get update && apt-get install -y ffmpeg && pip install -r requirements-web.txt
```

### App Times Out on Large Files

**Issue:** Free tier has 512MB RAM limit

**Solutions:**
- Process fewer songs at once (3-5 max)
- Upgrade to paid plan ($7/month for 2GB RAM)
- Use shorter song clips

### yt-dlp Errors

**Common causes:**
- YouTube URL is invalid
- Video is age-restricted or private
- Rate limiting from YouTube

**Solution:**
- Verify URLs work in a browser first
- Try again after a few minutes

### Build Takes Too Long

**Why:** Installing ffmpeg takes 2-3 minutes

**Solution:**
- This is normal for first deployment
- Subsequent deploys are faster (use cached dependencies)

## 📊 Usage Limits (Free Tier)

| Limit | Value |
|-------|-------|
| RAM | 512 MB |
| Build time | 15 minutes max |
| CPU | Shared |
| Bandwidth | 100 GB/month |
| Apps | Unlimited |

**What this means:**
- ~3-5 songs per playlist recommended
- Each song: ~3-5 MB
- Can handle ~20-30 playlists/day comfortably

## 🔄 Updating Your App

After making code changes:

```bash
git add .
git commit -m "Update web app"
git push origin main
```

Render will **automatically redeploy** when you push to main!

## 🎨 Customization

### Change App Name/URL

1. Go to Render Dashboard → Your Service
2. Click **"Settings"**
3. Under "Name" → Change and save
4. New URL: `https://YOUR-NEW-NAME.onrender.com`

### Add Custom Domain

1. In service settings, scroll to "Custom Domains"
2. Add your domain (e.g., `playlist.yourdomain.com`)
3. Update your DNS as instructed
4. Free SSL included!

## 🌐 Using Your App

### For Yourself:

1. Open your Render URL
2. Add your songs:
   - Paste YouTube links
   - Set timestamps (MM:SS format)
3. Click "Create Playlist"
4. Download ZIP when ready!

### For Others:

Share your Render URL! Perfect for:
- Event planners
- DJs
- Wedding coordinators
- Dance teams

## 💰 Cost Breakdown

### Free Tier (Recommended for Personal Use)

- ✅ Everything works
- ✅ Unlimited apps
- ⚠️ Spins down after 15 min inactivity (30 sec to wake up)
- ⚠️ 512MB RAM (limit to 3-5 songs)

### Paid Tier ($7/month)

- ✅ Always on (no spin down)
- ✅ 2GB RAM (10-15 songs per playlist)
- ✅ Faster processing
- ✅ Priority support

## 🔐 Security Notes

- App generates random SECRET_KEY automatically
- Files are deleted after 1 hour
- No data is stored permanently
- HTTPS enabled by default

## 📝 Files Needed for Deployment

Make sure these are in your repository:

```
ytconverter/
├── app.py                      # Flask application
├── templates/
│   └── index.html             # Web interface
├── requirements-web.txt        # Python dependencies
└── render.yaml                # Render configuration (optional)
```

## 🎯 Next Steps After Deployment

1. **Test it out** - Create a test playlist
2. **Share the link** - Send to friends/family
3. **Monitor usage** - Check Render dashboard for logs
4. **Upgrade if needed** - If you need more capacity

## 💡 Pro Tips

### Faster Processing

- Trim songs to only what you need (shorter = faster)
- Process in batches (3-5 songs at a time)
- Use common timestamps (0:30 - 2:30 is typical)

### Best Practices

- Test YouTube URLs before adding them
- Use descriptive song names
- Keep timestamps in MM:SS format
- Download ZIP immediately (files expire after 1 hour)

### Sharing with Others

Create a simple landing page with:
```
🎵 Music Playlist Converter

1. Visit: https://your-app.onrender.com
2. Add YouTube links
3. Set timestamps
4. Download your playlist!

Perfect for weddings, events, and parties! 🎉
```

## 📞 Support

### App Issues

- Check Render logs: Dashboard → Your Service → Logs
- Common errors usually show in logs

### Deployment Issues

- Render Docs: https://render.com/docs
- Community: https://community.render.com

### Code Issues

- Check the main README.md
- Review app.py for error messages

## 🎉 Success!

Once deployed, you'll have a professional web app that:
- ✅ Works on any device
- ✅ No installation needed
- ✅ Easy to share
- ✅ Free to use!

Perfect for creating custom playlists without any technical knowledge!

---

**Happy deploying! 🚀**

*Made with ❤️ for easy event planning*
