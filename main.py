
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOUDLY_API_KEY = "pmdd6s8-I7Y-mfVbSQGHCIoBV1ikiu-Rsv2OkYdhsso"

@app.post("/generate-mix", response_class=HTMLResponse)
async def generate_mix(
    email: str = Form(...),
    style: str = Form(...),
    occasion: str = Form(...),
    transition: str = Form(...),
    artistes: str = Form(""),
    exclusions: str = Form(""),
    duree: int = Form(...)
):
    mood = "energetic" if transition in ["cut", "drop", "mix"] else "chill"

    headers = {"Authorization": f"Bearer {LOUDLY_API_KEY}", "Content-Type": "application/json"}
    data = {"style": style, "mood": mood, "duration": duree * 60}

    r = requests.post("https://b2b-soundtracks-swagger-dev.loudly.com/api/v1/generate", headers=headers, json=data)

    debug_response = r.text

    return f'''
    <html>
      <head><title>DEBUG JukeBot</title></head>
      <body style="font-family:monospace; padding:30px;">
        <h1>Réponse brute de l'API Loudly :</h1>
        <pre>{debug_response}</pre>
        <hr>
        <p>Si tu ne vois pas de "audio_url" ici, c'est que la génération ne fonctionne pas.</p>
      </body>
    </html>
    '''
