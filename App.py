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

# for imagem in caminho:
#     img = cv2.imread(imagem)
#     nome_imagem = os.path.split(imagem)[-1]
#     nome_divisao = '=================\n' + str(nome_imagem)
#     texto_completo = texto_completo + nome_divisao + '\n'
#     texto = OCR_process(img, config_tesseract)
#     texto_completo = texto_completo + texto

# texto_completo

# arquivo_txt = open(nome_txt, 'w')
# arquivo_txt.write(texto_completo + '\n')
# arquivo_txt.close()

termo_pesquisa = 'ambiente'

# for imagem in caminho:
#     img = cv2.imread(imagem)
#     img_original = img.copy()
#     nome_imagem=os.path.split(imagem)[-1]
#     print('==============\n' + str(nome_imagem))

#     texto = OCR_process(imagem, config_tesseract)
#     ocorrencias = [i.start() for i in re.finditer(termo_pesquisa, texto)]
#     print('Número de ocorrencias para o termo: {}: {}'.format(termo_pesquisa, len(ocorrencias)))
#     print('\n')

fonte_dir = '/home/gabriel/Alura-OCR/text-recognize/Imagens/calibri.ttf'

def escreve_texto(texto, x, y, img, fonte, color=(50,50,255), tamanho=16):
    fonte = ImageFont.truetype(fonte_dir, tamanho)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y-tamanho), texto, font=fonte, fill=color)
    img = np.array(img_pil)
    return img

def caixa_texo(i, resultado, img, cor=(255,100,0)):
    x = resultado['left'][i]
    y = resultado['top'][i]
    w = resultado['width'][i]
    h = resultado['height'][i]

    cv2.rectangle(img, (x,y), (x + w, y + h), cor, 2)

    return x, y, img

min_conf = 30

def OCR_processa_imagem(img, termo_pesquisa, config_tesseract, min_conf):
    resultado = pytesseract.image_to_data(img, config=config_tesseract, lang='por', output_type=Output.DICT)
    num_ocorrencias = 0
    for i in range(0, len(resultado['text'])):
        confianca = int(resultado['conf'][i])
        if confianca > min_conf:
            texto = resultado['text'][i]
            if termo_pesquisa in texto.lower():
                x, y, img = caixa_texo(i, resultado, img,(0,0,255))
                img = escreve_texto(texto,x,y,img,fonte_dir,(50,50,225), 14)

                num_ocorrencias += 1
    return img, num_ocorrencias

os.makedirs('images_project', exist_ok=True)

termo_pesquisa = 'learning'

for imagem in caminho:
    img = cv2.imread(imagem)
    img_original = img.copy()
    nome_imagem=os.path.split(imagem)[-1]
    img, numero_ocorrencias = OCR_processa_imagem(img, termo_pesquisa, config_tesseract, min_conf)
    if numero_ocorrencias > 0:
        mostrar_imagem(img)
        novo_nome_img = 'OCR_' + nome_imagem
        nova_img = 'images_project/' + str(novo_nome_img)
        cv2.imwrite(nova_img, img)
