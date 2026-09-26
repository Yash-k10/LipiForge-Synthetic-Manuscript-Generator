# LipiForge: Synthetic Historical Indic Manuscript Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-yellow)](https://huggingface.co/datasets/Yash-kapse/synthetic-manuscripts)

An automated, end-to-end Python pipeline engineered to synthesize **photorealistic historical Indic manuscript folios** paired with **synchronized ground-truth annotations (`.md`)**.

Developed to bridge the domain gap in historical Optical Character Recognition (OCR), **LipiForge** simulates authentic manuscript materials (aged handmade rag paper, palm-leaf strips), natural calligraphic handwriting, traditional scribal layouts, dual-ink rubrication, and natural physical degradation.

---

## 🏛️ Key Features

- **Multi-Script Support**: Out-of-the-box synthesis for three historical Indic scripts:
  - **Devanagari**: Classical Sanskrit and Hindi verses with continuous headstroke (*shirorekha*).
  - **Modi**: Historical cursive script with continuous looping characters and sloped baselines.
  - **Sharada**: Ancient Kashmiri Brahmi-derived script with distinctive angles and sharp strokes.
- **Physical Manuscript Realism (≥90% Visual Parity)**:
  - **Authentic Paper Materials**: Vibrant antique golden-ochre parchment, classical aged paper, and fibrous palm-leaf (*Tāḍapatra*).
  - **Physical Folio Features**: Hand-drawn double vertical red margin rules, margin binding pin-holes, and frayed deckle borders.
  - **Aging & Degradation**: Edge oxidation, natural paper creases, subtle handling stains, and scattered dark foxing spots.
- **Natural Calligraphy & Humanized Imperfections**:
  - **Reed-Pen Dipping Simulation**: Variable ink density and saturation across sentences (dark fresh ink to thinner dry strokes).
  - **Organic Baseline Drift**: Micro-jitter and gentle baseline waviness replicating natural human scribal movement.
  - **Dual-Ink Rubrication**: Deep charcoal/iron-gall black for primary body text with rich cinnabar/vermilion red accents for section headers, dandas (`।`, `॥`), and highlighted keywords.
- **Synchronized Ground Truth Annotations**:
  - Every image `folio_XXX.png` is paired with an exact line-by-line `.md` transcription file matching the visual line breaks.
- **Strict Boundary Guarantee**:
  - Dynamic line-breaking ensures 0% horizontal or vertical text overflow off the folio.

---

## 📂 Repository Structure

```text
LipiForge/
├── dataset/                    # Generated synthetic manuscript dataset (300 folios)
│   ├── devanagari/             # Devanagari subset
│   │   ├── train/              # 85 images + 85 .md annotation files
│   │   ├── validation/         # 10 images + 10 .md annotation files
│   │   └── test/               # 5 images + 5 .md annotation files
│   ├── modi/                   # Modi subset (85 train, 10 val, 5 test)
│   │   ├── train/
│   │   ├── validation/
│   │   └── test/
│   └── sharada/                # Sharada subset (85 train, 10 val, 5 test)
│       ├── train/
│       ├── validation/
│       └── test/
├── fonts/                      # Open-source TrueType font assets
│   ├── devanagari_kalam.ttf    # Calligraphic handwriting Devanagari font
│   ├── devanagari_yatra.ttf    # Traditional signage style font
│   ├── modi_noto.ttf           # Official Google Noto Modi Unicode font
│   └── sharada_noto.ttf        # Official Google Noto Sharada Unicode font
├── pipeline/                   # Modular generator package
│   ├── __init__.py
│   ├── background.py           # Procedural parchment & physical aging engine
│   ├── renderer.py             # Calligraphy, rubrication, & ground-truth renderer
│   ├── corpus.py               # Text loading & unique chunk sampling
│   └── uploader.py             # Hugging Face Hub dataset uploader
├── devanagari_md.md            # Raw corpus text for Devanagari (classical Sanskrit)
├── Modi_md.md                  # Raw corpus text for Modi (historical Marathi)
├── sharada_md.md               # Raw corpus text for Sharada (classical Sanskrit)
├── generate.py                 # Single terminal entrypoint for dataset generation
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation & setup guide
```

---

## 📊 Dataset Distribution & Hugging Face Hub

The generated dataset consists of **300 total image-annotation pairs** distributed across the three scripts according to the specified split:

| Script | Train (85%) | Validation (10%) | Test (5%) | Total Folios |
| :--- | :---: | :---: | :---: | :---: |
| **Devanagari** | 85 | 10 | 5 | **100** |
| **Modi** | 85 | 10 | 5 | **100** |
| **Sharada** | 85 | 10 | 5 | **100** |
| **Total** | **255** | **30** | **15** | **300** |

- **Hugging Face Dataset Repository**: [`Yash-kapse/synthetic-manuscripts`](https://huggingface.co/datasets/Yash-kapse/synthetic-manuscripts)
- **GitHub Repository**: [`https://github.com/Yash-k10/LipiForge-Synthetic-Manuscript-Generator.git`](https://github.com/Yash-k10/LipiForge-Synthetic-Manuscript-Generator.git)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Yash-k10/LipiForge-Synthetic-Manuscript-Generator.git
cd LipiForge-Synthetic-Manuscript-Generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage & Execution

### 1. Run Complete Generation via Terminal
To generate the full 300 folios (100 per script with 85/10/5 splits) along with their paired `.md` annotation files:
```bash
python generate.py
```

### 2. Optional Arguments
- `--count`: Set custom image count per script (default: `100`).
- `--output_dir`: Set custom destination folder (default: `dataset`).
- `--push_to_hub`: Upload generated dataset to Hugging Face Hub after synthesis.
- `--hf_repo`: Hugging Face dataset repo ID (default: `Yash-kapse/synthetic-manuscripts`).
- `--hf_token`: Hugging Face write token (or set via `HF_TOKEN` environment variable).

**Example: Generate and push directly to Hugging Face:**
```bash
python generate.py --push_to_hub --hf_token "your_hf_token_here"
```

---

## 📝 Ground-Truth Annotation Specification

Each image (`folio_001.png`) is accompanied by an exact synchronized Markdown (`folio_001.md`) file containing the clean, line-for-line transcription of the visible text:

**Example `folio_001.md`**:
```markdown
तथोर्ध्वशायिकावृक्षे तथान्ये मृगचारिणः । पंचाग्नयस्तथा चान्ये केचित्
पर्णफलाशिनः ॥ ११४ ॥
अधमाढकमानस्य हविषो मुख्यकल्पने । मात्रार्थं तण्डुलं प्रस्थं
तदर्धमनुकल्पके ॥ ॥
विद्यातपोव्रतधरानसृजः प्रथमं द्विजा । आत्मतत्त्वं समावेत्तुं मुखतः
परमेश्वरः ॥ ३८ ॥
अब्भक्षा वायुभक्षाश्च तथाऽन्ये शाकभक्षिणः । तापसा विविधास्त्वेते
```

This ensures plug-and-play compatibility with modern Line-Level and Page-Level OCR architectures (TrOCR, CRNN, Vision-Language OCR models).

---

## 📜 License
This project is licensed under the MIT License.
