import requests
import streamlit as st
from loguru import logger

logger.add('logs/sentiment_streamlit.log', rotation='500 MB', level='INFO')

def analyse_sentiment(text:str):
    request_body = {'text': text}
    response = requests.post('http://127.0.0.1:9000/analyse_sentiment', json=request_body)
    response.raise_for_status() 
    return response.json()

def analyse_compound_score(sentiment:dict[str,str]) -> str:
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
        analyse = analyse_sentiment(text)
        analyse_compound_score(analyse)