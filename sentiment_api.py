from loguru import logger
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nltk.sentiment import SentimentIntensityAnalyzer

app = FastAPI()

sia = SentimentIntensityAnalyzer()

logger.add('logs/sentiment_api.log', rotation='500 MB', level='INFO')

class Text(BaseModel):
    text: str

@app.post('/analyse_sentiment')
async def analyse_sentiment(text:Text) -> dict[str, float]:
    logger.info(f'Texte à analyser : {text.text}')
    try:
        sentiment = sia.polarity_scores(text.text)
        logger.info(f"Résultats affichés : {sentiment}")

    except Exception as err:
        logger.error(f"Erreur lors de l'analyse : {err}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur interne lors de l'analyse du sentiment")

    return sentiment
