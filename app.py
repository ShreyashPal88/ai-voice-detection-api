from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import base64

app = FastAPI(
    title="AI Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or Human",
    version="0.1.0"
)

# =====================
# API KEY CONFIG
# =====================
API_KEY = "HCL_GUVI_2026_KEY"
API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# =====================
# REQUEST / RESPONSE MODELS
# =====================
class AudioRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str

class AudioResponse(BaseModel):
    result: str
    confidence: float

# =====================
# ENDPOINT
# =====================
@app.post("/detect", response_model=AudioResponse, dependencies=[Depends(verify_api_key)])
def detect_voice(data: AudioRequest):
    # Dummy logic (hackathon-safe)
    try:
        base64.b64decode(data.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    return {
        "result": "HUMAN",
        "confidence": 1.0
    }


