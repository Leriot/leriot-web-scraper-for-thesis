#!/usr/bin/env python3
"""
Actor Extraction Tool - Data Analysis Tool #3

Purpose:
    Extracts actors (Organizations and Persons) from Czech NGO texts using GLiNER
    (Generalist and Lightweight Model for Named Entity Recognition).

What it does:
    1. Uses GLiNER multilingual model for zero-shot entity extraction
    2. Extracts two entity types:
       - Organization: NGO names, government agencies, companies, coalitions
       - Person: People mentioned in the text (staff, partners, officials)
    3. Creates a database per organization with:
       - Extracted entities with context
       - Co-occurrence networks
       - Source document tracking
    4. Outputs structured data for network analysis

Usage:
    # Extract actors from a specific organization's processed data
    python scripts/extract_actors.py --org "Hnutí DUHA"

    # Extract from all organizations
    python scripts/extract_actors.py --all

    # Use specific GLiNER model
    python scripts/extract_actors.py --org "Arnika" --model "urchade/gliner_multi-v2.1"

    # Adjust confidence threshold
    python scripts/extract_actors.py --org "Arnika" --threshold 0.3

    # Process only relevant content (recommended)
    python scripts/extract_actors.py --org "Arnika" --relevant-only

Author: Thesis Research - NGO Network Analysis
Date: 2025-11-19
"""

import os
import sys
import json
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set
import re

try:
    from gliner import GLiNER
    from tqdm import tqdm
except ImportError as e:
    print(f"⚠ Error: Required package not installed: {e}")
    print("Please install GLiNER: pip install gliner")
    sys.exit(1)


# --- CONFIGURATION ---
DEFAULT_MODEL = "urchade/gliner_multi-v2.1"  # Multilingual model for Czech support
DEFAULT_THRESHOLD = 0.5  # Confidence threshold for entity extraction
DEFAULT_CONTEXT_WINDOW = 100  # Characters before/after entity for context

# Entity labels to extract (in English - GLiNER is multilingual)
ENTITY_LABELS = ["organization", "person"]


class ActorExtractor:
    """Extracts actors (organizations and persons) from Czech NGO texts using GLiNER."""

    def __init__(self, data_root="data", model_name=DEFAULT_MODEL,
                 threshold=DEFAULT_THRESHOLD, context_window=DEFAULT_CONTEXT_WINDOW):
        self.data_root = Path(data_root)
        self.model_name = model_name
        self.threshold = threshold
        self.context_window = context_window

        # Initialize GLiNER model
        print(f"📦 Loading GLiNER model: {model_name}")
        print("   (This may take a few minutes on first run...)")
        try:
            self.model = GLiNER.from_pretrained(model_name)
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise

        self.stats = {
            'files_processed': 0,
            'organizations_found': 0,
            'persons_found': 0,
            'total_entities': 0,
            'errors': 0
        }

    def find_organizations(self):
        """Find all organizations with processed data."""
        processed_path = self.data_root / "processed"
        if not processed_path.exists():
            return []
        return [d.name for d in processed_path.iterdir() if d.is_dir()]

    def find_sessions(self, org_name):
        """Find all processed sessions for an organization."""
        org_path = self.data_root / "processed" / org_name
        if not org_path.exists():
            return []
        return [d.name for d in org_path.iterdir() if d.is_dir()]

    def get_context(self, text: str, start: int, end: int) -> str:
        """Extract context around an entity."""
        context_start = max(0, start - self.context_window)
        context_end = min(len(text), end + self.context_window)

        context = text[context_start:context_end]

        # Add ellipsis if truncated
        if context_start > 0:
            context = "..." + context
        if context_end < len(text):
            context = context + "..."

        return context.strip()

    def extract_entities_from_text(self, text: str, source_file: str) -> List[Dict]:
        """
        Extract entities from text using GLiNER.

        Returns:
            List of entity dictionaries with text, label, score, context, source
        """
        try:
            # Extract entities using GLiNER
            entities = self.model.predict_entities(
                text,
                ENTITY_LABELS,
                threshold=self.threshold
            )

            # Enrich entities with context and source
            enriched_entities = []
            for entity in entities:
                enriched = {
                    'text': entity['text'],
                    'label': entity['label'],
                    'score': entity['score'],
                    'start': entity['start'],
                    'end': entity['end'],
                    'context': self.get_context(text, entity['start'], entity['end']),
                    'source_file': source_file,
                    'extracted_at': datetime.now().isoformat()
                }
                enriched_entities.append(enriched)

                # Update stats
                if entity['label'].lower() == 'organization':
                    self.stats['organizations_found'] += 1
                elif entity['label'].lower() == 'person':
                    self.stats['persons_found'] += 1
                self.stats['total_entities'] += 1

            return enriched_entities

        except Exception as e:
            print(f"  ✗ Error extracting entities: {e}")
            self.stats['errors'] += 1
            return []

    def normalize_entity_name(self, name: str) -> str:
        """Normalize entity name for deduplication."""
        # Remove extra whitespace
        name = ' '.join(name.split())
        # Remove common prefixes/suffixes
        name = re.sub(r'\s+(s\.r\.o\.|z\.s\.|o\.s\.|a\.s\.)$', '', name, flags=re.IGNORECASE)
        return name.strip()

    def create_database(self, org_name: str, session_name: str) -> sqlite3.Connection:
        """Create SQLite database for storing extracted actors."""
        db_dir = self.data_root / "actors" / org_name / session_name
        db_dir.mkdir(parents=True, exist_ok=True)

        db_path = db_dir / "actors.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create entities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                normalized_text TEXT NOT NULL,
                label TEXT NOT NULL,
                score REAL NOT NULL,
                context TEXT,
                source_file TEXT NOT NULL,
                extracted_at TEXT NOT NULL,
                start_pos INTEGER,
                end_pos INTEGER
            )
        """)

        # Create co-occurrences table (entities appearing in same document)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS co_occurrences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity1_id INTEGER NOT NULL,
                entity2_id INTEGER NOT NULL,
                source_file TEXT NOT NULL,
                co_occurrence_count INTEGER DEFAULT 1,
                FOREIGN KEY (entity1_id) REFERENCES entities(id),
                FOREIGN KEY (entity2_id) REFERENCES entities(id)
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_label ON entities(label)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_normalized ON entities(normalized_text)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_source ON entities(source_file)")

        conn.commit()
        return conn

    def save_entities_to_db(self, conn: sqlite3.Connection, entities: List[Dict]):
        """Save extracted entities to database."""
        cursor = conn.cursor()

        entity_ids = []
        for entity in entities:
            normalized = self.normalize_entity_name(entity['text'])

            cursor.execute("""
                INSERT INTO entities
                (text, normalized_text, label, score, context, source_file, extracted_at, start_pos, end_pos)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entity['text'],
                normalized,
                entity['label'],
                entity['score'],
                entity['context'],
                entity['source_file'],
                entity['extracted_at'],
                entity['start'],
                entity['end']
            ))

            entity_ids.append(cursor.lastrowid)

        # Create co-occurrence entries
        for i in range(len(entity_ids)):
            for j in range(i + 1, len(entity_ids)):
                cursor.execute("""
                    INSERT INTO co_occurrences (entity1_id, entity2_id, source_file)
                    VALUES (?, ?, ?)
                """, (entity_ids[i], entity_ids[j], entities[0]['source_file']))

        conn.commit()

    def export_to_json(self, conn: sqlite3.Connection, output_dir: Path):
        """Export database contents to JSON files for analysis."""
        cursor = conn.cursor()

        # Export all entities
        cursor.execute("""
            SELECT text, normalized_text, label, score, context, source_file, extracted_at
            FROM entities
            ORDER BY label, normalized_text
        """)

        entities = []
        for row in cursor.fetchall():
            entities.append({
                'text': row[0],
                'normalized_text': row[1],
                'label': row[2],
                'score': row[3],
                'context': row[4],
                'source_file': row[5],
                'extracted_at': row[6]
            })

        entities_file = output_dir / "entities.json"
        with open(entities_file, 'w', encoding='utf-8') as f:
            json.dump(entities, f, ensure_ascii=False, indent=2)

        # Export unique entities (deduplicated)
        cursor.execute("""
            SELECT normalized_text, label, COUNT(*) as count, AVG(score) as avg_score,
                   GROUP_CONCAT(DISTINCT source_file) as sources
            FROM entities
            GROUP BY normalized_text, label
            ORDER BY count DESC, avg_score DESC
        """)

        unique_entities = []
        for row in cursor.fetchall():
            unique_entities.append({
                'name': row[0],
                'type': row[1],
                'mention_count': row[2],
                'avg_confidence': row[3],
                'sources': row[4].split(',') if row[4] else []
            })

        unique_file = output_dir / "unique_entities.json"
        with open(unique_file, 'w', encoding='utf-8') as f:
            json.dump(unique_entities, f, ensure_ascii=False, indent=2)

        # Export co-occurrences network
        cursor.execute("""
            SELECT e1.normalized_text, e1.label, e2.normalized_text, e2.label,
                   COUNT(*) as weight
            FROM co_occurrences co
            JOIN entities e1 ON co.entity1_id = e1.id
            JOIN entities e2 ON co.entity2_id = e2.id
            GROUP BY e1.normalized_text, e2.normalized_text
            ORDER BY weight DESC
        """)

        network = []
        for row in cursor.fetchall():
            network.append({
                'source': row[0],
                'source_type': row[1],
                'target': row[2],
                'target_type': row[3],
                'weight': row[4]
            })

        network_file = output_dir / "co_occurrence_network.json"
        with open(network_file, 'w', encoding='utf-8') as f:
            json.dump(network, f, ensure_ascii=False, indent=2)

        print(f"  📊 Exported {len(entities)} entities ({len(unique_entities)} unique)")
        print(f"      Network edges: {len(network)}")

    def process_session(self, org_name: str, session_name: str, relevant_only: bool = True):
        """Process all text files in a session."""
        session_path = self.data_root / "processed" / org_name / session_name

        # Determine which folder to process
        if relevant_only:
            text_path = session_path / "relevant"
            if not text_path.exists():
                print(f"  ⚠ No relevant folder found: {text_path}")
                return
        else:
            text_path = session_path / "relevant"
            if not text_path.exists():
                text_path = session_path

        # Find all text files
        text_files = list(text_path.glob("*.txt"))

        if not text_files:
            print(f"  ⚠ No text files found in {text_path}")
            return

        print(f"\n📄 Processing {len(text_files)} text files from {session_name}")
        print(f"   Source: {text_path}")

        # Create database
        conn = self.create_database(org_name, session_name)
        output_dir = self.data_root / "actors" / org_name / session_name

        # Process each file
        for text_file in tqdm(text_files, desc="Extracting actors"):
            try:
                # Read text
                text = text_file.read_text(encoding='utf-8', errors='ignore')

                # Skip metadata header if present
                if "SOURCE_FILE:" in text and "="*80 in text:
                    parts = text.split("="*80, 1)
                    if len(parts) > 1:
                        text = parts[1].strip()

                # Extract entities
                entities = self.extract_entities_from_text(text, text_file.name)

                if entities:
                    self.save_entities_to_db(conn, entities)

                self.stats['files_processed'] += 1

            except Exception as e:
                print(f"\n  ✗ Error processing {text_file.name}: {e}")
                self.stats['errors'] += 1

        # Export results
        self.export_to_json(conn, output_dir)

        conn.close()

        print(f"   ✓ Database saved: {output_dir / 'actors.db'}")

    def process_organization(self, org_name: str, session_filter: str = None,
                           relevant_only: bool = True):
        """Process all sessions for an organization."""
        sessions = self.find_sessions(org_name)

        if not sessions:
            print(f"⚠ No processed sessions found for '{org_name}'")
            return

        if session_filter:
            sessions = [s for s in sessions if s == session_filter]
            if not sessions:
                print(f"⚠ Session '{session_filter}' not found for '{org_name}'")
                return

        print(f"\n{'='*80}")
        print(f"Extracting Actors: {org_name}")
        print(f"{'='*80}")
        print(f"Model: {self.model_name}")
        print(f"Threshold: {self.threshold}")
        print(f"Sessions: {len(sessions)}")

        for session in sessions:
            self.process_session(org_name, session, relevant_only)

    def process_all(self, relevant_only: bool = True):
        """Process all organizations and sessions."""
        orgs = self.find_organizations()

        if not orgs:
            print("⚠ No organizations found in data/processed/")
            return

        print(f"\n🔍 Found {len(orgs)} organizations: {', '.join(orgs)}")

        for org in orgs:
            self.process_organization(org, relevant_only=relevant_only)

    def print_summary(self):
        """Print processing statistics."""
        print(f"\n{'='*80}")
        print("📊 EXTRACTION SUMMARY")
        print(f"{'='*80}")
        print(f"Files processed:          {self.stats['files_processed']}")
        print(f"Total entities found:     {self.stats['total_entities']}")
        print(f"  ↳ Organizations:        {self.stats['organizations_found']}")
        print(f"  ↳ Persons:              {self.stats['persons_found']}")
        print(f"Errors:                   {self.stats['errors']}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract actors (organizations and persons) from Czech NGO texts using GLiNER",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract actors from one organization (recommended)
  python scripts/extract_actors.py --org "Hnutí DUHA"

  # Extract from all organizations
  python scripts/extract_actors.py --all

  # Use specific model and threshold
  python scripts/extract_actors.py --org "Arnika" --model "urchade/gliner_multi-v2.1" --threshold 0.3

  # Process all content (not just relevant)
  python scripts/extract_actors.py --org "Arnika" --all-content

  # List available data
  python scripts/extract_actors.py --list
        """
    )

    parser.add_argument('--org', type=str, help='Organization name to process')
    parser.add_argument('--session', type=str, help='Specific session timestamp to process')
    parser.add_argument('--all', action='store_true', help='Process all organizations')
    parser.add_argument('--data-root', type=str, default='data',
                       help='Root data directory (default: data)')
    parser.add_argument('--model', type=str, default=DEFAULT_MODEL,
                       help=f'GLiNER model to use (default: {DEFAULT_MODEL})')
    parser.add_argument('--threshold', type=float, default=DEFAULT_THRESHOLD,
                       help=f'Confidence threshold (default: {DEFAULT_THRESHOLD})')
    parser.add_argument('--context-window', type=int, default=DEFAULT_CONTEXT_WINDOW,
                       help=f'Context window size in characters (default: {DEFAULT_CONTEXT_WINDOW})')
    parser.add_argument('--all-content', action='store_true',
                       help='Process all content, not just relevant folder')
    parser.add_argument('--list', action='store_true',
                       help='List available organizations and sessions')

    args = parser.parse_args()

    # Handle --list command
    if args.list:
        data_root = Path(args.data_root)
        processed_path = data_root / "processed"

        if not processed_path.exists():
            print("⚠ No processed data found in data/processed/")
            return

        orgs = [d.name for d in processed_path.iterdir() if d.is_dir()]

        if not orgs:
            print("⚠ No organizations found in data/processed/")
            return

        print("\n📁 Available Organizations and Sessions:")
        for org in orgs:
            org_path = processed_path / org
            sessions = [d.name for d in org_path.iterdir() if d.is_dir()]
            print(f"\n  {org}:")
            for session in sessions:
                session_path = org_path / session
                relevant_path = session_path / "relevant"
                if relevant_path.exists():
                    txt_count = len(list(relevant_path.glob("*.txt")))
                    print(f"    - {session} ({txt_count} text files)")
                else:
                    print(f"    - {session} (no relevant folder)")
        return

    # Validate arguments
    if not args.all and not args.org:
        parser.error("Must specify either --org or --all")

    # Initialize extractor
    try:
        extractor = ActorExtractor(
            data_root=args.data_root,
            model_name=args.model,
            threshold=args.threshold,
            context_window=args.context_window
        )
    except Exception as e:
        print(f"✗ Failed to initialize extractor: {e}")
        sys.exit(1)

    # Process data
    relevant_only = not args.all_content

    if args.all:
        extractor.process_all(relevant_only=relevant_only)
    else:
        extractor.process_organization(
            args.org,
            session_filter=args.session,
            relevant_only=relevant_only
        )

    # Print summary
    extractor.print_summary()


if __name__ == "__main__":
    main()
