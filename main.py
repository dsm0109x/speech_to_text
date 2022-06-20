#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Subitus
Convierte todos los audios de la carpeta ./ARCHIVOS a un CSV con el texto respectivo a cada audio
03/02/22
'''

import pandas as pd 
import speech_recognition as sr
import os.path
from thefuzz import fuzz
import sys
import difflib
import csv
import os
from pydub import AudioSegment
import shutil

print('speech_to_text')
print('iniciando el programa...')

if getattr(sys, 'frozen', False):
    BASE_DIR = sys.executable[:-5]
else:
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Ruta de los archivos fuente
PATH_FILES = '{}/ARCHIVOS/'.format(BASE_DIR)
# Ruta de salida de resultados
PATH_OUTPUT = '{}/SALIDA/'.format(BASE_DIR)
# Formatos aceptados
ACCEPTED_FORMATS = ['wav', 'mp3', 'aif', 'aiff']

print('ruta de los archivos fuentes: {}'.format(PATH_FILES))
print('ruta de los resultados: {}'.format(PATH_OUTPUT))

# Verifica si existe la carpeta de salida sino la crea
if(not os.path.exists('{}'.format(PATH_OUTPUT))):
    os.mkdir(PATH_OUTPUT)
else:
    shutil.rmtree(PATH_OUTPUT)
    os.mkdir(PATH_OUTPUT)

# Se inicializa el reconocimiento de voz
r = sr.Recognizer()

FORMAT_AUDIO = ''
csv_file_content = []

#se revisa la extensión de los archivos de audio
list_extensions = os.listdir(PATH_FILES)
#se eliminan los archivos ocultos
list_extensions = [file.split('.')[-1] for file in list_extensions if not file[0] == '.']
list_extensions = list(set(list_extensions))
list_extensions = list(filter(lambda x: x != 'csv', list_extensions))
if len(list_extensions) > 1:
    print('Existen archivos de varias extensiones:')
    print(list_extensions)
    print('Favor de homologar los audios')
    sys.exit(0)
else:
    FORMAT_AUDIO = list_extensions[0]
    if FORMAT_AUDIO not in ACCEPTED_FORMATS:
        print('El programa no soporta ese formato de audio: {}'.format(FORMAT_AUDIO))
        print('Los formatos aceptados son: {}'.format(ACCEPTED_FORMATS))
        sys.exit(0)


files = os.listdir(PATH_FILES)
for file in files:
    if file[0] != '.':
        print(file)
        info_csv = []
        if FORMAT_AUDIO == 'mp3':
            sound = AudioSegment.from_mp3("{}{}.mp3".format(PATH_FILES,file.split('.')[0]))
            sound.export("{}{}.wav".format(PATH_FILES,file.split('.')[0]), format="wav")
        if FORMAT_AUDIO == 'aif' or FORMAT_AUDIO == 'aiff':
            sound = AudioSegment.from_file("{}{}.{}".format(PATH_FILES,file.split('.')[0], FORMAT_AUDIO))
            sound.export("{}{}.wav".format(PATH_FILES,file.split('.')[0]), format="wav")
        path_audio = '{}{}.wav'.format(PATH_FILES,file.split('.')[0])
        info_csv.append(path_audio)
        print('Buscando el audio: {}'.format(path_audio))  
        if(os.path.exists('{}'.format(path_audio))):
            print('Analizando el audio...\n\n')
            try: 
                with sr.AudioFile(path_audio) as source:
                    audio = r.record(source)
                    text = r.recognize_google(audio, language='es-MX')
                info_csv.append(text)
            except Exception as e:
                print('Error el cargar el audio: {}'.format(e))
        else:
            print('No existe el archivo')
            info_csv.append('No existe el archivo!')
        csv_file_content.append(info_csv)
        print('=======')

with open('{}relacion.csv'.format(PATH_OUTPUT), mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Audio','Texto'])
    for row in csv_file_content:
        csv_writer.writerow(row)

#borrar archivos que se crearon el file path
if FORMAT_AUDIO != 'wav':
    lista_archivos = os.listdir(PATH_FILES)
    lista_archivos = list(filter(lambda x: x.split('.')[-1] == 'wav', lista_archivos))
    for archivo in lista_archivos:
        print('borrando archivo: {}{}'.format(PATH_FILES,archivo))
        os.remove('{}{}'.format(PATH_FILES,archivo))
