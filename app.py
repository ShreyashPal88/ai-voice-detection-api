from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, Field
import base64
import os

# --------------------
# App config
# --------------------
app = FastAPI(
    title="AI Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or Human",
    version="1.0.0"
)

# --------------------
# API Key setup
# --------------------
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="x-api-key",
    auto_error=False
)

# --------------------
# Request / Response Models
# --------------------
class AudioRequest(BaseModel):
    language: str
    audio_format: str = Field(..., alias="audioFormat")
    audio_base64: str = Field(..., alias="audioBase64")

    class Config:
        populate_by_name = True  # accept snake_case + camelCase


class AudioResponse(BaseModel):
    result: str
    confidence: float


# --------------------
# Endpoint
# --------------------
@app.post("/detect", response_model=AudioResponse)
def detect_voice(
    data: AudioRequest,
    x_api_key: str = Depends(api_key_header)
):
    # API key not set on server
    if API_KEY is None:
        raise HTTPException(
            status_code=500,
            detail="API key not configured"
        )

    # Invalid API key
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    # Validate base64 audio
    try:
        base64.b64decode(data.audio_base64)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid base64 audio data"
        )

    # Dummy inference (replace with ML later)
    return {
        "result": "Human",
        "confidence": 0.87
    }






