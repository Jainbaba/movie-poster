"""
Local face swapping script (no API required)

This script performs face swapping directly without needing to run the API server.
Useful for quick testing and batch processing.
"""

import cv2
import sys
from pathlib import Path
from face2face.core.face2face import Face2Face


def swap_faces_local(poster_path: str, couples_path: str, output_path: str):
    """
    Swap faces from a couples photo onto a movie poster (local execution).

    Args:
        poster_path: Path to the movie poster image
        couples_path: Path to the couples photo
        output_path: Path where to save the result
    """
    print("🎬 Movie Poster Face Swap (Local)")
    print("=" * 50)
    print(f"📸 Poster: {poster_path}")
    print(f"👥 Couple: {couples_path}")
    print(f"💾 Output: {output_path}")
    print()

    # Check if files exist
    if not Path(poster_path).exists():
        print(f"❌ Error: Poster file not found: {poster_path}")
        return False

    if not Path(couples_path).exists():
        print(f"❌ Error: Couples photo not found: {couples_path}")
        return False

    try:
        # Load images
        print("📂 Loading images...")
        poster_img = cv2.imread(poster_path)
        couple_img = cv2.imread(couples_path)

        if poster_img is None:
            print(f"❌ Error: Could not load poster image")
            return False

        if couple_img is None:
            print(f"❌ Error: Could not load couples photo")
            return False

        print(f"   Poster size: {poster_img.shape[1]}x{poster_img.shape[0]}")
        print(f"   Couple size: {couple_img.shape[1]}x{couple_img.shape[0]}")
        print()

        # Initialize Face2Face
        print("🤖 Initializing Face2Face model...")
        print("   (First run may take time to download models)")
        f2f = Face2Face(device_id=0)
        print("   ✅ Model loaded")
        print()

        # Detect faces in couples photo
        print("👤 Detecting faces in couples photo...")
        couple_faces = f2f.detect_faces(couple_img)
        print(f"   Found {len(couple_faces)} face(s)")

        if len(couple_faces) == 0:
            print("❌ Error: No faces detected in couples photo")
            return False

        if len(couple_faces) > 2:
            print(f"⚠️  Warning: Found {len(couple_faces)} faces, using first 2")
            couple_faces = couple_faces[:2]

        # Detect faces in poster
        print()
        print("🎭 Detecting faces in movie poster...")
        poster_faces = f2f.detect_faces(poster_img)
        print(f"   Found {len(poster_faces)} face(s)")

        if len(poster_faces) == 0:
            print("❌ Error: No faces detected in movie poster")
            return False

        # Perform face swapping
        print()
        print("🔄 Swapping faces...")
        print("   (This may take a minute...)")

        swapped_result = f2f.swap(
            media=(couple_img, poster_img),
            faces=couple_faces,
            enhance_face_model='gpen_bfr_512'  # Use face enhancement
        )

        # Extract the image from result
        if hasattr(swapped_result, 'get_image'):
            swapped_img = swapped_result.get_image()
        elif isinstance(swapped_result, str) and Path(swapped_result).exists():
            swapped_img = cv2.imread(swapped_result)
        else:
            swapped_img = swapped_result

        # Save result
        print()
        print(f"💾 Saving result to: {output_path}")
        cv2.imwrite(output_path, swapped_img, [cv2.IMWRITE_JPEG_QUALITY, 95])

        print()
        print("✅ Success! Face swapping completed!")
        print(f"   Output saved to: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error during face swapping: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    if len(sys.argv) < 4:
        print("Movie Poster Face Swap - Local Execution")
        print()
        print("Usage: python swap_local.py <poster_path> <couples_path> <output_path>")
        print()
        print("Example:")
        print("  python swap_local.py poster.jpg couple.jpg swapped_poster.jpg")
        print()
        print("Note: This runs locally without needing the API server.")
        print("      First run will download AI models (~500MB)")
        sys.exit(1)

    poster_path = sys.argv[1]
    couples_path = sys.argv[2]
    output_path = sys.argv[3]

    success = swap_faces_local(poster_path, couples_path, output_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
