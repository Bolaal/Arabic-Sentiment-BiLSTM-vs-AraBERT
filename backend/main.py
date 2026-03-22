import os
import logging
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
MODEL_NAME = os.getenv("MODEL_NAME", "Belall87/arabert-arabic-sentiment")
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "128"))
PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(
    title="Arabic Sentiment Analysis API",
    version="1.0.0",
    description="Production-ready API for Arabic sentiment analysis using fine-tuned AraBERT",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
tokenizer = None
model = None
LABELS = {0: "negative", 1: "positive"}

# Startup timestamp
startup_time = None


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, description="Arabic text to analyze")


class BatchTextInput(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100, description="List of Arabic texts to analyze")


class PredictionOutput(BaseModel):
    label: str = Field(..., description="Predicted sentiment label")
    confidence: float = Field(..., description="Confidence score for the prediction")
    scores: dict = Field(..., description="Probability scores for all classes")


class BatchPredictionOutput(BaseModel):
    predictions: List[PredictionOutput]
    count: int


class ModelInfo(BaseModel):
    model_name: str
    model_loaded: bool
    max_length: int
    available_labels: dict
    device: str


class HealthStatus(BaseModel):
    status: str
    model_loaded: bool
    uptime_seconds: float


@app.on_event("startup")
async def startup_event():
    """Load model on application startup"""
    global tokenizer, model, startup_time
    startup_time = datetime.now()
    
    try:
        logger.info(f"Loading model: {MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.eval()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Application shutting down")


@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Arabic Sentiment Analysis API",
        "version": "1.0.0",
        "model": MODEL_NAME,
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "model_info": "/model/info"
        }
    }


@app.get("/health", response_model=HealthStatus)
def health():
    """Health check endpoint for liveness and readiness probes"""
    uptime = (datetime.now() - startup_time).total_seconds() if startup_time else 0
    model_loaded = model is not None and tokenizer is not None
    
    return HealthStatus(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        uptime_seconds=uptime
    )


@app.get("/model/info", response_model=ModelInfo)
def model_info():
    """Get information about the loaded model"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    return ModelInfo(
        model_name=MODEL_NAME,
        model_loaded=True,
        max_length=MAX_LENGTH,
        available_labels=LABELS,
        device=device
    )


@app.post("/predict", response_model=PredictionOutput)
def predict(input: TextInput):
    """Predict sentiment for a single text input"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    try:
        logger.debug(f"Processing text: {input.text[:50]}...")
        
        inputs = tokenizer(
            input.text,
            return_tensors="pt",
            truncation=True,
            max_length=MAX_LENGTH,
            padding=True,
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.softmax(outputs.logits, dim=-1).squeeze().tolist()

        if isinstance(probs, float):
            probs = [probs]

        predicted_class = int(torch.argmax(outputs.logits).item())
        confidence = float(max(probs))
        scores = {LABELS[i]: round(float(p), 4) for i, p in enumerate(probs)}

        logger.info(f"Prediction: {LABELS[predicted_class]} (confidence: {confidence:.2%})")

        return PredictionOutput(
            label=LABELS[predicted_class],
            confidence=round(confidence, 4),
            scores=scores,
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionOutput)
def batch_predict(input: BatchTextInput):
    """Predict sentiment for multiple texts in batch"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        logger.info(f"Processing batch of {len(input.texts)} texts")
        
        predictions = []
        
        for text in input.texts:
            if not text.strip():
                # Skip empty texts but include placeholder
                predictions.append(
                    PredictionOutput(
                        label="unknown",
                        confidence=0.0,
                        scores={"negative": 0.0, "positive": 0.0}
                    )
                )
                continue
            
            inputs = tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=MAX_LENGTH,
                padding=True,
            )

            with torch.no_grad():
                outputs = model(**inputs)

            probs = torch.softmax(outputs.logits, dim=-1).squeeze().tolist()

            if isinstance(probs, float):
                probs = [probs]

            predicted_class = int(torch.argmax(outputs.logits).item())
            confidence = float(max(probs))
            scores = {LABELS[i]: round(float(p), 4) for i, p in enumerate(probs)}

            predictions.append(
                PredictionOutput(
                    label=LABELS[predicted_class],
                    confidence=round(confidence, 4),
                    scores=scores,
                )
            )
        
        logger.info(f"Batch prediction completed: {len(predictions)} results")
        
        return BatchPredictionOutput(
            predictions=predictions,
            count=len(predictions)
        )
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")
