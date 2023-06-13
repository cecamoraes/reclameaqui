import pandas as pd
import sqlalchemy

#df = pd.read_csv('D:\\_streamlit\\wspython\\arquivos gerados\\reclamacoesCSV.csv')
df = pd.read_excel('D:\\_streamlit\\wspython\\arquivos gerados\\reclamacoesExcel.xlsx')
df.drop(columns='idtabela')

from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                              db="reclame_aqui"))
df = engine.execute('select * from reclamacoes_moura')

df.to_sql('reclamacoes_moura', con = engine, if_exists = 'append', chunksize = 1000, index=False)