# Quick Start Guide

Get the Arabic Sentiment Analysis API running in minutes.

## 🚀 Fastest Way: Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT.git
cd Arabic-Sentiment-BiLSTM-vs-AraBERT

# 2. Start the API
docker-compose up -d

# 3. Wait ~30 seconds for model download, then test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "هذا المنتج رائع جداً"}'
```

**Output:**
```json
{
  "label": "positive",
  "confidence": 0.9842,
  "scores": {
    "negative": 0.0158,
    "positive": 0.9842
  }
}
```

## 📖 Interactive API Documentation

Visit: http://localhost:8000/docs

## 🛑 Stop the Service

```bash
docker-compose down
```

## 📚 Next Steps

- Read [API Documentation](docs/API_DOCS.md) for all endpoints
- See [Deployment Guide](docs/DEPLOYMENT.md) for production deployment
- Check [README.md](README.md) for project details

---

**Need Help?**
- GitHub Issues: https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT/issues
- Email: belalmahmoud8787@gmail.com
