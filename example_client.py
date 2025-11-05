"""
Example client for Movie Poster Face Swap API

This script demonstrates how to use the face swap API programmatically.
"""

import requests
import sys
from pathlib import Path


def swap_faces(
    api_url: str,
    poster_path: str,
    couples_path: str,
    output_path: str,
    enhance_faces: bool = True
):
    """
    Swap faces from a couples photo onto a movie poster.

    Args:
        api_url: The API endpoint URL (e.g., http://localhost:8000/swap)
        poster_path: Path to the movie poster image
        couples_path: Path to the couples photo
        output_path: Path where to save the result
        enhance_faces: Whether to enhance face quality
    """
    print(f"🎬 Movie Poster Face Swap")
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

    # Prepare files for upload
    files = {
        'movie_poster': ('poster.jpg', open(poster_path, 'rb'), 'image/jpeg'),
        'couples_photo': ('couple.jpg', open(couples_path, 'rb'), 'image/jpeg')
    }

    data = {
        'enhance_faces': str(enhance_faces).lower()
    }

    try:
        print("🔄 Sending request to API...")
        response = requests.post(api_url, files=files, data=data, timeout=120)

        if response.status_code == 200:
            # Save the result
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ Success! Swapped poster saved to: {output_path}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.json()}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Is the server running?")
        print("   Start the server with: python api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    finally:
        # Close files
        for file_tuple in files.values():
            file_tuple[1].close()


def main():
    """Main function"""
    if len(sys.argv) < 4:
        print("Usage: python example_client.py <poster_path> <couples_path> <output_path>")
        print()
        print("Example:")
        print("  python example_client.py poster.jpg couple.jpg swapped_poster.jpg")
        sys.exit(1)

    poster_path = sys.argv[1]
    couples_path = sys.argv[2]
    output_path = sys.argv[3]

    # API endpoint (change if running on a different host/port)
    api_url = "http://localhost:8000/swap"

    success = swap_faces(api_url, poster_path, couples_path, output_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
