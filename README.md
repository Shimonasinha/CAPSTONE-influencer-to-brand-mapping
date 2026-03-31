# CAPSTONE-influencer-to-brand-mapping

## Project Structure

```
CAPSTONE-influencer-to-brand-mapping/
├── data/
│   ├── raw/                    # Original scraped data
│   │   ├── youtube/
│   │   ├── twitter/
│   │   └── reddit/
│   └── scripts/                # Data collection scripts
│       └── Scraping/
├── notebooks/                  # Jupyter notebooks for research
│   ├── 01_exploratory_analysis/
│   ├── 02_bot_detection/
│   ├── 03_feature_extraction/
│   └── 04_documentation/
├── processed_data/             # Cleaned and processed data
├── models/                     # Saved models and embeddings
├── research_outputs/           # Visualizations and reports for paper
└── requirements.txt            # Python dependencies
```

## Components

### 1. Fake Follower Detection
- **YouTube**: Subscriber authenticity, comment spam detection
- **Twitter**: Fake follower identification, engagement quality analysis
- **Reddit**: Bot account detection, content authenticity

### 2. Feature Extraction
- **CLIP**: Visual embeddings from YouTube thumbnails (512-dim)
- **BERT**: Textual embeddings from content (768-dim)
- **Multi-modal**: Combined visual + textual features

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download NLTK data (if needed):
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

3. For GPU acceleration (recommended for CLIP/BERT):
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"
```

## Notebooks

All notebooks are self-contained with:
- Markdown documentation explaining methodology
- Code with inline comments
- Visualizations for research paper
- Performance metrics and analysis

## Research Paper Support

Each notebook generates outputs suitable for academic research:
- Publication-ready figures (high resolution)
- Statistical test results
- Methodology documentation
- Reproducibility information

## Data Sources

- **YouTube**: 26M+ subscribers across channels, 2.1M videos, 5.2M comments
- **Twitter**: 120K+ user profiles and engagement data
- **Reddit**: 14M posts from fitness communities

## Notes

- Ensure sufficient disk space for embeddings (~2GB for visual, ~5GB for textual)
- GPU recommended for CLIP/BERT (10-20x faster than CPU)
- Notebooks save intermediate results to avoid reprocessing