import os

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.services.analyseur_clignements import AnalyseurClignements
from app.services.analyseur_levres import AnalyseurLevres
from app.services.calculateur_score import CalculateurScore


app = FastAPI(title="Sentinelle Numerique - Deepfake Video")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def accueil():
    return {
        "message": "API de detection deepfake video active"
    }


@app.post("/analyser-video")
async def analyser_video(video: UploadFile = File(...)):
    dossier_temporaire = "videos_temporaires"
    os.makedirs(dossier_temporaire, exist_ok=True)

    chemin_video = os.path.join(dossier_temporaire, video.filename)

    contenu = await video.read()

    with open(chemin_video, "wb") as fichier:
        fichier.write(contenu)

    analyseur_yeux = AnalyseurClignements()
    analyseur_levres = AnalyseurLevres()
    calculateur_score = CalculateurScore()

    score_yeux = analyseur_yeux.analyser(chemin_video)
    score_levres = analyseur_levres.analyser(chemin_video)

    resultat = calculateur_score.calculer(score_yeux, score_levres)

    os.remove(chemin_video)

    return resultat