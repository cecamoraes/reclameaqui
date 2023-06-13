import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

df = pd.read_csv("D:\\_streamlit\\wspython\\reclamacoesCSV.csv")
textos = df.dropna(subset=['texto'], axis=0)['texto']

print (len(textos))
print ("fim")

for texto in textos:
    i = texto.find("garantia") 
    if i != -1:
        print(texto[i:i+8])
    j = texto.find("nota fiscal") 
    if j != -1:
        print(texto[j:j+11])
         