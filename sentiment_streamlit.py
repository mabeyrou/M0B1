import requests
import streamlit as st
from loguru import logger

API_URL = 'http://127.0.0.1:9000'

logger.add('logs/sentiment_streamlit.log', rotation='500 MB', level='INFO')

def analyse_sentiment(text:str):
    response = requests.post(f'{API_URL}/analyse_sentiment', json={'text': text})
    response.raise_for_status() 
    return response.json()

def analyse_compound_score(sentiment:dict[str,float]) -> str:  # Changed type hint for sentiment
    result = ''
    if sentiment['compound'] >= 0.05 :
        result = "Sentiment global : Positif 😀"
    elif sentiment['compound'] <= -0.05 :
        result = "Sentiment global : Négatif 🙁"
    else :
        result = "Sentiment global : Neutre 😐"
    st.write(result)
    logger.info(f"Résultats affichés: {result}")

with st.form('analyse_sentiment_form'):
    st.header('Analyse de sentiment')
    text = st.text_area(label='Taper le texte à analyser:')
    submitted = st.form_submit_button(label="Analyser")
    if submitted:
        if not text:
            st.write("Veuillez entrer du texte pour l'analyse.")
        else:
            logger.info(f"Texte à analyser: {text}")
            try:
                response = analyse_sentiment(text)
                analyse_compound_score(response)
            except requests.exceptions.HTTPError as http_err:
                error_message = f"Erreur HTTP {http_err.response.status_code}"
                try:
                    error_detail = http_err.response.json().get("detail", "Erreur inconnue")
                    error_message += f": {error_detail}"
                except (ValueError, KeyError):
                    pass
                st.error(error_message)
                logger.error(f"Erreur HTTP: {http_err}")
            except requests.exceptions.RequestException as err:
                st.error(f"Erreur de connexion à l'API : {err}")
                logger.error(f"Erreur de connexion à l'API : {err}")
            except Exception as err :
                st.error(f"Une erreur inattendue est survenue: {err}")
                logger.error(f"Une erreur inattendue est survenue: {err}")
