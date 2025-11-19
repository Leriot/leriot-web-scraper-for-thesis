#!/usr/bin/env python3
"""
PDF OCR Processor - Data Cleanup Tool for Scanned PDFs

Purpose:
    Processes quarantined PDFs (from process_pdfs.py) that contain scanned images
    rather than text. Uses Tesseract OCR to extract text from image-based PDFs.

Prerequisites:
    IMPORTANT: Tesseract must be installed on your system before running this script.

    Installation instructions:
    - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
               After installation, add Tesseract to your PATH or update TESSERACT_PATH below
    - macOS: brew install tesseract tesseract-lang
    - Linux: sudo apt-get install tesseract-ocr tesseract-ocr-ces

    For Czech language support, also install:
    - Windows: Select Czech language pack during installation
    - macOS: Already included with tesseract-lang
    - Linux: tesseract-ocr-ces package

What it does:
    1. Scans 'needs_ocr' folders for quarantined PDFs
    2. Converts each PDF page to images
    3. Runs Tesseract OCR on each page (supports English + Czech)
    4. Combines text from all pages
    5. Saves extracted text in same format as process_pdfs.py
    6. Moves processed PDFs to 'ocr_processed' folder

Usage:
    # Process all quarantined PDFs for an organization
    python scripts/ocr_pdfs.py --org "Hnutí DUHA"

    # Process specific scrape session
    python scripts/ocr_pdfs.py --org "Hnutí DUHA" --session "20240115_103000"

    # Process all organizations
    python scripts/ocr_pdfs.py --all

    # Use custom Tesseract path (Windows)
    python scripts/ocr_pdfs.py --org "Arnika" --tesseract-path "C:/Program Files/Tesseract-OCR/tesseract.exe"

    # English only (faster, but may miss Czech text)
    python scripts/ocr_pdfs.py --org "Arnika" --lang eng

Author: Thesis Research - NGO Network Analysis
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Check for required dependencies
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
except ImportError as e:
    print("=" * 70)
    print("ERROR: Missing required Python packages")
    print("=" * 70)
    print(f"\nMissing package: {e.name}")
    print("\nPlease install required packages:")
    print("  pip install pytesseract pdf2image Pillow")
    print("\nIMPORTANT: You also need to install Tesseract on your system:")
    print("  - Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    print("  - macOS: brew install tesseract tesseract-lang")
    print("  - Linux: sudo apt-get install tesseract-ocr tesseract-ocr-ces")
    print("=" * 70)
    sys.exit(1)

# Platform-specific Tesseract configuration
TESSERACT_PATH = None  # Set to None for auto-detection, or specify path on Windows


class OCRProcessor:
    """Processes quarantined PDFs using Tesseract OCR."""

    def __init__(self, data_root="data", tesseract_path=None, language="eng+ces"):
        self.data_root = Path(data_root)
        self.language = language

        # Configure Tesseract path if specified
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        self.stats = {
            'processed': 0,
            'success': 0,
            'errors': 0,
            'total_pages': 0
        }

    def check_tesseract(self):
        """
        Verify that Tesseract is installed and accessible.

        Returns:
            bool: True if Tesseract is available, False otherwise
        """
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract found: version {version}")

            # Check available languages
            langs = pytesseract.get_languages()
            print(f"✓ Available languages: {', '.join(langs)}")

            # Check if requested languages are available
            requested_langs = self.language.split('+')
            missing_langs = [lang for lang in requested_langs if lang not in langs]

            if missing_langs:
                print(f"\n⚠ WARNING: Missing language packs: {', '.join(missing_langs)}")
                print(f"  OCR will only use available languages: {', '.join([l for l in requested_langs if l in langs])}")
                # Update language to only use available ones
                self.language = '+'.join([l for l in requested_langs if l in langs])
                if not self.language:
                    print("\n✗ ERROR: No compatible language packs found!")
                    return False

            return True

        except Exception as e:
            print("=" * 70)
            print("ERROR: Tesseract is not installed or not accessible")
            print("=" * 70)
            print(f"\nError: {e}")
            print("\nPlease install Tesseract:")
            print("  - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
            print("            After installation, add to PATH or specify --tesseract-path")
            print("  - macOS: brew install tesseract tesseract-lang")
            print("  - Linux: sudo apt-get install tesseract-ocr tesseract-ocr-ces")
            print("=" * 70)
            return False

    def find_organizations(self):
        """Find all organizations with processed data."""
        processed_path = self.data_root / "processed"
        if not processed_path.exists():
            return []
        return [d.name for d in processed_path.iterdir() if d.is_dir()]

    def find_sessions(self, org_name):
        """Find all sessions for an organization that have needs_ocr folders."""
        org_path = self.data_root / "processed" / org_name
        if not org_path.exists():
            return []

        sessions = []
        for session_dir in org_path.iterdir():
            if session_dir.is_dir():
                ocr_dir = session_dir / "needs_ocr"
                if ocr_dir.exists() and any(ocr_dir.glob("*.pdf")):
                    sessions.append(session_dir.name)

        return sessions

    def extract_text_from_pdf_ocr(self, pdf_path: Path) -> Optional[str]:
        """
        Extract text from a PDF using OCR.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text or None if extraction failed
        """
        try:
            print(f"  Converting PDF to images...", end=" ", flush=True)

            # Convert PDF to images (one per page)
            images = convert_from_path(pdf_path, dpi=300)
            print(f"{len(images)} pages")

            self.stats['total_pages'] += len(images)

            # OCR each page
            all_text = []
            for i, image in enumerate(images, 1):
                print(f"  OCR page {i}/{len(images)}...", end=" ", flush=True)

                # Run Tesseract OCR
                text = pytesseract.image_to_string(image, lang=self.language)

                if text.strip():
                    all_text.append(f"--- Page {i} ---\n{text}")
                    print(f"{len(text)} chars")
                else:
                    print("no text")

            # Combine all pages
            combined_text = "\n\n".join(all_text)

            if not combined_text.strip():
                return None

            return combined_text

        except Exception as e:
            print(f"\n  ✗ Error: {e}")
            return None

    def process_pdf(self, pdf_path: Path, output_dir: Path, processed_dir: Path) -> str:
        """
        Process a single PDF with OCR.

        Args:
            pdf_path: Path to the quarantined PDF
            output_dir: Directory to save extracted text
            processed_dir: Directory to move processed PDFs

        Returns:
            'success', 'error', or 'empty'
        """
        filename = pdf_path.name
        print(f"\n📄 Processing: {filename}")

        # Extract text using OCR
        text = self.extract_text_from_pdf_ocr(pdf_path)

        if not text or len(text.strip()) < 50:
            print(f"  ⚠ Extracted text too short ({len(text.strip()) if text else 0} chars)")
            return 'empty'

        # Prepare output
        output_filename = pdf_path.stem + ".txt"
        output_path = output_dir / output_filename

        # Create metadata header (same format as process_pdfs.py)
        metadata = f"""SOURCE_FILE: {filename}
OCR_EXTRACTED: {datetime.now().isoformat()}
TEXT_LENGTH: {len(text)} characters
OCR_LANGUAGE: {self.language}

"""

        final_output = metadata + text

        # Save extracted text
        output_path.write_text(final_output, encoding='utf-8')

        # Move PDF to processed folder
        processed_path = processed_dir / filename
        shutil.move(str(pdf_path), str(processed_path))

        print(f"  ✓ Extracted {len(text)} characters → {output_filename}")

        return 'success'

    def process_session(self, org_name: str, session_name: str):
        """Process all quarantined PDFs for a specific session."""
        session_path = self.data_root / "processed" / org_name / session_name
        needs_ocr_dir = session_path / "needs_ocr"

        if not needs_ocr_dir.exists():
            print(f"  ℹ No 'needs_ocr' folder found for session {session_name}")
            return

        # Get all PDFs
        pdf_files = list(needs_ocr_dir.glob("*.pdf"))

        if not pdf_files:
            print(f"  ℹ No PDFs found in needs_ocr folder")
            return

        # Create output directories
        extracted_text_dir = session_path / "extracted_text"
        extracted_text_dir.mkdir(exist_ok=True)

        ocr_processed_dir = session_path / "ocr_processed"
        ocr_processed_dir.mkdir(exist_ok=True)

        print(f"\n{'='*70}")
        print(f"Session: {org_name} / {session_name}")
        print(f"PDFs to process: {len(pdf_files)}")
        print(f"{'='*70}")

        # Process each PDF
        for pdf_path in pdf_files:
            self.stats['processed'] += 1

            try:
                result = self.process_pdf(pdf_path, extracted_text_dir, ocr_processed_dir)

                if result == 'success':
                    self.stats['success'] += 1
                elif result == 'error':
                    self.stats['errors'] += 1

            except Exception as e:
                print(f"  ✗ Unexpected error: {e}")
                self.stats['errors'] += 1

    def process_organization(self, org_name: str, session_name: Optional[str] = None):
        """Process all sessions for an organization."""
        if session_name:
            sessions = [session_name]
        else:
            sessions = self.find_sessions(org_name)

        if not sessions:
            print(f"ℹ No sessions with quarantined PDFs found for {org_name}")
            return

        print(f"\n🔍 Organization: {org_name}")
        print(f"   Sessions with quarantined PDFs: {len(sessions)}")

        for session in sessions:
            self.process_session(org_name, session)

    def print_summary(self):
        """Print processing summary."""
        print("\n" + "=" * 70)
        print("OCR PROCESSING SUMMARY")
        print("=" * 70)
        print(f"PDFs processed:        {self.stats['processed']}")
        print(f"  Successful:          {self.stats['success']}")
        print(f"  Errors/Empty:        {self.stats['errors']}")
        print(f"Total pages OCR'd:     {self.stats['total_pages']}")
        print("=" * 70)

        if self.stats['success'] > 0:
            avg_pages = self.stats['total_pages'] / self.stats['success']
            print(f"\nAverage pages per PDF: {avg_pages:.1f}")

        if self.stats['processed'] > 0:
            success_rate = (self.stats['success'] / self.stats['processed']) * 100
            print(f"Success rate:          {success_rate:.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from quarantined PDFs using OCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all quarantined PDFs for an organization
  python scripts/ocr_pdfs.py --org "Hnutí DUHA"

  # Process specific session
  python scripts/ocr_pdfs.py --org "Hnutí DUHA" --session "20240115_103000"

  # Process all organizations
  python scripts/ocr_pdfs.py --all

  # Windows with custom Tesseract path
  python scripts/ocr_pdfs.py --org "Arnika" --tesseract-path "C:/Program Files/Tesseract-OCR/tesseract.exe"

IMPORTANT: Tesseract must be installed on your system before running this script.
See script header for installation instructions.
        """
    )

    parser.add_argument('--org', type=str, help='Organization name to process')
    parser.add_argument('--session', type=str, help='Specific session to process')
    parser.add_argument('--all', action='store_true', help='Process all organizations')
    parser.add_argument('--data-root', type=str, default='data', help='Root data directory (default: data)')
    parser.add_argument('--tesseract-path', type=str, help='Path to Tesseract executable (auto-detected if not specified)')
    parser.add_argument('--lang', type=str, default='eng+ces', help='OCR language(s) (default: eng+ces for English and Czech)')

    args = parser.parse_args()

    # Validate arguments
    if not args.all and not args.org:
        parser.error("Must specify either --org or --all")

    if args.session and not args.org:
        parser.error("--session requires --org")

    # Initialize processor
    processor = OCRProcessor(
        data_root=args.data_root,
        tesseract_path=args.tesseract_path,
        language=args.lang
    )

    # Check Tesseract installation
    print("=" * 70)
    print("PDF OCR PROCESSOR")
    print("=" * 70)
    print("\nChecking Tesseract installation...")

    if not processor.check_tesseract():
        sys.exit(1)

    print("\n✓ All prerequisites met. Starting OCR processing...\n")

    # Process organizations
    if args.all:
        orgs = processor.find_organizations()

        if not orgs:
            print("✗ No organizations found in data/processed/")
            return

        print(f"Found {len(orgs)} organizations to process\n")

        for org in orgs:
            processor.process_organization(org)

    else:
        processor.process_organization(args.org, args.session)

    # Print summary
    processor.print_summary()

    if processor.stats['processed'] == 0:
        print("\nℹ No PDFs were found to process.")
        print("  Make sure you've run process_pdfs.py first to quarantine scanned PDFs.")


if __name__ == '__main__':
    main()
