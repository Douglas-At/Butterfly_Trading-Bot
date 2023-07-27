import pandas as pd
import os 
import xlwings as xw


path1 = r"C:\Cms Tech Talks\27-07-2023 Douglas\hist_trade"

for i in os.listdir(path1):
    df = pd.read_excel(os.path.join(path1,i))
    
    df = df[df['Strike'] < 1000]
    df.to_excel(os.path.join(path1,i), index=False)
    