from flask import request, jsonify
import os
import io
from openai import OpenAI
import requests
from io import BytesIO
import sys
from dotenv import load_dotenv

load_dotenv()
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY") 

def createVoiceVoxTTSFile(speaker, phrase, filename):
    #Audio Query to fetch data for synthesis
    vvInfo = requests.post('http://127.0.0.1:50021/audio_query?text='+ phrase +'&speaker='+ speaker)
    #Synthesis call that returns sound data
    vvBlob = requests.post('http://127.0.0.1:50021/synthesis?speaker=' + speaker + '&enable_interrogative_upspeak=true', json = vvInfo.json())
    with open(filename, 'wb') as f:
        f.write(vvBlob.content)

def openAiApiCall(messages):
    client = OpenAI(
        api_key=OPENAI_APIKEY,
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-turbo",
    )
    reply = chat_completion.choices[0].message.content 
    return reply