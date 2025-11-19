# Actor Extraction with GLiNER

## Overview

This tool uses **GLiNER** (Generalist and Lightweight Model for Named Entity Recognition) to extract actors from Czech NGO texts without requiring any training. GLiNER is a state-of-the-art NER model published at NAACL 2024 that can identify any entity type using a bidirectional transformer.

## Why GLiNER?

### Advantages for Czech NGO Analysis

1. **Zero-shot capability**: Works on Czech text without Czech-specific training
2. **Multilingual support**: GLiNER-Multi uses multilingual DeBERTa backbone
3. **Flexible entity types**: Can extract any entity types you define
4. **Lightweight**: More efficient than large language models
5. **High accuracy**: Outperforms ChatGPT on many NER benchmarks
6. **No API costs**: Runs locally on your hardware

### Model Performance

GLiNER was evaluated on the MultiCoNER multilingual dataset (11 languages). While Czech wasn't explicitly in the training data, the multilingual model demonstrates strong cross-lingual transfer capabilities through its multilingual transformer backbone.

**Expected performance on Czech:**
- Organizations: High precision (corporate/NGO names are distinctive)
- Persons: Good precision (Czech names follow predictable patterns)
- Context awareness: Captures surrounding text for disambiguation

## Installation

### Requirements

```bash
# Add to requirements.txt (already done)
gliner>=0.2.0

# Install
pip install gliner

# GPU support (recommended)
# GLiNER uses PyTorch - ensure you have CUDA drivers installed
# Installation will automatically download CUDA-enabled PyTorch if GPU available
```

### Hardware Requirements

- **CPU only**: Works but slower (~5-10 seconds per document)
- **GPU (NVIDIA)**: Much faster (~0.5-1 second per document)
- **RAM**: Minimum 4GB, recommended 8GB+
- **Disk**: ~500MB for model download (cached after first run)

## Usage

### Basic Usage

```bash
# Extract actors from one organization
python scripts/extract_actors.py --org "Hnutí DUHA"

# Process all organizations
python scripts/extract_actors.py --all

# List available data
python scripts/extract_actors.py --list
```

### Advanced Options

```bash
# Use different GLiNER model
python scripts/extract_actors.py --org "Arnika" --model "urchade/gliner_multi-v2.1"

# Adjust confidence threshold
# Lower threshold (0.3) = more entities extracted, more false positives
# Higher threshold (0.7) = fewer entities, higher precision
python scripts/extract_actors.py --org "Arnika" --threshold 0.3

# Process ALL content (not just relevant folder)
python scripts/extract_actors.py --org "Arnika" --all-content

# Adjust context window (characters before/after entity)
python scripts/extract_actors.py --org "Arnika" --context-window 150
```

### Available GLiNER Models

| Model | Size | Speed | Accuracy | Czech Support |
|-------|------|-------|----------|---------------|
| `urchade/gliner_multi-v2.1` | ~500MB | Fast | High | ✅ Multilingual |
| `urchade/gliner_medium-v2.1` | ~300MB | Faster | Medium | ⚠️ English-focused |
| `urchade/gliner_large-v2.1` | ~1GB | Slower | Highest | ⚠️ English-focused |

**Recommendation**: Use `gliner_multi-v2.1` (default) for Czech texts.

## Output Structure

### Database Schema

The tool creates a SQLite database for each organization/session:

```
data/actors/{organization}/{session}/
├── actors.db                        # SQLite database
├── entities.json                    # All extracted entities
├── unique_entities.json             # Deduplicated entities
└── co_occurrence_network.json       # Network edges
```

### Database Tables

**entities table:**
```sql
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,                -- Original entity text
    normalized_text TEXT NOT NULL,     -- Normalized for deduplication
    label TEXT NOT NULL,               -- 'organization' or 'person'
    score REAL NOT NULL,               -- Confidence score (0-1)
    context TEXT,                      -- Surrounding text
    source_file TEXT NOT NULL,         -- Source document
    extracted_at TEXT NOT NULL,        -- Timestamp
    start_pos INTEGER,                 -- Character position in text
    end_pos INTEGER
);
```

**co_occurrences table:**
```sql
CREATE TABLE co_occurrences (
    id INTEGER PRIMARY KEY,
    entity1_id INTEGER NOT NULL,
    entity2_id INTEGER NOT NULL,
    source_file TEXT NOT NULL,
    co_occurrence_count INTEGER DEFAULT 1,
    FOREIGN KEY (entity1_id) REFERENCES entities(id),
    FOREIGN KEY (entity2_id) REFERENCES entities(id)
);
```

### JSON Output Files

**entities.json** - All extracted entities:
```json
[
  {
    "text": "Hnutí DUHA",
    "normalized_text": "Hnutí DUHA",
    "label": "organization",
    "score": 0.95,
    "context": "...spolupracujeme s Hnutí DUHA na projektu...",
    "source_file": "page_001.txt",
    "extracted_at": "2025-11-19T14:30:00"
  }
]
```

**unique_entities.json** - Deduplicated entities:
```json
[
  {
    "name": "Hnutí DUHA",
    "type": "organization",
    "mention_count": 15,
    "avg_confidence": 0.93,
    "sources": ["page_001.txt", "page_002.txt", "page_045.txt"]
  }
]
```

**co_occurrence_network.json** - Network edges:
```json
[
  {
    "source": "Hnutí DUHA",
    "source_type": "organization",
    "target": "Greenpeace ČR",
    "target_type": "organization",
    "weight": 5
  }
]
```

## Integration with Analysis Pipeline

### Complete Workflow

```bash
# Step 1: Scrape NGO websites
python scripts/scraper_menu.py

# Step 2: Extract PDF text
python scripts/process_pdfs.py --all

# Step 3: Filter relevant content
python scripts/filter_content.py --all

# Step 4: Extract actors with GLiNER
python scripts/extract_actors.py --all

# Step 5: Analyze network (use your own tools)
```

### Using Extracted Data

#### Load entities in Python:

```python
import json

# Load unique entities
with open('data/actors/Hnutí DUHA/20240115_103000/unique_entities.json', 'r') as f:
    entities = json.load(f)

# Get all organizations
orgs = [e for e in entities if e['type'] == 'organization']
print(f"Found {len(orgs)} unique organizations")

# Get top 10 most mentioned
top_orgs = sorted(orgs, key=lambda x: x['mention_count'], reverse=True)[:10]
for org in top_orgs:
    print(f"{org['name']}: {org['mention_count']} mentions")
```

#### Load network in Python:

```python
import json
import networkx as nx

# Load co-occurrence network
with open('data/actors/Hnutí DUHA/20240115_103000/co_occurrence_network.json', 'r') as f:
    edges = json.load(f)

# Create NetworkX graph
G = nx.Graph()
for edge in edges:
    G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

# Analyze network
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.3f}")

# Find central actors
centrality = nx.degree_centrality(G)
top_actors = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 central actors:")
for actor, score in top_actors:
    print(f"  {actor}: {score:.3f}")
```

#### Query SQLite database:

```python
import sqlite3

conn = sqlite3.connect('data/actors/Hnutí DUHA/20240115_103000/actors.db')
cursor = conn.cursor()

# Find all mentions of a specific organization
cursor.execute("""
    SELECT text, context, source_file, score
    FROM entities
    WHERE normalized_text LIKE '%Greenpeace%'
    AND label = 'organization'
    ORDER BY score DESC
""")

for row in cursor.fetchall():
    print(f"Text: {row[0]}")
    print(f"Context: {row[1][:100]}...")
    print(f"Source: {row[2]}, Score: {row[3]:.2f}\n")

conn.close()
```

## Entity Normalization

The tool normalizes entity names for deduplication:

**Normalization rules:**
- Removes extra whitespace
- Removes common Czech legal suffixes: `s.r.o.`, `z.s.`, `o.s.`, `a.s.`
- Case-insensitive matching

**Examples:**
- `Hnutí DUHA z.s.` → `Hnutí DUHA`
- `Greenpeace  ČR` → `Greenpeace ČR`
- `Arnika  -  Občanské  sdružení` → `Arnika - Občanské sdružení`

## Troubleshooting

### Model Download Issues

**Problem**: Model fails to download

**Solutions**:
```bash
# Check internet connection
ping huggingface.co

# Download manually from Hugging Face
# Visit: https://huggingface.co/urchade/gliner_multi-v2.1

# Set HF cache directory
export HF_HOME=/path/to/cache
python scripts/extract_actors.py --org "Arnika"
```

### GPU Not Detected

**Problem**: Using CPU instead of GPU

**Solutions**:
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu121

# Check GPU usage during extraction
nvidia-smi
```

### Low Precision / Many False Positives

**Problem**: Extracting too many irrelevant entities

**Solutions**:
```bash
# Increase confidence threshold
python scripts/extract_actors.py --org "Arnika" --threshold 0.6

# Process only relevant content (default)
python scripts/extract_actors.py --org "Arnika" --relevant-only
```

### Missing Entities

**Problem**: Not extracting known entities

**Solutions**:
```bash
# Lower confidence threshold
python scripts/extract_actors.py --org "Arnika" --threshold 0.3

# Check if content was filtered out
ls data/processed/Arnika/*/relevant/

# Process all content (including irrelevant)
python scripts/extract_actors.py --org "Arnika" --all-content
```

## Performance Tips

### GPU Optimization

```bash
# For NVIDIA GPUs, ensure CUDA is available
python -c "import torch; print(torch.cuda.get_device_name(0))"

# Monitor GPU usage
watch -n 1 nvidia-smi
```

### Batch Processing

For large datasets, process organizations one at a time:

```bash
# Process each organization separately
for org in "Hnutí DUHA" "Arnika" "Greenpeace ČR"; do
    echo "Processing: $org"
    python scripts/extract_actors.py --org "$org"
done
```

### Memory Management

If running out of memory:

```bash
# Process smaller batches
# Edit script to process fewer files at once

# Use smaller model
python scripts/extract_actors.py --org "Arnika" --model "urchade/gliner_medium-v2.1"

# Close other applications
# Monitor memory: htop or top
```

## Research References

### GLiNER Paper

```bibtex
@inproceedings{zaratiana2024gliner,
  title={GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer},
  author={Zaratiana, Urchade and Tomeh, Nadi and Holat, Pierre and Charnois, Thierry},
  booktitle={Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)},
  pages={5364--5376},
  year={2024}
}
```

### Links

- **Paper**: https://aclanthology.org/2024.naacl-long.300/
- **ArXiv**: https://arxiv.org/abs/2311.08526
- **GitHub**: https://github.com/urchade/GLiNER
- **Models**: https://huggingface.co/urchade

## Future Improvements

Potential enhancements for Czech NGO analysis:

1. **Fine-tuning on Czech NGO corpus**: Train GLiNER on Czech NGO-specific data for higher accuracy
2. **Entity linking**: Connect extracted entities to knowledge base (Wikipedia, company registry)
3. **Relation extraction**: Extract relationships between entities (partnerships, funding)
4. **Temporal analysis**: Track actor mentions over time
5. **Entity disambiguation**: Resolve entity references (e.g., "DUHA" → "Hnutí DUHA")
6. **Additional entity types**: Extract locations, events, projects, funding sources

## Contact

For questions or issues with actor extraction:
- Email: 498079@mail.muni.cz
- Repository: https://github.com/Leriot/leriot-web-scraper-for-thesis
