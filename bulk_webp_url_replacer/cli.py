"""CLI interface for bulk-webp-url-replacer."""
import argparse
import sys
from .pipeline import ImageETL


def main():
    parser = argparse.ArgumentParser(
        prog="bulk-webp-url-replacer",
        description="Bulk convert images to WebP and update URLs in markdown files"
    )
    
    parser.add_argument(
        "--content", 
        required=True, 
        help="Content directory with markdown files"
    )
    parser.add_argument(
        "--raw-dir", 
        required=True, 
        help="Directory to save raw downloaded images"
    )
    parser.add_argument(
        "--webp-dir", 
        required=True, 
        help="Directory to save converted WebP images"
    )
    parser.add_argument(
        "--webp-base-url", 
        help="Base URL prefix for WebP images in markdown"
    )
    parser.add_argument(
        "--quality", 
        type=int, 
        default=80, 
        help="WebP quality 1-100 (default: 80)"
    )
    parser.add_argument(
        "--width", 
        type=int, 
        default=1200, 
        help="Max image width in pixels (default: 1200)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Preview without making changes"
    )

    args = parser.parse_args()

    etl = ImageETL(
        content_dir=args.content,
        raw_dir=args.raw_dir,
        webp_dir=args.webp_dir,
        webp_base_url=args.webp_base_url,
        quality=args.quality,
        max_width=args.width
    )
    
    result = etl.run(dry_run=args.dry_run)
    
    if result.errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
