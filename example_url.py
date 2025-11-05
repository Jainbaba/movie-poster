"""
Example: Using URLs for Movie Poster Face Swap

This script demonstrates how to use image URLs with the face swap API
instead of uploading local files.
"""

import requests
import sys


def swap_faces_from_urls(
    poster_url: str,
    couple_url: str,
    output_path: str,
    api_url: str = "http://localhost:8000/swap-url"
):
    """
    Swap faces using image URLs

    Args:
        poster_url: URL of the movie poster
        couple_url: URL of the couples photo
        output_path: Path to save the result
        api_url: API endpoint URL
    """
    print("🎬 Movie Poster Face Swap (Using URLs)")
    print("=" * 50)
    print(f"📸 Poster URL: {poster_url}")
    print(f"👥 Couple URL: {couple_url}")
    print(f"💾 Output: {output_path}")
    print()

    # Prepare data
    data = {
        'poster_url': poster_url,
        'couple_url': couple_url,
        'enhance_faces': 'true'
    }

    try:
        print("🔄 Sending request to API...")
        print("   (Downloading images and swapping faces...)")

        response = requests.post(api_url, data=data, timeout=120)

        if response.status_code == 200:
            # Save the result
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print()
            print(f"✅ Success! Swapped poster saved to: {output_path}")
            return True
        else:
            print()
            print(f"❌ Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   {error_detail.get('detail', 'Unknown error')}")
            except:
                print(f"   {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print()
        print("❌ Error: Could not connect to API. Is the server running?")
        print("   Start the server with: python api.py")
        return False
    except Exception as e:
        print()
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main function"""
    if len(sys.argv) < 4:
        print("Movie Poster Face Swap - Using URLs")
        print()
        print("Usage: python example_url.py <poster_url> <couple_url> <output_path>")
        print()
        print("Example:")
        print("  python example_url.py \\")
        print("    'https://example.com/poster.jpg' \\")
        print("    'https://example.com/couple.jpg' \\")
        print("    swapped_poster.jpg")
        print()
        print("Real Example (using public images):")
        print("  python example_url.py \\")
        print("    'https://image.tmdb.org/t/p/original/ABC123.jpg' \\")
        print("    'https://picsum.photos/800/600' \\")
        print("    result.jpg")
        sys.exit(1)

    poster_url = sys.argv[1]
    couple_url = sys.argv[2]
    output_path = sys.argv[3]

    success = swap_faces_from_urls(poster_url, couple_url, output_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
