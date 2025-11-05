# 🚀 Deploy for FREE with GPU

Don't have GPU or storage? No problem! Deploy this app to **FREE** cloud services with GPU support!

## 🌟 Best Option: Hugging Face Spaces (Recommended)

**FREE GPU** • **No Credit Card** • **Simple Deployment**

### Why Hugging Face Spaces?

- ✅ **FREE GPU** (T4 GPU for public spaces)
- ✅ **No credit card required**
- ✅ **Automatic model downloads**
- ✅ **Beautiful web interface**
- ✅ **Easy sharing** (get a public URL)
- ✅ **Auto-scaling**

### 🎯 Deploy to Hugging Face Spaces

#### Step 1: Create Account

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up for free (no credit card needed!)

#### Step 2: Create a Space

1. Click **"New Space"** at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Fill in:
   - **Space name**: `movie-poster-face-swap` (or your choice)
   - **License**: `gpl-3.0`
   - **SDK**: Select **Gradio**
   - **Hardware**: Select **CPU basic** (can upgrade to free GPU later)

#### Step 3: Upload Files

Clone your repo and upload these files to your Space:

**Required Files:**
```
app_gradio.py              # Main Gradio app
requirements_gradio.txt    # Rename to requirements.txt
README_HUGGINGFACE.md      # Rename to README.md
face2face/                 # Entire folder
pyproject.toml
LICENSE
```

**Using Git:**

```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/movie-poster-face-swap
cd movie-poster-face-swap

# Copy files from this repo
cp app_gradio.py .
cp requirements_gradio.txt requirements.txt
cp README_HUGGINGFACE.md README.md
cp -r face2face/ .
cp pyproject.toml .
cp LICENSE .

# Commit and push
git add .
git commit -m "Initial commit"
git push
```

**Or using the Web UI:**
Just drag and drop the files into your Space!

#### Step 4: Enable FREE GPU (Optional but Recommended)

1. Go to your Space settings
2. Under **"Hardware"**, select **"GPU T4 - small"** (FREE for public spaces!)
3. Click **"Update"**

#### Step 5: Wait for Build

- First build takes 3-5 minutes (downloading models)
- Your app will auto-start when ready
- You'll get a public URL like: `https://huggingface.co/spaces/USERNAME/movie-poster-face-swap`

#### Step 6: Share & Use! 🎉

Your app is now live and FREE to use! Share the URL with anyone!

---

## 🔬 Option 2: Google Colab (Testing)

**FREE GPU** • **Great for Testing** • **Not for Deployment**

### Deploy to Google Colab

1. **Open the Colab Notebook**: [Click Here](#) *(we'll create this)*

2. **Or create manually:**

```python
# In a new Colab notebook:

# Install dependencies
!pip install gradio opencv-python-headless face2face

# Clone the repo
!git clone https://github.com/your-repo/movie-poster.git
%cd movie-poster

# Run the Gradio app with public URL
!python app_gradio.py --share
```

3. **Click the public URL** (e.g., `https://xxxxx.gradio.live`)

**Pros**: Free GPU, easy testing
**Cons**: Session expires after inactivity, not permanent

---

## 🎮 Option 3: Replicate (For Developers)

**Pay-per-use** • **API Access** • **Professional**

### Deploy to Replicate

1. **Create account** at [replicate.com](https://replicate.com)
2. **Install Cog**:
   ```bash
   sudo curl -o /usr/local/bin/cog -L https://github.com/replicate/cog/releases/latest/download/cog_`uname -s`_`uname -m`
   sudo chmod +x /usr/local/bin/cog
   ```

3. **Create `cog.yaml`**:
   ```yaml
   build:
     gpu: true
     python_version: "3.10"
     system_packages:
       - "libgl1-mesa-glx"
       - "libglib2.0-0"
     python_packages:
       - "opencv-python-headless==4.8.0"
       - "face2face"
       - "numpy>=1.24.0"
   predict: "predict.py:Predictor"
   ```

4. **Create `predict.py`** (we can provide this)

5. **Push to Replicate**:
   ```bash
   cog push r8.im/your-username/movie-poster-swap
   ```

**Pros**: Professional API, pay-per-use
**Cons**: Requires credit card (free tier available)

---

## 📊 Comparison

| Service | Cost | GPU | Persistent | Best For |
|---------|------|-----|------------|----------|
| **Hugging Face Spaces** | FREE | ✅ T4 | ✅ Yes | **Recommended - Best overall** |
| **Google Colab** | FREE | ✅ T4/K80 | ❌ No | Testing & experiments |
| **Replicate** | Pay-per-use | ✅ A40 | ✅ Yes | Production API |
| **Kaggle** | FREE | ✅ P100 | ❌ No | Data science / testing |

---

## 🎯 Quick Start: Hugging Face Spaces (Full Guide)

### Video Tutorial

*(Coming soon - we can add a YouTube tutorial)*

### Step-by-Step with Screenshots

**1. Create Space**

```bash
# On Hugging Face, click "New Space"
Name: movie-poster-face-swap
License: gpl-3.0
SDK: Gradio
Hardware: CPU basic (upgrade to GPU later)
```

**2. Prepare Files**

```bash
# In your local repo
cd movie-poster

# Create a new branch for HF deployment
git checkout -b huggingface-deploy

# Copy Gradio app as main app
cp app_gradio.py app.py

# Use Gradio requirements
cp requirements_gradio.txt requirements.txt

# Use HF README
cp README_HUGGINGFACE.md README.md
```

**3. Push to Hugging Face**

```bash
# Add HF as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/movie-poster-face-swap

# Push
git add .
git commit -m "Deploy to Hugging Face Spaces"
git push hf huggingface-deploy:main
```

**4. Enable GPU**

- Go to Settings → Hardware
- Select "GPU T4 - small" (FREE for public spaces)
- Click "Save"

**5. Done! 🎉**

Your app will be live at:
```
https://huggingface.co/spaces/YOUR_USERNAME/movie-poster-face-swap
```

---

## 🆘 Troubleshooting

### Space won't build

**Issue**: Build fails or times out

**Solution**:
1. Check `requirements.txt` is correct
2. Ensure all files are uploaded
3. Check the build logs for errors

### Out of memory

**Issue**: "Killed" error or OOM

**Solution**:
1. Enable GPU hardware in settings
2. Reduce image sizes in preprocessing
3. Use CPU-only ONNX runtime if needed

### Models not downloading

**Issue**: Face detection models fail to download

**Solution**:
1. Models auto-download on first run
2. Be patient (takes 2-3 minutes)
3. Check Space logs for download progress

---

## 💡 Pro Tips

1. **Use GPU**: Always enable the free T4 GPU for better performance
2. **Public = Free GPU**: Keep your Space public to get free GPU access
3. **Examples**: Add example images to your Space for users to try
4. **Analytics**: Enable analytics to see usage stats
5. **Gradio Share**: Use `.launch(share=True)` for temporary testing links

---

## 📚 Additional Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs)
- [Google Colab Guide](https://colab.research.google.com/)
- [Replicate Documentation](https://replicate.com/docs)

---

## 🎉 You're All Set!

Deploy to Hugging Face Spaces and enjoy **FREE GPU-powered face swapping**! 🚀

**Questions?** Open an issue on GitHub or ask on Hugging Face community forums.
