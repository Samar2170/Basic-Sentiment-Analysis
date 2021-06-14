import pandas as pd 
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="tweets",
    user="jarvis",
    password="tests@654",
)
cur = conn.cursor()

df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE '%nifty%' ORDER BY unix DESC LIMIT 1000", conn)
print(df.tail())