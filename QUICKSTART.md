# 🚀 Quick Start Guide

Get your Movie Poster Face Swap API running in 5 minutes!

## ⚡ Fast Track

### Option 1: Docker (Easiest)

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd movie-poster

# 2. Start with Docker
docker-compose up -d

# 3. Wait for models to download (first time only)
docker-compose logs -f

# 4. Use the API
curl -X POST "http://localhost:8000/swap" \
  -F "movie_poster=@your_poster.jpg" \
  -F "couples_photo=@your_couple.jpg" \
  --output result.jpg
```

### Option 2: Python (Quick)

```bash
# 1. Clone repository
git clone <your-repo-url>
cd movie-poster

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start API server
python api.py

# 4. In another terminal, test it
python example_client.py poster.jpg couple.jpg output.jpg
```

### Option 3: Local Script (No API)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run directly
python swap_local.py poster.jpg couple.jpg output.jpg
```

## 🎯 What You Need

**Required:**
- Python 3.8+ OR Docker
- 5GB+ RAM
- 2GB disk space

**Optional (for speed):**
- NVIDIA GPU with 8GB+ VRAM
- CUDA installed

## 📸 Preparing Your Images

### Movie Poster
- ✅ Clear, visible faces
- ✅ Front-facing preferred
- ✅ At least 512px resolution
- ✅ JPG, PNG formats

### Couples Photo
- ✅ Should have 2 faces
- ✅ Well-lit, clear faces
- ✅ Front-facing preferred
- ✅ High resolution recommended

## 🧪 Test It

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🆘 Quick Troubleshooting

### "Killed" Error
→ Need more RAM (5GB minimum)

### "No faces detected"
→ Use clearer images with visible faces

### Slow processing
→ First run downloads models (~500MB)
→ Use GPU version or disable face enhancement

### Connection refused
→ Check if API is running: `curl http://localhost:8000/health`

## 📚 Next Steps

1. Read [MOVIE_POSTER_README.md](MOVIE_POSTER_README.md) for full documentation
2. Try the examples in the README
3. Customize the API for your needs
4. Deploy to production

## 💡 Pro Tips

1. **First Run**: Models download automatically (~500MB), be patient
2. **GPU**: 10x faster processing with CUDA GPU
3. **Batch**: Process multiple posters programmatically
4. **Quality**: Use high-resolution images for best results
5. **Enhancement**: Toggle face enhancement for speed vs quality

## 🎉 You're Ready!

Start swapping faces on movie posters and have fun! 🎬✨
