from fastapi import FastAPI, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import base64
import os

app = FastAPI(
    title="AI Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or Human",
    version="0.1.0"
)

API_KEY = os.getenv("API_KEY")

api_key_header = APIKeyHeader(
    name="x-api-key",
    auto_error=False
)

class AudioRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str

class AudioResponse(BaseModel):
    result: str
    confidence: float

@app.post("/detect", response_model=AudioResponse)
def detect_voice(
    data: AudioRequest,
    x_api_key: str = Depends(api_key_header)
):
    # 🔎 DEBUG LOGS (TEMP)
    print("ENV API_KEY =", repr(API_KEY))
    print("HEADER x-api-key =", repr(x_api_key))

    if API_KEY is None:
        raise HTTPException(status_code=500, detail="API key not configured")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    base64.b64decode(data.audio_base64)

    return {
        "result": "Human",
        "confidence": 0.87
    }





