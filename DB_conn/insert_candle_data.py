import cx_Oracle as ora
import os
import pyupbit


# 쿼리 결과를 dictionary형태로 받아오기위한 함수 오버라이딩
def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow

os.putenv('NLS_LANG', '.UTF8')
conn = ora.connect('c##upbitpy', '1234', '172.30.1.33:1522/XE')
cursor = conn.cursor()

df = pyupbit.get_ohlcv("KRW-ELF", "minute1", 10)

for i, data in enumerate(df.values.tolist()):
    qry = "insert into elf_min_1_data values('%s','%d','%d','%d','%d','%d')" % (df.index[i],data[0],data[1],data[2],data[3],data[4])
    print(qry)
    cursor.execute(qry)

#
# # 딕셔너리변환 함수 오버라이딩
# cursor.rowfactory = makeDictFactory(cursor)
#
# rows = cursor.fetchall()