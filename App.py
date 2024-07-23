import pytesseract
import numpy as np
import cv2 
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
from pytesseract import Output
import os
import re


def escreve_texto(texto, x, y, img, fonte, tamanho_texto=32):
    fonte = ImageFont.truetype(fonte, tamanho_texto)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x,y - tamanho_texto), texto, font=fonte)
    img = np.array(img_pil)
    return img 

def caixa_texto(result, img, color = (255, 100, 0)):
    x = result['left'][i]
    y = result['top'][i]
    w = result['width'][i]
    h = result['height'][i]
    cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
    return x, y, img


img = cv2.imread('/home/gabriel/Alura-OCR/text-recognize/Imagens/Aula4-caneca2.jpg')
plt.imshow(img)

config_tesseract = '--tessdata-dir tessdata --psm 6'
min_confidence = 40
fonte = '/home/gabriel/Alura-OCR/text-recognize/Imagens/calibri.ttf'

result = pytesseract.image_to_data(img, lang='por', config=config_tesseract, output_type=Output.DICT)
result
img_copy = img.copy()

for i in range(0, len(result['text'])):
    confidence = int(result['conf'][i])
    if confidence > min_confidence:
        x, y , img = caixa_texto(result, img_copy)
        text = result['text'][i]
        img_copy = escreve_texto(text, x, y, img_copy, fonte)
    plt.imshow(img_copy)


# os.makedirs('images_tesseract', exist_ok=True)
# img = cv2.imread('/home/gabriel/Alura-OCR/text-recognize/Atividades/Aula4_cotacao.png')
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# fonte = '/home/gabriel/Alura-OCR/text-recognize/Imagens/calibri.ttf'
# config_tesseract = '--tessdata-dir tessdata'
# result = pytesseract.image_to_data(img_rgb, config=config_tesseract, lang='por', output_type=Output.DICT)
# result

# padrao_data = '^[0-2][0-3]:[0-5][0-9]$'

# # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # result = pytesseract.image_to_data(img_rgb,config=config_tesseract, lang='por', output_type=Output.DICT)
# # result
# plt.imshow(img_rgb)

# min_confidence = 40
# img_copy = img_rgb.copy()
# logo_tesseract = '/home/gabriel/Alura-OCR/text-recognize/Atividades/Aula4_cotacao.png'
# data = []

# for i in range(len(result['text'])):
#     confidence = int(result['conf'][i])
#     if confidence > min_confidence:
#         text = result['text'][i]
#         if re.match(padrao_data, text):
#             x, y, img = caixa_texto(result, img_copy, color=(0,0,255))    
#             # cv2.putText(img_copy, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,100,255))
#             img_copy = escreve_texto(text, x, y, img_copy, fonte, 12)
#             data.append(text)
#         else:
#             x, y, img_copy = caixa_texto(result, img_copy)
# data

# plt.imshow(img_copy)
# cv2.imwrite(logo_tesseract, img_copy)