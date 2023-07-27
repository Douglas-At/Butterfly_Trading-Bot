import time 
import pandas as pd
import os 
import sqlite3

def column_reader(db,table):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Specify the name of the table
    table_name = table

    # Fetch the table schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()

    # Extract the column names
    column_names = [row[1] for row in rows]

    # Print the column names
    for column_name in column_names:
        print(column_name)

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

def verify_tables(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = cursor.fetchall()
    for name in table_names:
        print(name[0])
    conn.close()

def extract_call_dates(start_date,end_date):
    conn = sqlite3.connect("bovespa_data.db")
    cursor = conn.cursor()
    date_range = pd.date_range(start=start_date, end=end_date)
    dates_to_query = [date.strftime('%Y%m%d') for date in date_range]

    start1 = time.time()
    not_d =[]
    for data in dates_to_query:
        query = f''' SELECT * FROM bovespa_data WHERE tipo_mercado=70 AND data_pregao="{data}" '''
        start = time.time()
        data_extract = pd.read_sql(query, conn)
        print('tempo para query de um dia ', time.time() - start, "dia: ", data)
        if len(data_extract)    != 0:
            data_extract.to_excel(r"C:\Cms Tech Talks\27-07-2023 Douglas\day\{}_call.xlsx".format(data))
        else:
            print("Não teve pregão nesse dia ", data)
            not_d.append(data)


    a = {"dias_off":not_d}
    df_aux =pd.DataFrame(a)
    df_aux.to_excel("dias_off.xlsx")

    print('tempo para query de um dia ', time.time() - start1)

#verify_tables("bovespa_data.db")
#column_reader("bovespa_data.db","bovespa_data")
#extract_call_dates("20210104","20231231")

