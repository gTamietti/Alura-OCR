import pytesseract
import numpy as np
import cv2 
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from pytesseract import Output
import os
import re


def mostrar_imagem(img):
    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    plt.axis('off')
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

def OCR_process(img, config_tesseract):
    texto = pytesseract.image_to_string(img, lang='por', config=config_tesseract)
    return texto


projeto = '/home/gabriel/Alura-OCR/text-recognize/Imagens/Projeto'
caminho = [os.path.join(projeto, f) for f in os.listdir(projeto)]
print(caminho)

config_tesseract = "--tessdata-dir tessdata"

texto_completo = ''
nome_txt = 'resultados_ocr.txt'

for imagem in caminho:
    img = cv2.imread(imagem)
    nome_imagem = os.path.split(imagem)[-1]
    nome_divisao = '=================\n' + str(nome_imagem)
    texto_completo = texto_completo + nome_divisao + '\n'
    texto = OCR_process(img, config_tesseract)
    texto_completo = texto_completo + texto

texto_completo

arquivo_txt = open(nome_txt, 'w')
arquivo_txt.write(texto_completo + '\n')
arquivo_txt.close()
