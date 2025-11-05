# 🔗 Using Image URLs

You can now use **image URLs** instead of uploading files! This makes it super easy to swap faces on movie posters you find online.

## 🌟 New Features

### ✅ Gradio App (Web Interface)
- **URL Input Fields** for both poster and couple photo
- **Choose Either**: Upload a file OR paste a URL
- **URL Priority**: If you provide a URL, it will be used instead of uploaded file

### ✅ API Endpoints
- **New `/swap-url` endpoint**: Use URLs instead of file uploads
- **Original `/swap` endpoint**: Still works with file uploads
- **Both work perfectly!**

---

## 📖 How to Use

### Option 1: Gradio Web Interface

**Simply paste URLs:**

1. Go to the Gradio interface
2. Instead of uploading files, **paste URLs** in the text boxes:
   - Movie Poster URL: `https://example.com/poster.jpg`
   - Couples Photo URL: `https://example.com/couple.jpg`
3. Click "Swap Faces"!

**Example URLs you can try:**
```
Movie Poster: https://image.tmdb.org/t/p/original/[movie-id].jpg
Couple Photo: https://picsum.photos/800/600
```

---

### Option 2: API with URLs

**Using cURL:**

```bash
curl -X POST "http://localhost:8000/swap-url" \
  -F "poster_url=https://example.com/poster.jpg" \
  -F "couple_url=https://example.com/couple.jpg" \
  --output swapped_poster.jpg
```

**Using Python:**

```python
import requests

data = {
    'poster_url': 'https://example.com/poster.jpg',
    'couple_url': 'https://example.com/couple.jpg',
    'enhance_faces': True
}

response = requests.post('http://localhost:8000/swap-url', data=data)

with open('result.jpg', 'wb') as f:
    f.write(response.content)
```

**Using the example script:**

```bash
python example_url.py \
  "https://example.com/poster.jpg" \
  "https://example.com/couple.jpg" \
  output.jpg
```

---

### Option 3: Mix & Match

You can even **mix file uploads and URLs**!

**In Gradio:**
- Upload a poster file + Paste a couple photo URL
- Or vice versa!

**In API:**
- Use `/swap` for file uploads
- Use `/swap-url` for URLs
- Choose what works best for your workflow

---

## 🎯 Why Use URLs?

### ✅ Benefits:

1. **No Download Needed**: Work directly with online images
2. **Faster Testing**: Copy-paste URLs instead of downloading
3. **Easy Sharing**: Share URLs instead of large files
4. **Save Bandwidth**: No need to upload large files
5. **Bulk Processing**: Automate with lists of URLs

### 💡 Use Cases:

- Swap faces on movie posters from TMDB/IMDB
- Use images from your cloud storage (Dropbox, Google Drive)
- Process images from Instagram, Pinterest, etc.
- Automate batch processing with URL lists
- Quick demos and testing

---

## 📋 Supported URL Formats

### ✅ Works With:

- Direct image URLs: `https://example.com/image.jpg`
- HTTPS and HTTP
- JPG, JPEG, PNG, GIF formats
- Public URLs (no authentication required)

### ❌ Doesn't Work With:

- URLs requiring login/authentication
- URLs behind paywalls
- Redirects to non-image content
- Blocked by CORS/firewall

---

## 🔒 Privacy & Security

**Important Notes:**

- ✅ **Images are downloaded to server temporarily**
- ✅ **Processed and deleted immediately**
- ✅ **Not stored permanently**
- ⚠️ **Only use public, non-sensitive images**
- ⚠️ **Don't use URLs with personal/private photos**

---

## 🎨 Examples

### Example 1: Gradio Interface

```
1. Open Gradio app: http://localhost:7860
2. Paste movie poster URL:
   https://image.tmdb.org/t/p/original/xyz.jpg
3. Paste couples photo URL:
   https://your-cloud-storage.com/couple.jpg
4. Click "Swap Faces"
5. Download result!
```

### Example 2: Python Script

```python
# example_url.py usage
python example_url.py \
  "https://example.com/avengers-poster.jpg" \
  "https://example.com/us-together.jpg" \
  our_avengers_poster.jpg
```

### Example 3: cURL Command

```bash
# Quick test with curl
curl -X POST "http://localhost:8000/swap-url" \
  -F "poster_url=https://picsum.photos/800/1200" \
  -F "couple_url=https://picsum.photos/800/600" \
  -F "enhance_faces=true" \
  --output test_result.jpg
```

### Example 4: Batch Processing

```python
import requests

posters = [
    'https://example.com/poster1.jpg',
    'https://example.com/poster2.jpg',
    'https://example.com/poster3.jpg'
]

couple_url = 'https://example.com/our-photo.jpg'

for i, poster_url in enumerate(posters):
    response = requests.post(
        'http://localhost:8000/swap-url',
        data={
            'poster_url': poster_url,
            'couple_url': couple_url,
            'enhance_faces': True
        }
    )

    with open(f'result_{i}.jpg', 'wb') as f:
        f.write(response.content)

    print(f"✅ Processed poster {i+1}")
```

---

## 🆘 Troubleshooting

### "Failed to download image from URL"

**Possible Causes:**
1. URL is not publicly accessible
2. URL requires authentication
3. Image format not supported
4. Network/firewall blocking the request

**Solutions:**
1. ✅ Make sure URL is public and directly accessible
2. ✅ Test URL in browser first
3. ✅ Use direct image URLs (not webpage URLs)
4. ✅ Check if URL is blocked by firewall

### "Connection refused"

**Solution**: Make sure the API server is running:
```bash
python api.py
```

### "Timeout error"

**Solution**:
- Image might be too large
- Slow network connection
- Increase timeout in your request

---

## 📚 API Documentation

### Endpoints

**GET /** - API info
**POST /swap** - File upload endpoint
**POST /swap-url** - URL endpoint (NEW!)
**POST /swap-advanced** - Advanced with mapping
**GET /health** - Health check
**GET /docs** - Interactive API docs

### Try It Out!

Visit the interactive docs:
- Swagger UI: http://localhost:8000/docs
- You can test the `/swap-url` endpoint directly in the browser!

---

## 🎉 Summary

**New Features:**
- ✅ URL support in Gradio interface
- ✅ New `/swap-url` API endpoint
- ✅ Mix file uploads and URLs
- ✅ Example scripts included

**Try it now:**
1. Start the app: `python app_gradio.py` or `python api.py`
2. Paste image URLs instead of uploading
3. Get instant results!

**Perfect for:**
- Quick testing with online images
- Batch processing with URL lists
- Sharing and collaboration
- Cloud-based workflows

---

**Questions?** Check the [main documentation](MOVIE_POSTER_README.md) or open an issue!
