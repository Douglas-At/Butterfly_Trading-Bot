import pandas as pd 
import xlwings as xw
import matplotlib.pyplot as plt

df = pd.read_excel("Resultado_consolidado.xlsx")

df["dia"] = df["dia"].astype(str)
df["ano"] = df["dia"].str[:4]
df["mes"] = df["dia"].str[4:6]
df["dia_dia"] = df["dia"].str[6:]
df['premio_hip'] = -df['premio_hip']
df['premio_real'] = -df['premio_real']
df = df.sort_values(by=["ano", "mes", "dia_dia"], ascending=[True, True, True])
df = df[:50]
fig, ax1 = plt.subplots()

ax1.bar(df["dia"], df["numero_tot_boletas"], color="blue", alpha=0.6, label="Total Boletas")
#ax1.bar(df["dia"], df["entrada"], color="green", alpha=0.6, label="Entrada")


ax1.set_ylabel("Total Boletas & Entrada")
ax1.set_xlabel("Dia")

#entradas 

premio = df['premio_hip'].sum()
premio = format(premio, ",.0f").replace(",", ".")
#ax1.set_title("Numero de boletas Entrada {} vs. Premio Embolsado {}".format(df['entrada'].sum(),premio))
ax1.set_title("Numero de boletas apontadas {} vs. Premio hipotetico {}".format(df['numero_tot_boletas'].sum(),premio))
#total

ax2 = ax1.twinx()


ax2.plot(df["dia"], df["premio_hip"], marker="o", color="red", label="Premio Hip")
#ax2.plot(df["dia"], df["premio_real"], marker="o", color="orange", label="Premio Real")


ax2.set_ylabel("Premio Hipotetico")
#ax2.set_ylabel("Premio Real")


ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# Show the plot
plt.show()