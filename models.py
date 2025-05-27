from openai import OpenAI
from prompts import PROMPT_SIS_INTERPRETADOR, PROMPT_USER_INTERPRETADOR, PROMPT_SIS_ENTENDER_CURRICULO, PROMPT_USER_ENTENDER_CURRICULO, PROMPT_SIS_ATS, PROMPT_USER_ATS, PROMPT_SIS_REFAZ_CURRICULO, PROMPT_USER_REFAZ_CURRICULO
import streamlit as st

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']


class AgenteInterpretaVaga:

    def __init__(self):
        self.__client = OpenAI(api_key = OPENAI_API_KEY)

    def interpretar_vaga(self, vaga):
        response = self.__client.chat.completions.create(
            model='gpt-4o-2024-05-13',
            messages=[
                {
                    'role': 'system',
                    'content': PROMPT_SIS_INTERPRETADOR
                },
                {
                    'role': 'user',
                    'content': PROMPT_USER_INTERPRETADOR.replace('{{vaga}}', vaga)
                }
            ]
        )
        resposta = response.choices[0].message.content
        return resposta

class AgenteInterpretaCurriculo:
    def __init__(self):
        self.__client = OpenAI(api_key = OPENAI_API_KEY)
    
    def interpretar_curriculo(self, curriculo_usuario):
        response = self.__client.chat.completions.create(
            model='gpt-4o-2024-05-13',
            messages=[
                {
                    'role': 'system',
                    'content': PROMPT_SIS_ENTENDER_CURRICULO
                },
                {
                    'role': 'user',
                    'content': PROMPT_USER_ENTENDER_CURRICULO.replace('{{curriculo}}', curriculo_usuario)
                }
            ]
        )
        resposta = response.choices[0].message.content
        return resposta


class AgenteATS:
    def __init__(self):
        self.__client = OpenAI(api_key = OPENAI_API_KEY)
    
    def ATS(self, curriculo_interpretado, vaga_interpretada):
        response = self.__client.chat.completions.create(
            model='gpt-4o-2024-05-13',
            messages=[
                {
                    'role': 'system',
                    'content': PROMPT_SIS_ATS
                },
                {
                    'role': 'user',
                    'content': PROMPT_USER_ATS.replace('{{curriculo_interpretado}}', curriculo_interpretado).replace('{{vaga}}', vaga_interpretada)
                }
            ],
            temperature=0.2
        )
        resposta = response.choices[0].message.content
        return resposta
    

class AgenteRefazCurriculo:
    def __init__(self):
        self.__client = OpenAI(api_key = OPENAI_API_KEY)
    
    def refaz_curriculo(self, curriculo_interpretado, vaga_interpretada):
        response = self.__client.chat.completions.create(
            model='gpt-4o-2024-05-13',
            messages=[
                {
                    'role': 'system',
                    'content': PROMPT_SIS_REFAZ_CURRICULO
                },
                {
                    'role': 'user',
                    'content': PROMPT_USER_REFAZ_CURRICULO.replace('{{curriculo_interpretado}}', curriculo_interpretado).replace('{{vaga}}', vaga_interpretada)
                }
            ],
            temperature=0.8
        )
        resposta = response.choices[0].message.content
        return resposta