# Arabic Sentiment Analysis: BiLSTM vs AraBERT Comparison

Comprehensive comparison of traditional deep learning (BiLSTM) and modern transfer learning (AraBERT) approaches for Arabic sentiment classification.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT)
[![Hugging Face](https://img.shields.io/badge/🤗-AraBERT_Model-yellow)](https://huggingface.co/Belall87/arabert-arabic-sentiment)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Project Overview

This project implements and compares two state-of-the-art approaches for Arabic sentiment analysis:

### **1. BiLSTM (Bidirectional LSTM)**
- Custom architecture with trainable word embeddings
- Bidirectional processing for context understanding
- 2-layer LSTM with dropout regularization
- **Accuracy: ~84.53%** (update with your results)

### **2. AraBERT (Transfer Learning)**
- Fine-tuned BERT-base model pre-trained on Arabic corpus
- Transformer architecture with 12 attention layers
- State-of-the-art NLP performance
- **Accuracy: ~92.87%** (update with your results)

---

## 📊 Model Comparison

| Model | Architecture | Parameters | Accuracy | F1-Score | Training Time |
|-------|-------------|------------|----------|----------|---------------|
| BiLSTM | 2-layer BiLSTM | ~500K | 84.53% | 84.03% | ~10 min |
| AraBERT | BERT-base | ~110M | 92.87% | 92.87% | ~30 min |

**Winner:** AraBERT outperformed BiLSTM by 92.87% in accuracy

---

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT.git
cd Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT

# Install dependencies
pip install -r requirements.txt
```

### Using AraBERT (Recommended)
```python
from transformers import pipeline

# Load fine-tuned AraBERT from Hugging Face
classifier = pipeline(
    "sentiment-analysis",
    model="Belall87/arabert-arabic-sentiment"
)

# Predict
result = classifier("هذا المنتج رائع جداً")
print(result)
# Output: [{'label': 'POSITIVE', 'score': 0.95}]
```

### Using BiLSTM
```python
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load model and tokenizer
model = load_model('models/bilstm_best_model.h5')
with open('models/bilstm_tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Predict
text = "الخدمة ممتازة"
seq = tokenizer.texts_to_sequences([text])
padded = pad_sequences(seq, maxlen=100)
prediction = model.predict(padded)[0][0]

sentiment = "Positive" if prediction >= 0.5 else "Negative"
print(f"{sentiment} ({prediction:.2%})")
```

---

## 🛠️ Technologies Used

### BiLSTM Model
- **Framework:** TensorFlow/Keras
- **Architecture:** Bidirectional LSTM
- **Embeddings:** Trainable 128-dim word vectors
- **Regularization:** Dropout (0.3)

### AraBERT Model
- **Framework:** PyTorch + Hugging Face Transformers
- **Base Model:** aubmindlab/bert-base-arabertv02
- **Fine-tuning:** Task-specific sentiment classification
- **Optimization:** AdamW with cosine scheduling

---

## 📁 Project Structure
```
Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   └── bilstm_vs_arabert_comparison.ipynb    # Main analysis notebook
│
├── models/
│   ├── bilstm_best_model.h5                  # Trained BiLSTM model
│   └── bilstm_tokenizer.pkl                   # BiLSTM tokenizer
│
├── results/
│   ├── comparison_metrics.json
│   └── plots/
│       ├── accuracy_comparison.png
│       ├── confusion_matrices.png
│       └── training_history.png
│
└── data/
    └── README.md                              # Dataset information
```

---

## 🔬 Methodology

### 1. Data Preprocessing
- Arabic text normalization (alef, yeh, hamza variants)
- Diacritics (tashkeel) removal
- URL, mention, and hashtag filtering
- Whitespace normalization

### 2. BiLSTM Architecture
```
Embedding (128-dim)
    ↓
BiLSTM-1 (64 units) → Dropout (0.3)
    ↓
BiLSTM-2 (32 units) → Dropout (0.3)
    ↓
Dense (16, ReLU) → Dropout (0.2)
    ↓
Output (1, Sigmoid)
```

### 3. AraBERT Fine-tuning
- Base: aubmindlab/bert-base-arabertv02
- Added classification head for binary sentiment
- Training: 3 epochs with early stopping
- Learning rate: 2e-5 with warmup

### 4. Evaluation
- Train/Val/Test split: 72%/8%/20%
- Stratified sampling for class balance
- Metrics: Accuracy, Precision, Recall, F1-Score
- Confusion matrix analysis

---

## 📈 Results

### Key Findings

1. **AraBERT Superior Performance**
   - Higher accuracy by XX%
   - Better handling of context and nuance
   - Robust to spelling variations

2. **BiLSTM Advantages**
   - Faster inference time
   - Smaller model size (~1000x smaller)
   - Lower computational requirements

3. **Use Case Recommendations**
   - **Production (high accuracy needed):** AraBERT
   - **Edge devices (resource-constrained):** BiLSTM
   - **Real-time systems:** BiLSTM
   - **Research/benchmarking:** AraBERT

### Training Curves

![Model Comparison](results/plots/comparison.png)

---

## 🔗 Links & Resources

- **🤗 AraBERT Model:** [Belall87/arabert-arabic-sentiment](https://huggingface.co/Belall87/arabert-arabic-sentiment)
- **📓 Kaggle Notebook:** [https://www.kaggle.com/code/bilalmahmoud/arabic-sentiment-analysis-cv/edit/run/294758328]
- **📚 Base Model:** [aubmindlab/bert-base-arabertv02](https://huggingface.co/aubmindlab/bert-base-arabertv02)
- **💻 GitHub:** [Bolaal/Arabic-Sentiment-Analysis](https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT)

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Arabic NLP preprocessing techniques
- ✅ Custom LSTM architecture design
- ✅ Transfer learning with transformers
- ✅ Model comparison methodology
- ✅ Production-ready inference pipelines

---

## 📝 Citation
```bibtex
@misc{arabic-sentiment-comparison-2025,
  author = {Belal Mahmoud Hussien},
  title = {Arabic Sentiment Analysis: BiLSTM vs AraBERT Comparison},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT}
}
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

---

## 📧 Contact

**Belal Mahmoud Hussien**

- 📧 Email: belalmahmoud8787@gmail.com
- 💼 LinkedIn: [Belal Mahmoud](https://www.linkedin.com/in/belal-mahmoud-husien)
- 🐱 GitHub: [@Bolaal](https://github.com/Bolaal)
- 🤗 Hugging Face: [@Belall87](https://huggingface.co/Belall87)

---

<div align="center">

**Made with ❤️ for the Arabic NLP Community**

⭐ Star this repo if you found it helpful!

</div>
