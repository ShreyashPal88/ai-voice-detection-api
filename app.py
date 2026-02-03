from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Literal
import base64
import binascii
import os

app = FastAPI(
    title="AI Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or Human",
    version="0.1.0"
)

# Read API key from Railway environment
API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="x-api-key",
    auto_error=False
)

class AudioRequest(BaseModel):
    language: Literal["en", "hi"]
    audio_format: Literal["wav", "mp3"]
    audio_base64: str

class AudioResponse(BaseModel):
    result: str
    confidence: float

@app.post("/detect", response_model=AudioResponse)
def detect_voice(
    data: AudioRequest,
    x_api_key: str = Depends(api_key_header)
):
    if API_KEY is None:
        raise HTTPException(
            status_code=500,
            detail="API key not configured"
        )

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    # Validate base64 audio
    try:
        base64.b64decode(data.audio_base64, validate=True)
    except binascii.Error:
        raise HTTPException(
            status_code=422,
            detail="Invalid base64 audio data"
        )

    # Dummy detection logic (ML-ready)
    result = "Human" if data.audio_format == "wav" else "AI-generated"

    return {
        "result": result,
        "confidence": 0.87
    }





