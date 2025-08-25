from flask import request, jsonify
import os
import io
import requests
from io import BytesIO
import sys

def createVoiceVoxTTSFile(speaker, phrase, filename):
    #Audio Query to fetch data for synthesis
    vvInfo = requests.post('http://127.0.0.1:50021/audio_query?text='+ phrase +'&speaker='+ speaker)
    #Synthesis call that returns sound data
    vvBlob = requests.post('http://127.0.0.1:50021/synthesis?speaker=' + speaker + '&enable_interrogative_upspeak=true', json = vvInfo.json())
    with open(filename, 'wb') as f:
        f.write(vvBlob.content)
