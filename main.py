import streamlit as st
import requests
from bs4 import BeautifulSoup
from models import AgenteInterpretaVaga, AgenteInterpretaCurriculo, AgenteATS, AgenteRefazCurriculo
import PyPDF2
from ferramentas import ler_texto_pdf
from time import sleep


seletor_vaga = st.radio('Selecione o tipo de vaga preenchida', options=['Link', 'Texto'], index = 0)

agente = AgenteInterpretaVaga()
agente_ats = AgenteATS()

if seletor_vaga == 'Texto':
    texto_vaga = st.text_input('Digite os dados da vaga')
    if texto_vaga:
        vaga = agente.interpretar_vaga(texto_vaga)
        st.session_state['vaga'] = vaga

elif seletor_vaga == 'Link':
    link_vaga = st.text_input('Digite o link da vaga')

    if link_vaga:
        r = requests.get(link_vaga)
        r = BeautifulSoup(r.text, 'html.parser')
        r = str(r)
        
        vaga = agente.interpretar_vaga(r)
        st.session_state['vaga'] = vaga




seletor_curriculo = st.radio('Selecione o tipo de currículo', options=['Link', 'Texto', 'PDF'], index = 0)

if seletor_curriculo:

    if seletor_curriculo == 'PDF':
        curriculo_pdf = st.file_uploader('Envie um arquivo PDF')
        curriculo_upload = ler_texto_pdf(curriculo_pdf)

    elif seletor_curriculo == 'Texto':
        curriculo_upload = st.text_input('Digite o Texto do seu currículo')

    elif seletor_curriculo == 'Link':
        link_curriculo = st.text_input('Digite o link do seu currículo online')
        
        if link_curriculo:
            r = requests.get(link_curriculo)
            r = BeautifulSoup(r.text, 'html.parser')
            curriculo_upload = str(r)


    if curriculo_upload:
        agente = AgenteInterpretaCurriculo()
        curriculo = agente.interpretar_curriculo(curriculo_upload)
        st.session_state['curriculo'] = curriculo
            
with st.expander('Interpretação Vaga'):
    st.write(vaga)

with st.expander('Interpretação Currículo'):
    st.write(curriculo)


avaliar = st.button('Avaliar candidato')
if avaliar:
    if curriculo and vaga:
        nota_ats = agente_ats.ATS(st.session_state['curriculo'], st.session_state['vaga'])

        st.markdown(f'## Nota do currículo: {nota_ats}')
        st.session_state['nota_ats'] = nota_ats


refazer_curriculo = st.button('Refazer currículo')
if refazer_curriculo:
    if curriculo and vaga:
        agente_refaz_curriculo = AgenteRefazCurriculo()
        curriculo_novo = agente_refaz_curriculo.refaz_curriculo(st.session_state['curriculo'], st.session_state['vaga'])
        st.session_state['curriculo_novo'] = curriculo_novo

        if curriculo_novo:
            nota_ats_novo = agente_ats.ATS(st.session_state['curriculo_novo'], st.session_state['vaga'])
            st.markdown(f'## Nota do currículo: {nota_ats_novo}')
            st.session_state['nota_ats_novo'] = nota_ats_novo

        with st.expander('Currículo novo'):
            st.write(st.session_state['curriculo_novo'])
