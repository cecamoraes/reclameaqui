
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap 
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from nltk.corpus import stopwords


df = pd.read_csv("D:\\_streamlit\\wspython\\reclamacoesCSV.csv")
df = pd.DataFrame(df)
#print(df.head())

words = df['texto']
#print(words)

all_words = " ".join(w for w in words)
#print(all_words)
#stopwords = set(STOPWORDS)
stopwords = set(stopwords.words('portuguese'))
#print(stopwords)

wc = WordCloud(stopwords=stopwords,
               background_color='white',
               width=1600,
               height=800).generate(all_words)

fig, ax = plt.subplots(figsize =(14,7))
ax.imshow(wc,interpolation='bilinear')
ax.set_axis_off()
plt.imshow(wc)





