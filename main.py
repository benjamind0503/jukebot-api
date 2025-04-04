
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

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

    if r.status_code != 200:
        return "<h2>Erreur lors de la génération du mix.</h2>"

    audio_url = r.json().get("audio_url")
    if not audio_url:
        return "<h2>Mix non généré. Aucun lien reçu de Loudly.</h2>"

    return f'''
    <html>
      <head><title>Ton mix est prêt !</title></head>
      <body style="font-family:sans-serif; text-align:center; padding:50px;">
        <h1>🎧 Ton mix est prêt !</h1>
        <p>Merci pour ta commande. Voici ton mix généré automatiquement :</p>
        <audio controls style="margin-top:20px;">
          <source src="{audio_url}" type="audio/mpeg">
          Ton navigateur ne supporte pas l’audio.
        </audio>
        <p><a href="{audio_url}" download style="display:block; margin-top:20px;">📥 Télécharger le mix</a></p>
        <p style="margin-top:40px;">Développé par BDS Events avec JukeBot</p>
      </body>
    </html>
    '''
