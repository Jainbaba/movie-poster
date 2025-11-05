"""
Gradio App for Movie Poster Face Swap
Perfect for Hugging Face Spaces deployment with FREE GPU!
"""

import gradio as gr
import cv2
import numpy as np
from face2face.core.face2face import Face2Face
import logging
import requests
from PIL import Image
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable for model (lazy loading)
f2f_model = None

def get_model():
    """Lazy load the Face2Face model"""
    global f2f_model
    if f2f_model is None:
        logger.info("Loading Face2Face model...")
        f2f_model = Face2Face(device_id=0)
        logger.info("Model loaded successfully!")
    return f2f_model


def download_image_from_url(url):
    """
    Download image from URL and convert to numpy array

    Args:
        url: Image URL

    Returns:
        numpy array (RGB format) or None if failed
    """
    try:
        logger.info(f"Downloading image from URL: {url}")

        # Add headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Convert to PIL Image
        img = Image.open(BytesIO(response.content))

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert to numpy array
        img_array = np.array(img)

        logger.info(f"Successfully downloaded image: {img_array.shape}")
        return img_array

    except Exception as e:
        logger.error(f"Error downloading image from URL: {str(e)}")
        return None


def swap_faces_gradio(movie_poster, poster_url, couples_photo, couple_url, enhance_faces=True):
    """
    Swap faces from couples photo onto movie poster

    Args:
        movie_poster: PIL Image or numpy array (uploaded file)
        poster_url: URL string for poster image
        couples_photo: PIL Image or numpy array (uploaded file)
        couple_url: URL string for couple image
        enhance_faces: Whether to enhance face quality

    Returns:
        Swapped image as numpy array
    """
    try:
        # Handle movie poster input (file upload or URL)
        if poster_url and poster_url.strip():
            logger.info("Using poster from URL")
            poster_img = download_image_from_url(poster_url.strip())
            if poster_img is None:
                return None, "❌ Error: Failed to download movie poster from URL. Please check the URL."
        elif movie_poster is not None:
            logger.info("Using uploaded poster file")
            # Convert PIL to numpy if needed
            if not isinstance(movie_poster, np.ndarray):
                poster_img = np.array(movie_poster)
            else:
                poster_img = movie_poster
        else:
            return None, "❌ Error: Please provide a movie poster (upload file or enter URL)"

        # Handle couples photo input (file upload or URL)
        if couple_url and couple_url.strip():
            logger.info("Using couple photo from URL")
            couple_img = download_image_from_url(couple_url.strip())
            if couple_img is None:
                return None, "❌ Error: Failed to download couples photo from URL. Please check the URL."
        elif couples_photo is not None:
            logger.info("Using uploaded couple photo file")
            # Convert PIL to numpy if needed
            if not isinstance(couples_photo, np.ndarray):
                couple_img = np.array(couples_photo)
            else:
                couple_img = couples_photo
        else:
            return None, "❌ Error: Please provide a couples photo (upload file or enter URL)"

        # Convert RGB to BGR (OpenCV format)
        poster_img = cv2.cvtColor(poster_img, cv2.COLOR_RGB2BGR)
        couple_img = cv2.cvtColor(couple_img, cv2.COLOR_RGB2BGR)

        logger.info(f"Processing - Poster: {poster_img.shape}, Couple: {couple_img.shape}")

        # Get model
        f2f = get_model()

        # Detect faces
        logger.info("Detecting faces in couples photo...")
        couple_faces = f2f.detect_faces(couple_img)

        if len(couple_faces) == 0:
            return None, "❌ Error: No faces detected in couples photo. Please upload a clear photo with visible faces."

        logger.info(f"Found {len(couple_faces)} face(s) in couples photo")

        logger.info("Detecting faces in movie poster...")
        poster_faces = f2f.detect_faces(poster_img)

        if len(poster_faces) == 0:
            return None, "❌ Error: No faces detected in movie poster. Please upload a poster with visible faces."

        logger.info(f"Found {len(poster_faces)} face(s) in movie poster")

        # Perform face swap
        logger.info("Swapping faces...")
        enhancement = 'gpen_bfr_512' if enhance_faces else None

        swapped_result = f2f.swap(
            media=(couple_img, poster_img),
            faces=couple_faces,
            enhance_face_model=enhancement
        )

        # Extract image from result
        if hasattr(swapped_result, 'get_image'):
            swapped_img = swapped_result.get_image()
        elif isinstance(swapped_result, np.ndarray):
            swapped_img = swapped_result
        else:
            swapped_img = np.array(swapped_result)

        # Convert BGR back to RGB for display
        swapped_img = cv2.cvtColor(swapped_img, cv2.COLOR_BGR2RGB)

        logger.info("Face swapping completed successfully!")

        info_msg = f"""
✅ **Success!**
- Found {len(couple_faces)} face(s) in couples photo
- Found {len(poster_faces)} face(s) in movie poster
- Face swapping completed
- Enhancement: {'Enabled (GPEN)' if enhance_faces else 'Disabled'}
"""

        return swapped_img, info_msg

    except Exception as e:
        error_msg = f"❌ Error during face swapping: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None, error_msg


# Create Gradio interface
def create_interface():
    """Create the Gradio interface"""

    # Custom CSS for better styling
    css = """
    .gradio-container {
        max-width: 1200px;
        margin: auto;
    }
    .output-image {
        max-height: 600px;
    }
    footer {
        display: none !important;
    }
    """

    with gr.Blocks(css=css, theme=gr.themes.Soft(), title="Movie Poster Face Swap") as demo:
        gr.Markdown(
            """
            # 🎬 Movie Poster Face Swap

            Swap faces from a couples photo onto a movie poster using AI!

            **How it works:**
            1. **Upload** a movie poster OR **paste a URL** (with visible faces)
            2. **Upload** a couples photo OR **paste a URL** (with 2 faces)
            3. Click "Swap Faces" and wait for the magic! ✨

            *Powered by InsightFace, GPEN, and Face2Face*
            """
        )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📸 Movie Poster")
                poster_input = gr.Image(
                    label="Upload Movie Poster",
                    type="numpy",
                    sources=["upload", "clipboard"],
                    height=350
                )
                poster_url_input = gr.Textbox(
                    label="🔗 OR Enter Image URL",
                    placeholder="https://example.com/movie-poster.jpg",
                    lines=1
                )
                gr.Markdown("*Either upload a file or enter a URL (URL takes priority)*")

            with gr.Column():
                gr.Markdown("### 👥 Couples Photo")
                couple_input = gr.Image(
                    label="Upload Couples Photo",
                    type="numpy",
                    sources=["upload", "clipboard"],
                    height=350
                )
                couple_url_input = gr.Textbox(
                    label="🔗 OR Enter Image URL",
                    placeholder="https://example.com/couple-photo.jpg",
                    lines=1
                )
                gr.Markdown("*Either upload a file or enter a URL (URL takes priority)*")

        with gr.Row():
            enhance_checkbox = gr.Checkbox(
                label="✨ Enhance Face Quality (slower but better results)",
                value=True
            )

        with gr.Row():
            swap_btn = gr.Button("🔄 Swap Faces", variant="primary", size="lg")
            clear_btn = gr.Button("🗑️ Clear", variant="secondary")

        with gr.Row():
            output_image = gr.Image(
                label="🎉 Result",
                type="numpy",
                height=600,
                elem_classes="output-image"
            )

        with gr.Row():
            info_output = gr.Markdown(label="Info")

        gr.Markdown(
            """
            ## 💡 Tips for Best Results

            - ✅ Use high-resolution images (at least 512px)
            - ✅ Ensure faces are clearly visible and well-lit
            - ✅ Front-facing photos work best
            - ✅ First run may take 1-2 minutes (downloading AI models)
            - ⚡ Processing takes 10-30 seconds depending on image size

            ## 📝 Notes

            - The app uses AI to detect and swap faces automatically
            - Face enhancement improves quality but takes longer
            - Works best with 2 faces in the couples photo
            - If there are more faces in the poster, they'll be swapped in order

            ## ⚠️ Ethical Use

            - Only use with consent of people in photos
            - For entertainment and personal use only
            - Do not create misleading or harmful content

            ---

            **Source Code**: [GitHub](https://github.com/your-repo)
            **Based on**: [face2face](https://github.com/SocAIty/face2face) | [InsightFace](https://github.com/deepinsight/insightface)
            """
        )

        # Event handlers
        swap_btn.click(
            fn=swap_faces_gradio,
            inputs=[poster_input, poster_url_input, couple_input, couple_url_input, enhance_checkbox],
            outputs=[output_image, info_output]
        )

        clear_btn.click(
            fn=lambda: (None, "", None, "", None, ""),
            outputs=[poster_input, poster_url_input, couple_input, couple_url_input, output_image, info_output]
        )

    return demo


# Launch the app
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
