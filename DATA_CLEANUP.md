# Data Cleanup Tools

This repository includes Python scripts for processing and filtering scraped data. These tools help prepare raw scraped content for LLM-based network analysis.

## Overview

```
Raw Data → Script 1: PDF Extraction → Script 1.5: OCR Processing → Script 2: Content Filtering → Clean Data for Analysis
                            ↓
                    Quarantine (needs_ocr/)
```

1. **`process_pdfs.py`** - Extracts text from PDFs, quarantines image-based scans
2. **`ocr_pdfs.py`** - OCR processing for quarantined scanned PDFs (requires Tesseract)
3. **`filter_content.py`** - Cleans HTML, deduplicates, filters for relevance

---

## Script 1: `process_pdfs.py` - PDF Text Extraction

### Purpose
Extracts readable text from scraped PDFs and identifies scanned documents that require OCR processing.

### What It Does

#### 1. Text Extraction
- Uses `pdfplumber` library with layout preservation (maintains table structures)
- Extracts text from all pages in each PDF

#### 2. Cleaning Operations
- **Header/Footer Removal**: Detects lines appearing on >50% of pages (e.g., "Page 5 of 20") and removes them
- **Whitespace Collapse**: Reduces 3+ consecutive newlines to 2 (preserves paragraph breaks)

#### 3. Quality Check
- Counts total characters in extracted text
- If text length < 100 characters → likely a scanned image/photo-based PDF
- These are moved to a "quarantine" folder for later OCR processing

#### 4. Output
- **Successful extractions** → saved as `.txt` files in `data/processed/{org}/{session}/extracted_text/`
- **Failed extractions** → original PDFs copied to `data/processed/{org}/{session}/needs_ocr/`

### Usage

```bash
# List available organizations and sessions
python scripts/process_pdfs.py --list

# Process all PDFs for one organization (all sessions)
python scripts/process_pdfs.py --org "Hnutí DUHA"

# Process specific scrape session
python scripts/process_pdfs.py --org "Hnutí DUHA" --session "20240115_103000"

# Process all organizations
python scripts/process_pdfs.py --all

# Custom threshold (require 200 chars minimum before quarantine)
python scripts/process_pdfs.py --org "Arnika" --min-chars 200
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--org` | Organization name to process | Required (unless --all) |
| `--session` | Specific session timestamp | All sessions |
| `--all` | Process all organizations | False |
| `--min-chars` | Minimum characters to avoid quarantine | 100 |
| `--data-root` | Root data directory | `data` |
| `--list` | List available orgs/sessions | - |

### Output Structure

```
data/processed/{org}/{session}/
├── extracted_text/          # Successfully extracted PDFs
│   ├── document1.txt
│   ├── document2.txt
│   └── ...
└── needs_ocr/               # Scanned PDFs requiring OCR
    ├── scan1.pdf
    └── scan2.pdf
```

Each `.txt` file includes metadata header:
```
SOURCE_FILE: report_2023.pdf
EXTRACTED: 2024-01-15T10:30:00
TEXT_LENGTH: 4521 characters

[actual text content here...]
```

### Known Limitations

1. **Header detection**: Only checks first line of each page (won't catch multi-line headers)
2. **Footer detection**: Not specifically handled (only headers are detected)
3. **Scanned PDFs**: Only identified and quarantined; use `ocr_pdfs.py` to process them (see Script 1.5 below)

### Dependencies

```bash
pip install pdfplumber
```

---

## Script 1.5: `ocr_pdfs.py` - OCR Processing for Scanned PDFs

### Purpose
Processes quarantined PDFs (from `process_pdfs.py`) that contain scanned images rather than extractable text. Uses Tesseract OCR to extract text from image-based PDFs.

### Prerequisites

**IMPORTANT: Tesseract must be installed on your system before running this script.**

#### Tesseract Installation

**Windows:**
1. Download installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run installer and select **Czech language pack** during installation
3. Add Tesseract to your PATH, or note the installation path (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`)

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-ces poppler-utils
```

#### Verify Installation

```bash
tesseract --version
tesseract --list-langs  # Should show 'eng' and 'ces' (Czech)
```

### What It Does

#### 1. PDF to Image Conversion
- Converts each PDF page to high-resolution images (300 DPI)
- Uses `pdf2image` library (requires poppler)

#### 2. OCR Processing
- Runs Tesseract OCR on each page image
- Supports multiple languages simultaneously (default: English + Czech)
- Combines text from all pages with page markers

#### 3. Text Extraction
- Saves extracted text in same format as `process_pdfs.py`
- Includes metadata: source file, timestamp, language, character count

#### 4. File Management
- Successfully processed PDFs → moved to `ocr_processed/` folder
- Extracted text → saved to `extracted_text/` (same as regular PDFs)

### Usage

```bash
# Process all quarantined PDFs for one organization
python scripts/ocr_pdfs.py --org "Hnutí DUHA"

# Process specific scrape session
python scripts/ocr_pdfs.py --org "Hnutí DUHA" --session "20240115_103000"

# Process all organizations
python scripts/ocr_pdfs.py --all

# English only (faster, but may miss Czech text)
python scripts/ocr_pdfs.py --org "Arnika" --lang eng

# Windows with custom Tesseract path
python scripts/ocr_pdfs.py --org "Arnika" --tesseract-path "C:/Program Files/Tesseract-OCR/tesseract.exe"
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--org` | Organization name to process | Required (unless --all) |
| `--session` | Specific session timestamp | All sessions |
| `--all` | Process all organizations | False |
| `--lang` | OCR language(s) (e.g., eng, ces, eng+ces) | `eng+ces` |
| `--tesseract-path` | Path to Tesseract executable | Auto-detected |
| `--data-root` | Root data directory | `data` |

### Input/Output Structure

**Input:** PDFs from the quarantine folder
```
data/processed/{org}/{session}/
└── needs_ocr/               # Quarantined PDFs from process_pdfs.py
    ├── scan1.pdf
    └── scan2.pdf
```

**Output:** Extracted text and processed PDFs
```
data/processed/{org}/{session}/
├── extracted_text/          # OCR'd text files (merged with regular extractions)
│   ├── scan1.txt
│   └── scan2.txt
└── ocr_processed/           # Successfully processed PDFs (moved from needs_ocr/)
    ├── scan1.pdf
    └── scan2.pdf
```

### Output Format

Each `.txt` file includes metadata header:
```
SOURCE_FILE: scan_report_2023.pdf
OCR_EXTRACTED: 2024-01-15T14:30:00
TEXT_LENGTH: 3421 characters
OCR_LANGUAGE: eng+ces

--- Page 1 ---
[OCR extracted text from page 1...]

--- Page 2 ---
[OCR extracted text from page 2...]
```

### Performance Notes

- **Speed**: ~30-60 seconds per page depending on content complexity and system speed
- **Accuracy**:
  - Clean scanned text: 95-99% accuracy
  - Low-quality scans: 70-90% accuracy
  - Handwritten text: Poor accuracy (not recommended)
- **Language support**: Works best with English and Czech; other languages require additional language packs

### Troubleshooting

**Error: "Tesseract is not installed or not accessible"**
- Verify Tesseract is installed: `tesseract --version`
- Windows: Add Tesseract to PATH or use `--tesseract-path`
- Mac/Linux: Reinstall with package manager

**Error: "Missing language packs"**
- Check available languages: `tesseract --list-langs`
- Install missing languages:
  - Windows: Re-run installer and select languages
  - Mac: `brew install tesseract-lang`
  - Linux: `sudo apt-get install tesseract-ocr-ces` (for Czech)

**Poor OCR quality:**
- Check source PDF quality (blurry scans won't OCR well)
- Try single-language mode if bilingual detection fails: `--lang eng` or `--lang ces`
- Consider manual review for critical documents

### Dependencies

```bash
pip install pytesseract pdf2image Pillow
```

**System dependencies:**
- Tesseract OCR (see installation instructions above)
- Poppler (for PDF to image conversion):
  - Windows: Included in pdf2image or install separately
  - Mac: `brew install poppler`
  - Linux: `sudo apt-get install poppler-utils`

### Integration with Main UI

The OCR processor is integrated into the scraper menu (`scripts/scraper_menu.py`):
- **Option [13]**: Process PDFs (Extract Text) - runs `process_pdfs.py`
- **Option [14]**: OCR Quarantined PDFs - runs `ocr_pdfs.py`

The menu will remind you to install Tesseract before running OCR.

---

## Script 2: `filter_content.py` - Content Cleaning & Filtering

### Purpose
Cleans HTML content, removes boilerplate and duplicates, and filters documents for relevance to NGO network analysis using Czech social science keywords.

### What It Does

#### 1. HTML Cleaning (Boilerplate Removal)

Removes non-content elements:
- **Tag removal**: `<script>`, `<style>`, `<noscript>`, `<iframe>`, `<svg>`, `<form>`, `<button>`, `<input>`
- **Class/ID heuristics**: Elements with classes/IDs like `nav`, `footer`, `sidebar`, `menu`, `cookie`, `ads`
- **Role attributes**: Elements with `role="navigation"`, `role="banner"`, etc.
- **Link density**: Blocks where >60% of text is links (indicates navigation menus)

Protects content elements with safe terms: `article`, `content`, `main`, `body`

#### 2. Deduplication

Uses **shingling** + **Jaccard similarity**:
- Creates 3-word sequences (shingles) from each document
- Compares documents using Jaccard index: `intersection / union`
- If similarity ≥ 0.85 (85%) → marked as duplicate
- Duplicates are grouped by the first (master) occurrence

**Example:**
```
Doc A: "the cat sat on the mat" → shingles: {(the,cat,sat), (cat,sat,on), (sat,on,the), ...}
Doc B: "the cat sat on the rug" → shingles: {(the,cat,sat), (cat,sat,on), (sat,on,the), ...}
Jaccard = 0.8 → Not duplicate (< 0.85)
```

#### 3. Relevance Scoring

Uses **Czech keywords** with weights based on social science theory:

| Category | Keywords (roots) | Weight | Rationale |
|----------|------------------|--------|-----------|
| **Relations** | spoluprác, partner, alianc, koalic | 3 | Core network ties |
| | člen, platform, síť | 2 | Membership/structure |
| **Funding** | grant, financ, dar, nadac, fond, dotac | 2-3 | Resource dependency |
| **Policy Actors** | ministerstv | 3 | High-level influence |
| | parlament, senát | 2 | Legislative ties |
| | vlád, výbor, zákon | 1 | Common terms (low weight) |
| **Actions** | podpor, organiz, projekt | 1 | Context indicators |
| **Topics** | klimat, uhlí, strategi | 1 | Domain context |

**How scoring works:**
1. Search for keyword roots (e.g., "spoluprác" matches "spolupráce", "spolupracovat", "spolupracující")
2. Count occurrences: `spolupráce(5×)` = 5 occurrences
3. Calculate score: `5 × weight(3) = 15 points`
4. Sum all keyword scores → **Raw Score**

#### 4. Density Filtering (Length Penalty)

To prevent long documents with few keywords from passing:

- **Density Score** = `(Raw Score / Word Count) × 100`
- Example: 10 points in 1000 words = 1.0 density

**Why this matters:**
- Document A: 500 words, 10 points → Density = 2.0 ✓
- Document B: 5000 words, 10 points → Density = 0.2 ✗

Document B is probably a general news article with incidental keyword mentions.

#### 5. Decision Logic

A document is **RELEVANT** if it passes BOTH filters:
```
KEEP if: (Raw Score ≥ 5) AND (Density ≥ 0.5)
```

Default thresholds:
- **Minimum Raw Score**: 5 points
- **Minimum Density**: 0.5 points per 100 words

#### 6. Output

Documents are sorted into three folders:

```
data/processed/{org}/{session}/
├── relevant/           # Passes both filters
│   ├── page1.txt
│   └── page2.txt
├── irrelevant/         # Fails one or both filters
│   ├── page3.txt
│   └── page4.txt
└── duplicates/         # Grouped by master document
    ├── page1/          # Master: page1.html
    │   ├── page5.txt   # Duplicate of page1
    │   └── page6.txt
    └── page2/
        └── page7.txt
```

Each file includes metadata header:
```
SOURCE_FILE: page1.html
PROCESSED: 2024-01-15T10:30:00
RELEVANCE_RAW_SCORE: 15
RELEVANCE_DENSITY: 2.34
WORD_COUNT: 641
KEYWORDS_FOUND: spoluprác(3×w3), partner(2×w3), ministerstv(1×w3)

================================================================================

[actual cleaned text here...]
```

### Usage

```bash
# List available organizations and sessions
python scripts/filter_content.py --list

# Process all HTML files for one organization (all sessions)
python scripts/filter_content.py --org "Hnutí DUHA"

# Process specific scrape session
python scripts/filter_content.py --org "Hnutí DUHA" --session "20240115_103000"

# Process all organizations
python scripts/filter_content.py --all

# Stricter filtering (more selective)
python scripts/filter_content.py --org "Arnika" --min-score 10 --min-density 1.0

# More lenient filtering (keep more documents)
python scripts/filter_content.py --org "Greenpeace ČR" --min-score 3 --min-density 0.3

# Adjust deduplication sensitivity
python scripts/filter_content.py --org "Arnika" --similarity 0.90  # More strict (fewer dupes)
python scripts/filter_content.py --org "Arnika" --similarity 0.75  # More lenient (more dupes)
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--org` | Organization name to process | Required (unless --all) |
| `--session` | Specific session timestamp | All sessions |
| `--all` | Process all organizations | False |
| `--min-score` | Minimum raw relevance score | 5 |
| `--min-density` | Minimum density per 100 words | 0.5 |
| `--similarity` | Jaccard threshold for duplicates | 0.85 |
| `--data-root` | Root data directory | `data` |
| `--list` | List available orgs/sessions | - |

### Tuning Recommendations

#### If keeping too many irrelevant documents:
```bash
# Increase thresholds
python scripts/filter_content.py --org "..." --min-score 8 --min-density 1.0
```

#### If losing too many relevant documents:
```bash
# Decrease thresholds
python scripts/filter_content.py --org "..." --min-score 3 --min-density 0.3
```

#### If too many duplicates are kept:
```bash
# Lower similarity threshold (more aggressive deduplication)
python scripts/filter_content.py --org "..." --similarity 0.75
```

#### If too many unique documents marked as duplicates:
```bash
# Raise similarity threshold (less aggressive)
python scripts/filter_content.py --org "..." --similarity 0.90
```

### Customizing Keywords

**Keywords are now configurable!** Edit `config/content_filter_keywords.yaml` to customize filtering:

```yaml
keywords:
  relations:
    - root: "spoluprác"
      weight: 3
      variations: ["spolupráce", "spolupracovat", "spolupracující", "spolupracoval"]
      description: "Cooperation, collaboration"

    - root: "partner"
      weight: 3
      variations: ["partner", "partneři", "partnerství", "partnerský", "partnera"]
      description: "Partners, partnerships"

  funding:
    - root: "grant"
      weight: 3
      variations: ["grant", "grantu", "grantů", "grantový"]
      description: "Grant"
```

**How keyword matching works (improved in v2):**

1. **Root matching**: Searches for the keyword root (e.g., "spoluprác")
2. **Variation matching**: Uses regex with word boundaries to match exact variations (e.g., `\bspolupráce\b`)
3. **Takes maximum**: Uses max(root_count, variation_count) to avoid double-counting
4. **Scores**: `count × weight`

**Example:**
```
Text: "Naše spolupráce s partnery zahrnuje 5 partnerů."

spoluprác: root_count=1, variations=['spolupráce']=1 → count=1, score=1×3=3
partner:   root_count=2, variations=['partnery','partnerů']=2 → count=2, score=2×3=6

Total Raw Score: 9
Word Count: 7
Density: (9/7)×100 = 128.57 points per 100 words → PASS ✓
```

**Adding new keywords:**

```yaml
- root: "kooperac"
  weight: 3
  variations: ["kooperace", "kooperační", "kooperovat"]
  description: "Cooperation (alternative term)"
```

**Adjusting weights:**
- Weight 1: Common terms (context indicators)
- Weight 2: Medium importance (structural terms)
- Weight 3: High importance (core network concepts)

**Adjusting default thresholds:**

```yaml
filtering:
  min_raw_score: 5       # Change to 3 for more lenient, 10 for stricter
  min_density_score: 0.5 # Change to 0.3 for more lenient, 1.0 for stricter
  similarity_threshold: 0.85
```

**Using custom config:**

```bash
# Create custom config
cp config/content_filter_keywords.yaml config/my_keywords.yaml

# Edit your keywords
nano config/my_keywords.yaml

# Use custom config
python scripts/filter_content.py --org "..." --config config/my_keywords.yaml
```

### Dependencies

```bash
pip install beautifulsoup4 pyyaml
```

---

## Installation

Both scripts require additional dependencies:

```bash
pip install pdfplumber beautifulsoup4 pyyaml
```

Note: `beautifulsoup4` and `pyyaml` are already in requirements.txt. Only `pdfplumber` needs to be added:

```bash
# Or install from requirements.txt
pip install -r requirements.txt
```

---

## Workflow Example

Complete data cleanup pipeline:

```bash
# 1. List available data
python scripts/process_pdfs.py --list
python scripts/filter_content.py --list

# 2. Process PDFs for specific organization
python scripts/process_pdfs.py --org "Hnutí DUHA"

# 3. Filter HTML content for same organization
python scripts/filter_content.py --org "Hnutí DUHA"

# 4. Review results
ls -lh data/processed/Hnutí\ DUHA/*/extracted_text/
ls -lh data/processed/Hnutí\ DUHA/*/relevant/

# 5. Process everything
python scripts/process_pdfs.py --all
python scripts/filter_content.py --all
```

---

## Output for Analysis

After running both scripts, your analysis-ready data will be in:

```
data/processed/{org}/{session}/
├── extracted_text/     # Cleaned PDF text (from script 1)
├── relevant/           # Filtered HTML content (from script 2)
├── irrelevant/         # Filtered out content
├── duplicates/         # Duplicate pages
└── needs_ocr/          # Scanned PDFs requiring OCR
```

**For LLM network analysis**, focus on:
- `extracted_text/` - Reports, publications, policy documents
- `relevant/` - Web pages discussing partnerships, funding, policy actors

---

## Troubleshooting

### Script 1: PDF Processing

**Problem**: All PDFs going to quarantine
```bash
# Solution: Lower the character threshold
python scripts/process_pdfs.py --org "..." --min-chars 50
```

**Problem**: Error "pdfplumber not found"
```bash
pip install pdfplumber
```

**Problem**: Encoding errors in output
- Script uses UTF-8 with `errors='ignore'` - should handle Czech characters
- Check system locale: `locale` (should include UTF-8)

### Script 2: Content Filtering

**Problem**: No relevant documents found
```bash
# Solution: Lower filtering thresholds
python scripts/filter_content.py --org "..." --min-score 3 --min-density 0.25
```

**Problem**: Everything marked as irrelevant
- Check if Czech keywords are appropriate for your data
- Try `--min-score 1 --min-density 0.1` to see what passes
- Review keywords in script (lines 69-102)

**Problem**: Error "beautifulsoup4 not found"
```bash
pip install beautifulsoup4
```

**Problem**: Too many duplicates
- Websites often have template pages with similar content
- This is expected behavior - review `duplicates/` folder to verify
- Adjust with `--similarity 0.90` if needed

---

## Code Quality Notes

### Script 1 (`process_pdfs.py`)
✅ **Strengths**:
- Clean separation of concerns (extraction, cleaning, quality check)
- Good error handling with try-except blocks
- Preserves original PDFs in quarantine (doesn't delete)
- Metadata tracking in output

⚠️ **Limitations**:
- Header detection only checks first line (misses multi-line headers)
- No footer detection
- Doesn't attempt OCR (by design - requires external tool)

### Script 2 (`filter_content.py`)
✅ **Strengths**:
- Sophisticated deduplication using shingling
- Dual-criteria filtering (raw + density) prevents false positives
- Good balance of safe vs. junk element detection
- Link density check removes navigation blocks
- Extensive keyword dictionary with theory-based weights

⚠️ **Limitations**:
- No stemming (relies on root matching like "spoluprác" to catch variations)
- Keywords hardcoded (not in config file)
- Reprocesses all files each run (no incremental processing)

---

## Citation

If you use these scripts in your research, please cite:

```
Leriot. (2024). Data Cleanup Tools for NGO Network Analysis.
Web Scraper for Thesis Research, Masaryk University.
https://github.com/Leriot/leriot-web-scraper-for-thesis
```

---

## Contact

- Repository: https://github.com/Leriot/leriot-web-scraper-for-thesis
- Issues: Use GitHub Issues for bug reports or feature requests
