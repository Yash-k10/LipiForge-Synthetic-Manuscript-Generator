---
license: mit
task_categories:
- image-to-text
language:
- sa
- mr
tags:
- historical-manuscript
- synthetic-data
- indic-ocr
- devanagari
- modi
- sharada
pretty_name: LipiForge Synthetic Historical Indic Manuscripts
size_categories:
- n<1K
configs:
- config_name: devanagari
  data_files:
  - split: train
    path: devanagari/train/**
  - split: validation
    path: devanagari/validation/**
  - split: test
    path: devanagari/test/**
- config_name: modi
  data_files:
  - split: train
    path: modi/train/**
  - split: validation
    path: modi/validation/**
  - split: test
    path: modi/test/**
- config_name: sharada
  data_files:
  - split: train
    path: sharada/train/**
  - split: validation
    path: sharada/validation/**
  - split: test
    path: sharada/test/**
---

# LipiForge: Synthetic Historical Indic Manuscripts Dataset

This dataset contains **300 photorealistic synthetic Indic manuscript folios** paired with **synchronized line-by-line ground-truth annotations (`.md`)** across three historical scripts: **Devanagari**, **Modi**, and **Sharada**.

## 📁 Dataset Subsets & Splits

The dataset provides three distinct subsets selectable via the Hugging Face Subset dropdown:
- **`devanagari`**: 85 train, 10 validation, 5 test
- **`modi`**: 85 train, 10 validation, 5 test
- **`sharada`**: 85 train, 10 validation, 5 test

```text
├── devanagari/
│   ├── train/          # 85 images (.png) + 85 ground-truth transcripts (.md)
│   ├── validation/     # 10 images (.png) + 10 ground-truth transcripts (.md)
│   └── test/           # 5 images (.png) + 5 ground-truth transcripts (.md)
├── modi/
│   ├── train/          # 85 images (.png) + 85 ground-truth transcripts (.md)
│   ├── validation/     # 10 images (.png) + 10 ground-truth transcripts (.md)
│   └── test/           # 5 images (.png) + 5 ground-truth transcripts (.md)
└── sharada/
    ├── train/          # 85 images (.png) + 85 ground-truth transcripts (.md)
    ├── validation/     # 10 images (.png) + 10 ground-truth transcripts (.md)
    └── test/           # 5 images (.png) + 5 ground-truth transcripts (.md)
```

## 📜 Annotation Format

Each folio (e.g. `folio_001.png`) is paired with an identical `.md` file (`folio_001.md`) containing the clean line-by-line transcription corresponding to the lines on the folio image.
