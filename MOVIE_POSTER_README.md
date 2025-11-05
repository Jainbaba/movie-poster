# 🎬 Movie Poster Face Swap API

A **FREE**, open-source API for swapping faces from a couples photo onto a movie poster using AI-powered face detection and swapping technology.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/FastAPI-0.104+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License">
</p>

## ✨ Features

- 🎭 **Face Swapping**: Automatically detect and swap faces from a couples photo onto movie posters
- 🚀 **Fast API**: RESTful API built with FastAPI for easy integration
- 🤖 **AI-Powered**: Uses InsightFace's state-of-the-art face detection and swapping models
- ✨ **Face Enhancement**: Optional face quality enhancement with GPEN/GFPGAN models
- 🆓 **100% Free**: No API keys, no subscriptions, completely free and open source
- 🐳 **Easy Deployment**: Simple setup with Python or Docker

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
  - [Method 1: API Server](#method-1-api-server-recommended)
  - [Method 2: Local Script](#method-2-local-script)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

## 🎯 How It Works

1. **Upload** a movie poster and a couples photo
2. **Detect** faces in both images using AI
3. **Swap** the faces from the couples photo onto the poster
4. **Enhance** face quality for realistic results
5. **Download** your personalized movie poster!

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- 5GB+ RAM (8GB recommended)
- Optional: GPU with 8GB+ VRAM for faster processing

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd movie-poster
```

### Step 2: Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

**Note**: First run will automatically download AI models (~500MB)

### Alternative: CPU-Only Installation

If you don't have a GPU, modify `requirements.txt` to use CPU-only ONNX runtime:

```bash
# Replace onnxruntime-gpu with onnxruntime
pip install onnxruntime>=1.23.0
```

## 📖 Usage

### Method 1: API Server (Recommended)

#### Start the Server

```bash
python api.py
```

The API will be available at `http://localhost:8000`

#### Use the API

**Option A: Using cURL**

```bash
curl -X POST "http://localhost:8000/swap" \
  -F "movie_poster=@path/to/poster.jpg" \
  -F "couples_photo=@path/to/couple.jpg" \
  --output swapped_poster.jpg
```

**Option B: Using the Python Client**

```bash
python example_client.py poster.jpg couple.jpg output.jpg
```

**Option C: Using Any HTTP Client**

Send a POST request to `/swap` with two files:
- `movie_poster`: Your movie poster image
- `couples_photo`: Photo with the couple's faces

### Method 2: Local Script

No API server needed - direct face swapping:

```bash
python swap_local.py poster.jpg couple.jpg output.jpg
```

## 📚 API Documentation

### Endpoints

#### `GET /`
Health check and API information

#### `POST /swap`
Basic face swapping endpoint

**Parameters:**
- `movie_poster` (file, required): Movie poster image
- `couples_photo` (file, required): Couples photo with 2 faces
- `enhance_faces` (bool, optional): Enable face enhancement (default: true)
- `enhancement_model` (string, optional): Enhancement model (default: "gpen_bfr_512")

**Returns:**
- JPEG image with swapped faces

**Example:**
```python
import requests

files = {
    'movie_poster': open('poster.jpg', 'rb'),
    'couples_photo': open('couple.jpg', 'rb')
}

response = requests.post('http://localhost:8000/swap', files=files)

with open('result.jpg', 'wb') as f:
    f.write(response.content)
```

#### `POST /swap-advanced`
Advanced face swapping with custom face mapping

**Additional Parameters:**
- `face_mapping` (string, optional): Custom face mapping like "0:0,1:1"

#### `GET /health`
Health check endpoint

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎨 Examples

### Example 1: Simple Face Swap

```bash
# Using the Python client
python example_client.py movie_poster.jpg couple_photo.jpg result.jpg
```

### Example 2: Batch Processing

```python
from face2face.core.face2face import Face2Face
import cv2

f2f = Face2Face()

posters = ['poster1.jpg', 'poster2.jpg', 'poster3.jpg']
couple_photo = 'couple.jpg'

for i, poster in enumerate(posters):
    result = f2f.swap(
        media=(cv2.imread(couple_photo), cv2.imread(poster)),
        enhance_face_model='gpen_bfr_512'
    )
    cv2.imwrite(f'output_{i}.jpg', result.get_image())
```

### Example 3: Using Different Enhancement Models

Available enhancement models:
- `gpen_bfr_512`: Best quality, slower (default)
- `gpen_bfr_256`: Balanced
- `gfpgan_1.4`: Faster, good quality
- `None`: No enhancement (fastest)

```bash
curl -X POST "http://localhost:8000/swap" \
  -F "movie_poster=@poster.jpg" \
  -F "couples_photo=@couple.jpg" \
  -F "enhancement_model=gfpgan_1.4" \
  --output result.jpg
```

## 💻 Requirements

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 5GB | 8GB+ |
| GPU | None (CPU works) | NVIDIA GPU with 8GB+ VRAM |
| Storage | 2GB | 5GB+ |

### Software Requirements

- Python 3.8+
- OpenCV
- FastAPI
- ONNX Runtime (CPU or GPU)
- InsightFace models (auto-downloaded)

## 🐛 Troubleshooting

### "Killed" Error

**Problem**: Process gets killed without error message

**Solution**: Insufficient RAM. Need at least 5GB of available RAM. Close other applications or upgrade RAM.

### "No faces detected"

**Problem**: API returns "No faces detected in couples photo/movie poster"

**Solutions**:
1. Ensure faces are clearly visible and not too small
2. Use high-resolution images (at least 512px)
3. Check that faces are not covered or at extreme angles
4. Ensure good lighting in photos

### Slow Processing

**Problem**: Face swapping takes too long

**Solutions**:
1. Use GPU version: `pip install onnxruntime-gpu`
2. Reduce image resolution before processing
3. Disable face enhancement: `enhance_faces=false`
4. Use faster enhancement model: `enhancement_model=gfpgan_1.4`

### CUDA/GPU Issues

**Problem**: GPU not being used despite having CUDA installed

**Solutions**:
```bash
# Verify CUDA installation
python -c "import onnxruntime as ort; print(ort.get_available_providers())"

# Should include 'CUDAExecutionProvider'

# Install correct CUDA version
pip install onnxruntime-gpu --force-reinstall
```

### Model Download Issues

**Problem**: Models fail to download automatically

**Solution**: Models are downloaded to `~/.insightface/models/`. Check internet connection and disk space.

## 🎯 Use Cases

- 🎬 Create personalized movie posters
- 🎉 Fun photo effects for parties/events
- 🎨 Creative content for social media
- 🎁 Unique gifts with custom posters
- 🎓 Educational projects on AI/Computer Vision

## 🔒 Privacy & Ethics

- **Local Processing**: All processing happens locally on your machine
- **No Data Collection**: No images are sent to external servers
- **Responsible Use**: Only use with consent of people in photos
- **No Deepfakes**: Intended for fun, ethical, consensual use only

**⚠️ Important**: This tool is for entertainment and educational purposes only. Do not:
- Create misleading or harmful content
- Use without consent of people in photos
- Violate anyone's privacy or rights
- Create content that could harm others

## 📄 Credits

This project is built on top of:

- **[face2face](https://github.com/SocAIty/face2face)** by SocAIty - Face swapping SDK
- **[InsightFace](https://github.com/deepinsight/insightface)** - State-of-the-art face analysis
- **[ROOP](https://github.com/s0md3v/roop)** - One-click face swap inspiration
- **[GPEN](https://github.com/yangxy/GPEN)** - Face enhancement models
- **[GFPGAN](https://github.com/TencentARC/GFPGAN)** - Face restoration models

## 📝 License

This project is licensed under the **GNU General Public License v3.0** (GPLv3).

The underlying face2face library is also licensed under GPLv3. See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🌟 Support

If you find this project useful, please:
- ⭐ Star the repository
- 🐛 Report bugs via Issues
- 💡 Suggest features
- 🔀 Submit pull requests

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for the open-source community**

**Powered by**: InsightFace, face2face, FastAPI, Python
