# bulk-webp-url-replacer

[![PyPI version](https://badge.fury.io/py/bulk-webp-url-replacer.svg)](https://badge.fury.io/py/bulk-webp-url-replacer)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Bulk convert images to WebP and automatically update URLs in markdown files with a custom CDN prefix.

## Features

- 🔍 **Extract** image URLs from markdown files (frontmatter, galleries, inline images)
- 📥 **Download** images from remote URLs (parallel downloads)
- 🖼️ **Convert** to optimized WebP format
- 🔄 **Replace** original URLs with new CDN-prefixed paths
- ⏭️ **Skip** already-processed images and excluded extensions
- 👀 **Dry-run** mode to preview changes

## Installation

```bash
pip install bulk-webp-url-replacer
```

Or install from source:

```bash
git clone https://github.com/HoangYell/bulk-webp-url-replacer.git
cd bulk-webp-url-replacer
pip install -e .
```

## Usage

### CLI

```bash
# Dry run - preview what would be processed
bulk-webp-url-replacer \
  --scan-dir ./content \
  --output-dir ./webp_images \
  --dry-run

# Full run with custom URL prefix
bulk-webp-url-replacer \
  --scan-dir ./content \
  --output-dir ./webp_images \
  --new-url-prefix "https://cdn.example.com/images"

# Faster with more threads
bulk-webp-url-replacer \
  --scan-dir ./content \
  --output-dir ./webp_images \
  --new-url-prefix "https://cdn.example.com/images" \
  --threads 8
```

### As Python Module

```bash
python -m bulk_webp_url_replacer \
  --scan-dir ./content \
  --output-dir ./webp_images \
  --new-url-prefix "https://cdn.example.com/images"
```

### Programmatic Usage

```python
from bulk_webp_url_replacer import ImageETL, ImageURLExtractor

# Full ETL pipeline
etl = ImageETL(
    content_dir="./content",
    webp_dir="./webp_images",
    webp_base_url="https://cdn.example.com/images",
    quality=80,
    max_width=1200,
    exclude_extensions=["gif", "svg", "webp", "ico"],
    threads=4
)

# Dry run to preview changes
result = etl.run(dry_run=True)
print(f"Found {result.total_urls} URLs, {result.skipped} already processed")

# Full run
result = etl.run(dry_run=False)
print(f"Converted {result.converted} images, {result.failed} failed")

# Or just extract URLs without processing
extractor = ImageURLExtractor()
urls = extractor.extract_from_directory("./content")
for file_path, line_num, url in urls:
    print(f"{file_path}:{line_num} -> {url}")
```

## Automation

You can use the provided `bash.sh` script to automate the entire process using [uv](https://docs.astral.sh/uv/):

```bash
#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# ETL: Find image URLs → Download → Convert to WebP
#
# Scans markdown posts for image URLs, downloads them, 
# converts to WebP, and saves output to the specified directory.
#
# Uses UV for virtual environment management.
# ──────────────────────────────────────────────────────────────
set -euo pipefail

# ── Paths ─────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAN_DIR="${SCAN_DIR:-/path/to/your/markdown/content}"
OUTPUT_DIR="${OUTPUT_DIR:-/path/to/output/webp}"
VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/.venv}"
NEW_URL_PREFIX="${NEW_URL_PREFIX:-https://your-cdn.com/webp}"

# ── ETL Options (override via env vars) ───────────────────────
QUALITY="${QUALITY:-80}"
MAX_WIDTH="${MAX_WIDTH:-1200}"
THREADS="${THREADS:-4}"
DRY_RUN="${DRY_RUN:-false}"

# ── Colors ────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No color

info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
ok()    { echo -e "${GREEN}[ OK ]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; }

# ── Pre-flight checks ────────────────────────────────────────
if ! command -v uv &>/dev/null; then
    fail "uv is not installed. Install it from https://docs.astral.sh/uv/"
    exit 1
fi

if [ ! -d "$SCAN_DIR" ]; then
    fail "Scan directory not found: $SCAN_DIR"
    exit 1
fi

# ── Virtual environment setup ─────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment at $VENV_DIR"
    uv venv "$VENV_DIR"
fi

info "Activating virtual environment"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

info "Installing bulk-webp-url-replacer (editable mode)"
uv pip install -e "$SCRIPT_DIR"

# ── Ensure output directory exists ────────────────────────────
mkdir -p "$OUTPUT_DIR"

# ── Run ETL ───────────────────────────────────────────────────
echo ""
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "  Bulk WebP URL Replacer – ETL"
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "  Scan dir  : $SCAN_DIR"
info "  Output dir: $OUTPUT_DIR"
info "  Quality   : $QUALITY"
info "  Max width : $MAX_WIDTH"
info "  Threads   : $THREADS"
info "  URL Prefix: $NEW_URL_PREFIX"
info "  Dry run   : $DRY_RUN"
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

CMD=(
    bulk-webp-url-replacer
    --scan-dir "$SCAN_DIR"
    --output-dir "$OUTPUT_DIR"
    --quality "$QUALITY"
    --max-width "$MAX_WIDTH"
    --threads "$THREADS"
    --new-url-prefix "$NEW_URL_PREFIX"
)

if [ "$DRY_RUN" = "true" ]; then
    warn "Running in DRY-RUN mode (no files will be modified)"
    CMD+=(--dry-run)
fi

"${CMD[@]}"

echo ""
ok "ETL complete! WebP images saved to: $OUTPUT_DIR"
```

### Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `--scan-dir` | Yes | - | Directory to scan for files containing image URLs |
| `--output-dir` | Yes | - | Directory to save converted WebP images |
| `--new-url-prefix` | No | - | URL prefix to replace old image URLs |
| `--quality` | No | 80 | WebP quality 1-100 |
| `--max-width` | No | 1200 | Max image width in pixels |
| `--exclude-ext` | No | gif svg webp ico | File extensions to skip |
| `--threads` | No | 4 | Number of parallel download threads |
| `--dry-run` | No | - | Preview changes without downloading or modifying files |

## Supported Patterns

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

# HTML img tags in shortcodes
{{< embed >}}
<img src="https://example.com/image.jpg" width="250" height="250"/>
{{< /embed >}}

# Standard markdown
![Alt text](https://example.com/image.jpg)
```

## Output

After running, you'll have:

1. **WebP images** in your `--output-dir`
2. **mapping.json** tracking original → WebP conversions
3. **Updated files** with new URLs

## License

MIT
