from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64

app = FastAPI(
    title="AI Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or Human",
    version="0.1.0"
)

API_KEY = "CHANGE_ME"   # 👈 use this exact value in Swagger

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
    x_api_key: str = Header(...)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Just a dummy check (replace with ML later)
    audio_bytes = base64.b64decode(data.audio_base64)

    return {
        "result": "Human",
        "confidence": 0.87
    }


