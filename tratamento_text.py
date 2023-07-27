import pandas as pd
import xlwings as xw
import time
import sqlite3
arquivo_bovespa = r"C:\Cms Tech Talks\27-07-2023 Douglas\COTAHIST_A2023.TXT"
tamanho_campos=[2,8,2,12,3,12,10,3,4,13,13,13,13,13,13,13,5,18,18,13,1,8,7,13,12,3]
start = time.time()
dados_acoes=pd.read_fwf(arquivo_bovespa, widths=tamanho_campos, header=0)
print('tempo para ler o arquivo txt', time.time() - start)
## Nomear as colunas

dados_acoes.columns = [''
"tipo_registro",
"data_pregao",
"cod_bdi",
"cod_negociacao",
"tipo_mercado",
"noma_empresa",
"especificacao_papel",
"prazo_dias_merc_termo",
"moeda_referencia",
"preco_abertura",
"preco_maximo",
"preco_minimo",
"preco_medio",
"preco_ultimo_negocio",
"preco_melhor_oferta_compra",
"preco_melhor_oferta_venda",
"numero_negocios",
"quantidade_papeis_negociados",
"volume_total_negociado",
"preco_exercicio",
"indicador_correcao_precos",
"data_vencimento" ,
"fator_cotacao",
"preco_exercicio_pontos",
"codigo_isin",
"num_distribuicao_papel"]

# Eliminar a última linha
start = time.time()
linha=len(dados_acoes["data_pregao"])
dados_acoes=dados_acoes.drop(linha-1)
print('tempo para eliminar ultima linha', time.time() - start)

# Ajustar valores com virgula (dividir os valores dessas colunas por 100)
listaVirgula=[
"preco_abertura",
"preco_maximo",
"preco_minimo",
"preco_medio",
"preco_ultimo_negocio",
"preco_melhor_oferta_compra",
"preco_melhor_oferta_venda",
"volume_total_negociado",
"preco_exercicio",
"preco_exercicio_pontos"
]
start = time.time()
for coluna in listaVirgula:
    dados_acoes[coluna]=[i/100. for i in dados_acoes[coluna]]
print('tempo para arrumar a grandeza das colunas ', time.time() - start)

print(len(dados_acoes))
print(len(list(dados_acoes['data_pregao'].unique())))
conn = sqlite3.connect("bovespa_data.db")
dados_acoes.to_sql("bovespa_data", conn, if_exists="append", index=False)


#opcoes = dados_acoes[(dados_acoes['tipo_mercado']==17)&(dados_acoes['data_pregao'] == "20210104")]

#opcoes.to_excel("opcoes2021(1).xlsx")