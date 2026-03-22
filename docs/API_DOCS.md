# API Documentation

## Arabic Sentiment Analysis API

Production-ready REST API for Arabic sentiment analysis using fine-tuned AraBERT transformer model.

---

## Base URL

- **Development:** `http://localhost:8000`
- **Production:** `https://api.arabic-sentiment.example.com`

---

## Endpoints

### 1. Root Endpoint

Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Arabic Sentiment Analysis API",
  "version": "1.0.0",
  "model": "Belall87/arabert-arabic-sentiment",
  "endpoints": {
    "docs": "/docs",
    "health": "/health",
    "predict": "/predict",
    "batch_predict": "/predict/batch",
    "model_info": "/model/info"
  }
}
```

---

### 2. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "uptime_seconds": 3600.5
}
```

---

### 3. Single Text Prediction

**Endpoint:** `POST /predict`

**Request:**
```json
{
  "text": "هذا المنتج رائع جداً"
}
```

**Response:**
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

---

### 4. Batch Prediction

**Endpoint:** `POST /predict/batch`

**Request:**
```json
{
  "texts": ["هذا المنتج رائع", "تجربة سيئة"]
}
```

---

## Interactive Docs

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

