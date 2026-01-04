# bulk-webp-url-replacer

Bulk convert images to WebP and automatically update URLs in markdown files with a custom CDN prefix.

## Features

- 🔍 **Extract** image URLs from markdown files (frontmatter, galleries, inline images)
- 📥 **Download** images from remote URLs
- 🖼️ **Convert** to optimized WebP format
- 🔄 **Replace** original URLs with new CDN-prefixed paths
- ⏭️ **Skip** already-processed images on subsequent runs
- 👀 **Dry-run** mode to preview changes

## Installation

```bash
pip install bulk-webp-url-replacer
```

Or install from source:

```bash
git clone https://github.com/HoangGeek/bulk-webp-url-replacer.git
cd bulk-webp-url-replacer
pip install -e .
```

## Usage

### CLI

```bash
# Dry run - preview what would be processed
bulk-webp-url-replacer \
  --content ./content \
  --raw-dir ./raw_images \
  --webp-dir ./webp_images \
  --dry-run

# Full run with custom WebP base URL
bulk-webp-url-replacer \
  --content ./content \
  --raw-dir ./raw_images \
  --webp-dir ./webp_images \
  --webp-base-url "https://cdn.example.com/images"
```

### As Python Module

```bash
python -m bulk_webp_url_replacer \
  --content ./content \
  --raw-dir ./raw_images \
  --webp-dir ./webp_images \
  --webp-base-url "https://cdn.example.com/images"
```

### Options

| Option | Required | Description |
|--------|----------|-------------|
| `--content` | Yes | Directory containing markdown files |
| `--raw-dir` | Yes | Directory to save downloaded raw images |
| `--webp-dir` | Yes | Directory to save converted WebP images |
| `--webp-base-url` | No | Base URL prefix for WebP images in markdown |
| `--quality` | No | WebP quality 1-100 (default: 80) |
| `--width` | No | Max image width in pixels (default: 1200) |
| `--dry-run` | No | Preview without making changes |

## Supported Markdown Patterns

The tool detects image URLs in:

```markdown
# YAML frontmatter
---
image: "https://example.com/image.jpg"
---

# TOML frontmatter
+++
image = "https://example.com/image.jpg"
+++

# Gallery shortcodes
{{< gallery >}}
- https://example.com/photo1.jpg
- https://example.com/photo2.png
{{< /gallery >}}

# Standard markdown
![Alt text](https://example.com/image.jpg)
```

## Output

After running, you'll have:

1. **WebP images** in your `--webp-dir`
2. **mapping.json** tracking original → WebP conversions
3. **Updated markdown files** with new URLs

## License

MIT
