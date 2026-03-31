# Getting Started Guide: Edge Processing for Influencer-Brand Mapping

## Overview

This guide will help you get started with the edge processing components of the influencer-brand mapping project. The project focuses on two main areas:

1. **Fake Follower Detection**: Bot removal and account verification
2. **Feature Extraction**: Multi-modal embeddings using CLIP (visual) and BERT (textual)

## Quick Start

### 1. Install Dependencies

```bash
cd /home/sonic/Work/CAPSTONE-influencer-to-brand-mapping
pip install -r requirements.txt
```

**Note**: This will install:
- PyTorch and TorchVision (deep learning)
- Transformers library (BERT)
- CLIP from OpenAI
- Data science libraries (pandas, numpy, sklearn)
- Visualization tools (matplotlib, seaborn, plotly)

### 2. Check GPU Availability (Recommended)

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
```

**Processing Time Estimates**:
- With GPU: ~8-12 hours for full pipeline
- Without GPU: ~2-3 days for full pipeline

### 3. Navigate the Notebooks

The project is organized into four main phases:

#### Phase 1: Exploratory Analysis
```
notebooks/01_exploratory_analysis/
└── 01_exploratory_data_analysis.ipynb
```
**Purpose**: Understand the dataset structure, quality, and characteristics  
**Run Time**: ~10-15 minutes  
**Output**: Summary statistics, visualizations

#### Phase 2: Bot Detection
```
notebooks/02_bot_detection/
├── 00_bot_detection_research.ipynb     # Learning: Theory and methods
├── 01_youtube_bot_detection.ipynb      # Implementation: YouTube
└── 02_twitter_bot_detection.ipynb      # Implementation: Twitter
```
**Purpose**: Remove fake accounts and spam content  
**Run Time**: ~1-2 hours per platform  
**Output**: Cleaned datasets, bot scores, performance metrics

#### Phase 3: Feature Extraction
```
notebooks/03_feature_extraction/
├── 00_embeddings_research.ipynb        # Learning: CLIP and BERT
├── 01_clip_visual_features.ipynb       # Implementation: Visual embeddings
├── 02_bert_textual_features.ipynb      # Implementation: Textual embeddings
└── 03_multimodal_integration.ipynb     # Integration: Combined features
```
**Purpose**: Extract rich multi-modal feature representations  
**Run Time**: ~6-10 hours total (depends on GPU)  
**Output**: Embeddings, visualizations, clusters

#### Phase 4: Documentation
```
notebooks/04_documentation/
└── 00_research_methodology.ipynb       # Research paper methodology
```
**Purpose**: Compile results and methodology for research paper  
**Run Time**: Update as experiments complete  
**Output**: Methodology section, results tables

## Workflow Guide

### For Learning

1. **Start with research notebooks**:
   - `00_bot_detection_research.ipynb` - Understand bot detection theory
   - `00_embeddings_research.ipynb` - Learn about CLIP and BERT

2. **Review the methodology**:
   - `00_research_methodology.ipynb` - See how everything fits together

3. **Explore the data**:
   - `01_exploratory_data_analysis.ipynb` - Understand the dataset

### For Implementation

1. **Run in order**:
   ```bash
   # Phase 1: Understand the data
   jupyter notebook notebooks/01_exploratory_analysis/01_exploratory_data_analysis.ipynb
   
   # Phase 2: Clean the data
   jupyter notebook notebooks/02_bot_detection/01_youtube_bot_detection.ipynb
   jupyter notebook notebooks/02_bot_detection/02_twitter_bot_detection.ipynb
   
   # Phase 3: Extract features
   jupyter notebook notebooks/03_feature_extraction/01_clip_visual_features.ipynb
   jupyter notebook notebooks/03_feature_extraction/02_bert_textual_features.ipynb
   jupyter notebook notebooks/03_feature_extraction/03_multimodal_integration.ipynb
   ```

2. **Monitor progress**:
   - Each notebook saves intermediate results
   - Check `processed_data/` for cleaned datasets
   - Check `models/` for saved embeddings
   - Check `research_outputs/` for visualizations

### For Research Paper

1. **Methodology section**:
   - Use `00_research_methodology.ipynb` as template
   - Fill in results from experiment notebooks
   - Update with actual performance metrics

2. **Visualizations**:
   - All notebooks generate publication-ready figures
   - Saved to `research_outputs/` as high-resolution PNGs
   - Include confusion matrices, ROC curves, t-SNE plots, etc.

3. **Results tables**:
   - CSV files in `research_outputs/` with summary statistics
   - Easy to import into LaTeX or Word

## Dataset Structure

```
data/
├── raw/                          # Original scraped data
│   ├── youtube/
│   │   ├── final_youtube_channels_clean.csv      (~145K rows)
│   │   ├── final_youtube_videos_clean.csv        (~2.1M rows)
│   │   └── final_youtube_comments_clean.csv      (~5.2M rows)
│   ├── twitter/
│   │   ├── final_twitter_matched.csv             (~120K rows)
│   │   └── final_twitter_brands.csv              
│   └── reddit/
│       └── final_reddit_posts.csv                (~14M rows)
│
├── processed_data/               # After bot removal (created by notebooks)
│   ├── youtube_channels_clean_no_bots.csv
│   ├── youtube_videos_clean_no_bots.csv
│   ├── twitter_users_clean_no_bots.csv
│   └── reddit_posts_clean_no_bots.csv
│
└── models/                       # Saved embeddings (created by notebooks)
    ├── youtube_clip_embeddings.npy
    ├── youtube_bert_embeddings.npy
    ├── twitter_bert_embeddings.npy
    └── multimodal_combined_embeddings.npy
```

## Expected Outputs

### Bot Detection
- **Metrics**: Precision >0.9, Recall >0.7, F1 >0.79
- **Bot Removal Rate**: 8-12% of accounts flagged
- **Data Quality**: 30-50% improvement in engagement metrics

### Feature Extraction
- **Visual Embeddings**: ~2M × 512 dimensions (~4 GB)
- **Textual Embeddings**: ~5M × 768 dimensions (~15 GB)
- **Processing Time**: 8-12 hours on GPU
- **Cluster Quality**: Silhouette score >0.4

## Troubleshooting

### Out of Memory Errors

**Problem**: GPU running out of memory during batch processing

**Solution**:
```python
# Reduce batch size in notebook
batch_size = 64  # Instead of 256
```

### CUDA Out of Memory

**Problem**: Large model won't fit on GPU

**Solution**:
```python
# Use CPU (slower but works)
device = "cpu"
# Or use smaller model variant
model = BertModel.from_pretrained('distilbert-base-uncased')
```

### Slow Processing

**Problem**: Taking too long without GPU

**Solutions**:
1. Process a smaller sample first:
   ```python
   df_sample = df.head(10000)  # Test on 10K rows
   ```

2. Use multiprocessing for CPU:
   ```python
   from multiprocessing import Pool
   with Pool(processes=8) as pool:
       results = pool.map(process_function, data)
   ```

3. Save intermediate results frequently:
   ```python
   # Save every 1000 items
   if i % 1000 == 0:
       np.save(f'embeddings_checkpoint_{i}.npy', embeddings)
   ```

## Key Concepts

### Bot Detection

**Heuristic Approach**:
- Fast, rule-based scoring
- Platform-specific indicators
- Good for obvious cases

**ML Approach**:
- More accurate for edge cases
- Requires feature engineering
- Can adapt to new patterns

**Hybrid Pipeline**:
- Use heuristics first (fast filtering)
- Apply ML to uncertain cases (high accuracy)
- Best of both worlds

### Feature Extraction

**CLIP (Visual)**:
- Encodes images into 512-dim vectors
- Understands visual brand elements
- Zero-shot classification capable

**BERT (Textual)**:
- Encodes text into 768-dim vectors
- Captures semantic meaning
- Context-aware representations

**Multi-Modal**:
- Combines visual + textual
- Richer representation
- Better for brand matching

## Tips for Success

### 1. Start Small
- Test on small data samples first
- Verify pipeline works end-to-end
- Then scale to full dataset

### 2. Save Intermediate Results
- Don't reprocess everything if something fails
- Save cleaned data after each phase
- Save embeddings in batches

### 3. Monitor Resource Usage
```python
import psutil
print(f"CPU: {psutil.cpu_percent()}%")
print(f"RAM: {psutil.virtual_memory().percent}%")

import torch
if torch.cuda.is_available():
    print(f"GPU Memory: {torch.cuda.memory_allocated()/1e9:.2f} GB")
```

### 4. Document as You Go
- Take notes in notebook markdown cells
- Screenshot interesting visualizations
- Record performance metrics

### 5. Version Control
```bash
git add notebooks/
git commit -m "Add bot detection implementation"
git push
```

## Next Steps After Setup

1. **Run EDA notebook** to understand the data
2. **Read research notebooks** to learn the theory
3. **Start with one platform** (YouTube recommended - most complete data)
4. **Extract features** after bot detection
5. **Integrate results** for downstream GAIL pipeline

## Support and Resources

**Documentation**:
- CLIP: https://github.com/openai/CLIP
- BERT: https://huggingface.co/bert-base-uncased
- Transformers: https://huggingface.co/docs/transformers/

**Papers**:
- CLIP: Radford et al. (2021) "Learning Transferable Visual Models..."
- BERT: Devlin et al. (2019) "BERT: Pre-training of Deep Bidirectional..."
- Bot Detection: Ferrara et al. (2016) "The Rise of Social Bots"

**Questions?**
- Check notebook markdown cells for explanations
- Review error messages carefully
- Verify data paths and file existence

## Estimated Timeline

**Week 1**: Setup + EDA + Bot Detection Research
- Install dependencies
- Run exploratory analysis
- Study bot detection methods

**Week 2**: Bot Detection Implementation
- YouTube bot detection
- Twitter bot detection
- Validate and clean datasets

**Week 3**: Feature Extraction
- CLIP visual embeddings
- BERT textual embeddings
- Multi-modal integration

**Week 4**: Documentation + Analysis
- Compile results
- Generate visualizations
- Write methodology section

**Total**: ~4 weeks for complete implementation and documentation

## Success Criteria

✅ Environment set up correctly  
✅ All notebooks run without errors  
✅ Bot detection achieves >0.9 precision  
✅ Embeddings extracted for all content  
✅ Visualizations generated  
✅ Research methodology documented  
✅ Results compiled for paper  

Good luck with your research! 🚀
