import pandas as pd
import os
import yfinance as yf
import xlwings as xw
from itertools import combinations
import time 
import numpy as np


#preciso fazer um metodo de entrda em QUALQUER opção e mensurar os meus possíveis riscos 
#ver com qnts cotas preciso entrar em cada perda levando em consideração que uma delas terei que entrar com 100 cotas 

#usar codigoisin e cod_negociação(ticker) apenas para deixar estetico 
#preço ultimo negocio (leilçao de fechamento da opção ) -INFO FALSA, pode não ter saido no leilçao 
#qtde de papeis é apenas para ter um norte se é possível a operação 
#preço exercico é o norteador para executar a operação sem ele não teriamos como calcular é meu K1
#data vencimento é o segundo criterio

"""
'data_pregao','cod_negociacao','preco_ultimo_negocio',
'quantidade_papeis_negociados','volume_total_negociado','preco_exercicio','data_vencimento','codigo_isin',
"""

#preciso aplicar as contas para verificar com assimetria e não só 1 para 2 para 1 com mesma distancia 

def pa_verify(a, b, c):
    return (c - b) == (b - a)

def butter_verify(a,b,c):
    return 2*b-(a+c)>0
def append_triple(a,b,c,lista):
    lista.append(a)
    lista.append(b)
    lista.append(c)


def search_pa(strikes, precos, tickers):
    progressions = []
    tickers_arm = []
    value =[]
    qtde =[]
    for combo in combinations(strikes, 3):
        a, b, c = combo
        if pa_verify(a, b, c):
            if butter_verify(precos[strikes.index(a)],precos[strikes.index(b)],precos[strikes.index(c)]):
                append_triple(a,b,c,progressions)
                append_triple(tickers[strikes.index(a)],tickers[strikes.index(b)],tickers[strikes.index(c)],tickers_arm)
                x = 2*precos[strikes.index(b)]-precos[strikes.index(a)]-precos[strikes.index(c)]
                append_triple(x,x,x,value)
                append_triple(100,-200,100,qtde)
    return progressions, tickers_arm,value, qtde



#nesse modelo apenas boleto TUDO nada que seja em especifico cancelado pelo operacional
os.chdir(r"C:\Cms Tech Talks\27-07-2023 Douglas\day")
y = 0
z = 0
x = 0
df_master = pd.DataFrame()
for i in os.listdir():
    df = pd.read_excel(i)
    #nessa forma to trabalhando com o mesmo ativo mesmo vencimento no mesmo fechamento 
    grouped_data = df.groupby(['codigo_isin','data_vencimento'])
    start = time.time()
    
    for ativo, group_df in grouped_data:
        if y%2000 ==0:
            df_master.to_excel("C:\\Cms Tech Talks\\27-07-2023 Douglas\\hist_trade\\teste_butterfly({}).xlsx".format(str(z)), index=False)    
            df_master = pd.DataFrame()
            z +=1
        lista_sorted,lista_ticker,value,qtde = search_pa(list(group_df.sort_values('preco_exercicio')['preco_exercicio']),list(group_df.sort_values('preco_exercicio')['preco_ultimo_negocio']),list(group_df.sort_values('preco_exercicio')['cod_negociacao']))
        a = {"cod_negociacao":lista_ticker,"Strike":lista_sorted,"premio_total":value,"qtde":qtde}
        df_aux = pd.DataFrame(a)
        df_aux['data_boleta'] = group_df['data_pregao'].to_list()[0]
        df_aux['vencimento_boleta'] = group_df['data_vencimento'].to_list()[0]
        df_aux = df_aux.merge(group_df[['cod_negociacao','preco_ultimo_negocio']], on='cod_negociacao', how="left")
        df_master = pd.concat((df_master,df_aux))
        y += 1

    df_master.to_excel("C:\\Cms Tech Talks\\27-07-2023 Douglas\\hist_trade\\teste_butterfly({}).xlsx".format(str(z)), index=False)    
    print('tempo para ver as boletas de 1 dia', time.time() - start, z,"dias contados ", x )
    x += 1

#particularidades que não estou levando em considerção 
"""
fechamento != de leilão 
devido a isso, papeis com liquidez baixa, esse preço fechamento não bate com preço leilão (descasamento)
volume de exposição por papel, isto é abrir 100 cotas de MGLU3 e mt diferente de 100 cotas de BOVA11
não coloquei um limitede minimo de liquidez opção para poder entrar
não levei em consideração corretagem 
---
Ver como analisar tudo isso para tt de opções lançar e retirar tudo simultaneamente 
---
MAs com essas falhas posso fazer os lotes determinados por exposiçao de strike minimo
e não por lote
---

"""

os.chdir(r"C:\Cms Tech Talks\27-07-2023 Douglas")
df_master.to_excel("teste_butterfly.xlsx", index=False)
