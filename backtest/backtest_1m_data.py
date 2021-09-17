import pyupbit
import os
import cx_Oracle as ora
import numpy as np


def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow

os.putenv('NLS_LANG', '.UTF8')
conn = ora.connect('c##upbitpy', '1234', 'localhost:1522/XE')

cursor = conn.cursor()

# 쿼리 실행
cursor.execute("""
    SELECT * FROM ELF_MIN_1
    WHERE time_idx > to_date('2021-09-16 18:32:00', 'YYYY-MM-DD HH24:MI:SS')
""")

cursor.rowfactory = makeDictFactory(cursor)
rows = cursor.fetchall()


for i, val in enumerate(rows):
    if i > 60:
        arr = np.array(rows[i-60:i])
        avg_vol = np.mean(arr)
        print(avg_vol)