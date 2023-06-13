import pymysql
import pandas as pd

conn = pymysql.connect(host='localhost', port=3306, user='root', password='', database='reclame_aqui')
cursor = conn.cursor()
query = 'select * from reclamacoes_moura'

results = pd.read_sql_query(query, conn)
results.to_csv("D:\\Dropbox\\_workspace\\wspython\\arquivos gerados\\reclamacoesCSV.csv", index=False, encoding='utf-8-sig')
results.to_excel("D:\\Dropbox\\_workspace\\wspython\\arquivos gerados\\reclamacoesExcel.xlsx", index=False, encoding='utf-8-sig')
