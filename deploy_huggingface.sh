#!/bin/bash

# Quick deployment script for Hugging Face Spaces
# This prepares the repository for HF Spaces deployment

echo "🚀 Preparing deployment for Hugging Face Spaces"
echo "================================================"
echo ""

# Check if HF username is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide your Hugging Face username"
    echo ""
    echo "Usage: ./deploy_huggingface.sh YOUR_HF_USERNAME"
    echo ""
    echo "Example: ./deploy_huggingface.sh johndoe"
    exit 1
fi

HF_USERNAME=$1
SPACE_NAME="movie-poster-face-swap"

echo "📝 Configuration:"
echo "   Username: $HF_USERNAME"
echo "   Space Name: $SPACE_NAME"
echo ""

# Create deployment branch
echo "🌿 Creating deployment branch..."
git checkout -b huggingface-deploy 2>/dev/null || git checkout huggingface-deploy

# Copy Gradio app as main app
echo "📋 Copying Gradio files..."
cp app_gradio.py app.py
cp requirements_gradio.txt requirements.txt
cp README_HUGGINGFACE.md README.md

# Commit changes
echo "💾 Committing changes..."
git add app.py requirements.txt README.md
git commit -m "Prepare for Hugging Face Spaces deployment"

# Add HF remote
echo "🔗 Adding Hugging Face remote..."
git remote remove hf 2>/dev/null
git remote add hf https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME

echo ""
echo "✅ Repository prepared for deployment!"
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Create a Space on Hugging Face:"
echo "   → Go to https://huggingface.co/spaces"
echo "   → Click 'New Space'"
echo "   → Name: $SPACE_NAME"
echo "   → License: gpl-3.0"
echo "   → SDK: Gradio"
echo ""
echo "2. Push to Hugging Face:"
echo "   → git push hf huggingface-deploy:main"
echo ""
echo "3. Enable FREE GPU:"
echo "   → Go to Space Settings → Hardware"
echo "   → Select 'GPU T4 - small' (FREE for public spaces)"
echo ""
echo "4. Your app will be live at:"
echo "   → https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "🎉 Ready to deploy! Run:"
echo "   git push hf huggingface-deploy:main"
echo ""
