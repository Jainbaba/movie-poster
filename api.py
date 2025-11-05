"""
Movie Poster Face Swap API

A free API for swapping faces from a couples photo onto a movie poster.
This API uses the face2face library powered by InsightFace for face detection and swapping.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import io
import cv2
import numpy as np
from face2face.core.face2face import Face2Face
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Movie Poster Face Swap API",
    description="Swap faces from a couples photo onto a movie poster",
    version="1.0.0"
)

# Initialize Face2Face model (lazy loading)
f2f_instance = None

def get_f2f():
    """Lazy initialization of Face2Face model"""
    global f2f_instance
    if f2f_instance is None:
        logger.info("Initializing Face2Face model...")
        f2f_instance = Face2Face(device_id=0)
        logger.info("Face2Face model initialized successfully")
    return f2f_instance


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Movie Poster Face Swap API is running",
        "endpoints": {
            "swap": "/swap - POST endpoint for face swapping",
            "docs": "/docs - API documentation"
        }
    }


@app.post("/swap")
async def swap_faces(
    movie_poster: UploadFile = File(..., description="Movie poster image"),
    couples_photo: UploadFile = File(..., description="Couples photo with 2 faces"),
    enhance_faces: bool = True,
    enhancement_model: str = "gpen_bfr_512"
):
    """
    Swap faces from a couples photo onto a movie poster.

    Parameters:
    - movie_poster: The movie poster image where faces will be swapped
    - couples_photo: Photo containing the couple's faces (should have 2 faces)
    - enhance_faces: Whether to enhance face quality after swapping (default: True)
    - enhancement_model: Face enhancement model to use (default: gpen_bfr_512)

    Returns:
    - The movie poster with swapped faces

    Example Usage:
    ```bash
    curl -X POST "http://localhost:8000/swap" \\
      -F "movie_poster=@poster.jpg" \\
      -F "couples_photo=@couple.jpg" \\
      --output swapped_poster.jpg
    ```
    """
    try:
        logger.info("Received face swap request")

        # Read uploaded files
        poster_bytes = await movie_poster.read()
        couple_bytes = await couples_photo.read()

        # Convert to numpy arrays
        poster_array = np.frombuffer(poster_bytes, np.uint8)
        couple_array = np.frombuffer(couple_bytes, np.uint8)

        # Decode images
        poster_img = cv2.imdecode(poster_array, cv2.IMREAD_COLOR)
        couple_img = cv2.imdecode(couple_array, cv2.IMREAD_COLOR)

        if poster_img is None or couple_img is None:
            raise HTTPException(status_code=400, detail="Invalid image format")

        logger.info(f"Poster size: {poster_img.shape}, Couple photo size: {couple_img.shape}")

        # Get Face2Face instance
        f2f = get_f2f()

        # Detect faces in couples photo
        logger.info("Detecting faces in couples photo...")
        couple_faces = f2f.detect_faces(couple_img)

        if len(couple_faces) == 0:
            raise HTTPException(
                status_code=400,
                detail="No faces detected in couples photo"
            )

        if len(couple_faces) > 2:
            logger.warning(f"Found {len(couple_faces)} faces in couples photo, using first 2")
            couple_faces = couple_faces[:2]

        logger.info(f"Found {len(couple_faces)} face(s) in couples photo")

        # Detect faces in movie poster
        logger.info("Detecting faces in movie poster...")
        poster_faces = f2f.detect_faces(poster_img)

        if len(poster_faces) == 0:
            raise HTTPException(
                status_code=400,
                detail="No faces detected in movie poster"
            )

        logger.info(f"Found {len(poster_faces)} face(s) in movie poster")

        # Perform face swapping
        # Strategy: Swap each face from the couple onto the poster
        # If there are more faces in the poster than in the couple photo,
        # we'll cycle through the couple's faces
        logger.info("Swapping faces...")

        enhancement = enhancement_model if enhance_faces else None

        # Swap using the tuple format: (source_image, target_image)
        # The faces parameter contains the faces to swap from
        swapped_result = f2f.swap(
            media=(couple_img, poster_img),
            faces=couple_faces,
            enhance_face_model=enhancement
        )

        # Convert result to image
        if hasattr(swapped_result, 'get_image'):
            swapped_img = swapped_result.get_image()
        elif isinstance(swapped_result, np.ndarray):
            swapped_img = swapped_result
        else:
            swapped_img = np.array(swapped_result)

        logger.info("Face swapping completed successfully")

        # Encode result as JPEG
        _, buffer = cv2.imencode('.jpg', swapped_img, [cv2.IMWRITE_JPEG_QUALITY, 95])

        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(buffer.tobytes()),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": "attachment; filename=swapped_poster.jpg"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during face swapping: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Face swapping failed: {str(e)}")


@app.post("/swap-advanced")
async def swap_faces_advanced(
    movie_poster: UploadFile = File(..., description="Movie poster image"),
    couples_photo: UploadFile = File(..., description="Couples photo with 2 faces"),
    face_mapping: Optional[str] = None,
    enhance_faces: bool = True,
    enhancement_model: str = "gpen_bfr_512"
):
    """
    Advanced face swapping with face mapping control.

    Parameters:
    - movie_poster: The movie poster image where faces will be swapped
    - couples_photo: Photo containing the couple's faces (should have 2 faces)
    - face_mapping: Comma-separated mapping like "0:0,1:1" (couple_face_idx:poster_face_idx)
    - enhance_faces: Whether to enhance face quality after swapping (default: True)
    - enhancement_model: Face enhancement model to use (default: gpen_bfr_512)

    Returns:
    - The movie poster with swapped faces
    """
    try:
        logger.info("Received advanced face swap request")

        # Read uploaded files
        poster_bytes = await movie_poster.read()
        couple_bytes = await couples_photo.read()

        # Convert to numpy arrays
        poster_array = np.frombuffer(poster_bytes, np.uint8)
        couple_array = np.frombuffer(couple_bytes, np.uint8)

        # Decode images
        poster_img = cv2.imdecode(poster_array, cv2.IMREAD_COLOR)
        couple_img = cv2.imdecode(couple_array, cv2.IMREAD_COLOR)

        if poster_img is None or couple_img is None:
            raise HTTPException(status_code=400, detail="Invalid image format")

        # Get Face2Face instance
        f2f = get_f2f()

        # Detect faces
        couple_faces = f2f.detect_faces(couple_img)
        poster_faces = f2f.detect_faces(poster_img)

        if len(couple_faces) == 0:
            raise HTTPException(status_code=400, detail="No faces detected in couples photo")
        if len(poster_faces) == 0:
            raise HTTPException(status_code=400, detail="No faces detected in movie poster")

        logger.info(f"Detected {len(couple_faces)} faces in couple photo, {len(poster_faces)} in poster")

        # Apply face mapping if provided
        result_img = poster_img.copy()

        if face_mapping:
            # Parse mapping: "0:0,1:1"
            mappings = face_mapping.split(",")
            for mapping in mappings:
                couple_idx, poster_idx = map(int, mapping.split(":"))
                if couple_idx < len(couple_faces) and poster_idx < len(poster_faces):
                    # Swap individual face
                    result_img = f2f.swap_single_face(
                        result_img,
                        poster_faces[poster_idx],
                        couple_faces[couple_idx],
                        enhance_face_model=enhancement_model if enhance_faces else None
                    )
        else:
            # Default: swap all faces
            enhancement = enhancement_model if enhance_faces else None
            swapped_result = f2f.swap(
                media=(couple_img, poster_img),
                faces=couple_faces,
                enhance_face_model=enhancement
            )

            if hasattr(swapped_result, 'get_image'):
                result_img = swapped_result.get_image()
            elif isinstance(swapped_result, np.ndarray):
                result_img = swapped_result
            else:
                result_img = np.array(swapped_result)

        logger.info("Advanced face swapping completed")

        # Encode and return
        _, buffer = cv2.imencode('.jpg', result_img, [cv2.IMWRITE_JPEG_QUALITY, 95])

        return StreamingResponse(
            io.BytesIO(buffer.tobytes()),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": "attachment; filename=swapped_poster_advanced.jpg"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during advanced face swapping: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Face swapping failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": f2f_instance is not None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
