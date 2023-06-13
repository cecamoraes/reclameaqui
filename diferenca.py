import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import sqlalchemy
import pymysql
from time import sleep
from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="reclame_aqui"))
con = engine.connect()

consulta_sql = text("SELECT max(identificador) FROM reclamacoes_moura")
result = con.execute(consulta_sql)
ultimoid = int(result.first()[0])

cabecalho = {'user-agent':'Mozilla/5.0'}

urlbase = 'https://www.reclameaqui.com.br/empresa/baterias-moura/lista-reclamacoes/?pagina=1'

headers = requests.utils.default_headers()

headers.update({'User-Agent': 'My User Agent 1.0',})

resposta = requests.get(urlbase,headers=headers)
pagina_macarronica = resposta.text
pagina_bonita = BeautifulSoup(pagina_macarronica, 'html.parser')
textoquantidade = pagina_bonita.find("h1", {"class": "wydd4i-6 cLqHyR"})

qtdtext = textoquantidade.text[56:60]
temp = int(qtdtext)/10
paginas = int(round(temp,0))+1

lista_reclamacoes = []

for i in range(1,paginas):
    
    
    urlbase = 'https://www.reclameaqui.com.br/empresa/baterias-moura/lista-reclamacoes?pagina='+str(i)
    
    sleep(1.0)
    resposta = requests.get(urlbase,headers=headers)

    pagina_macarronica = resposta.text

    pagina_bonita = BeautifulSoup(pagina_macarronica, 'html.parser')

    lista_links = []
    
    lista_div = pagina_bonita.find_all("div", {"class": "sc-1pe7b5t-0 bJdtis"})
    for div in lista_div: 
        lista_links.append(div.find('a').attrs['href'])

    urlbasereclamacao = 'https://www.reclameaqui.com.br'
    for reclamacao in lista_links:
        urlreclamacao = urlbasereclamacao + reclamacao
        sleep(10)
        respostareclamacao = requests.get(urlreclamacao,headers=headers)
        reclamacao_macarronica = respostareclamacao.text
        reclamacao_bonita = BeautifulSoup(reclamacao_macarronica, 'html.parser')

        identificador = reclamacao_bonita.find('span', {'data-testid':'complaint-id'})

        if identificador is None: 
            idtupla = ''
        else:
            idtupla = identificador.text[4:]

        if int(idtupla) <= ultimoid:
            break

        titulo = reclamacao_bonita.find('h1', {'data-testid':'complaint-title'})
        if titulo is None: 
            titulotupla = ''
        else:
            titulotupla = titulo.text
        
        local = reclamacao_bonita.find('span', {'data-testid':'complaint-location'})
        if local is None: 
            localtupla = ''
        else:
            localtupla = local.text

        data = reclamacao_bonita.find('span', {'data-testid':'complaint-creation-date'})
        if data is None: 
            datatupla = ''
        else:
            #datatupla = data.text
            datatupla = data.text[6:10] + '-' + data.text[3:5] + '-' + data.text[0:2] + ' ' + data.text[14:19] + ':00'

        texto = reclamacao_bonita.find('p', {'data-testid':'complaint-description'})
        if texto is None: 
            textotupla = ''
        else:
            textotupla = texto.text

        status = reclamacao_bonita.find('div', {'data-testid':'complaint-status'})
        if status is None: 
            statustupla = ''
        else:
            statustupla = status.text

        resposta = reclamacao_bonita.find('p', {'class':'sc-1o3atjt-4 JkSWX'})
        if resposta is None:
            respostatupla = ''
        else:
            respostatupla = resposta.text
        
        tupla = (idtupla, titulotupla, datatupla, localtupla, statustupla, textotupla, respostatupla, i)
        lista_reclamacoes.append(tupla)

    if int(idtupla) <= ultimoid:
        break    

print(len(lista_reclamacoes))   

#df.sort_values(by=['identificador'])
#df.drop_duplicates()
#print(df)
#df.to_excel("D:\\_streamlit\\wspython\\arquivos gerados\\diferencaExcel.xlsx") 
#df.to_csv("D:\\_streamlit\\wspython\\arquivos gerados\\diferencaCSV.csv")

if len(lista_reclamacoes) > 0:
    df = pd.DataFrame(lista_reclamacoes, columns=['idtabela', 'identificador', 'titulo', 'datahora', 'local', 'status', 'texto', 'resposta', 'pagina'])
    
    dfcsv = pd.read_csv('D:\\Dropbox\\_workspace\\wspython\\arquivos gerados\\reclamacoesCSV.csv',  on_bad_lines='skip')
    dfexcel  = pd.read_excel('D:\\Dropbox\\_workspace\\wspython\\arquivos gerados\\reclamacoesExcel.xlsx')
    df3 = pd.concat([df,dfcsv])
    df3.to_csv("D:\\Dropbox\\_workspace\\wspython\\arquivos gerados\\reclamacoesCSV.csv")
    df4 = pd.concat([df,dfexcel])
    df4.to_excel("D:\\Dropbox\\_workspace\\wspython\\arquivos gerados\\reclamacoesExcel.xlsx") 

    #df.to_sql('diferenca', con = engine, if_exists = 'append', chunksize = 1000, index=False)
    df.to_sql('reclamacoes_moura', con = engine, if_exists = 'append', chunksize = 1000, index=False)
print("The End") 
    

