import pandas as pd
import os 
import xlwings as xw
import time
path1 = r"C:\Cms Tech Talks\27-07-2023 Douglas\hist_trade"

dia = []
num_boletas_apontadas = []
num_boletas_filtro = []
premio_real = []
premio_hip =[]

a = {"dia":dia,"numero_tot_boletas":num_boletas_apontadas,"premio_hip":premio_hip,"entrada":num_boletas_filtro,"premio_real":premio_real}

for i in os.listdir(path1):
    start = time.time()
    df = pd.read_excel(os.path.join(path1,i))
    df['premio_boletas'] = df['preco_ultimo_negocio']*df['qtde']
    for j, k in df.groupby('data_boleta'):
        try:
            dia_feito = a['dia'].index(j)
            a["numero_tot_boletas"][dia_feito] += len(k)
            a["premio_hip"][dia_feito] += k.groupby('data_boleta')['premio_boletas'].sum().iloc[0]
            k = k[k['premio_total']>0.30]
            a['entrada'][dia_feito] += int(len(k)*0.05)
            a['premio_real'][dia_feito] += k.groupby('data_boleta')['premio_boletas'].sum().iloc[0]*0.05
        except:
            dia.append(j)
            num_boletas_apontadas.append(len(k))
            try:
                premio_hip.append(k.groupby('data_boleta')['premio_boletas'].sum().iloc[0])
            except:
                premio_hip.append(0)
            k = k[k['premio_total']>0.30]
            if len(k) == 0:
                
                num_boletas_filtro.append(int(len(k)*0.05))
                premio_real.append(0)
            else:
                num_boletas_filtro.append(int(len(k)*0.05))
                premio_real.append(k.groupby('data_boleta')['premio_boletas'].sum().iloc[0]*0.05)
        #print(dia,num_boletas_apontadas,num_boletas_filtro,premio_real,premio_hip)
        a = {"dia":dia,"numero_tot_boletas":num_boletas_apontadas,"premio_hip":premio_hip,"entrada":num_boletas_filtro,"premio_real":premio_real}
    print('tempo ', time.time() - start)
df_aux = pd.DataFrame(a)
print(len(df_aux))
df_aux.to_excel("Resultado_consolidado.xlsx")
