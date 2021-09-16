import cx_Oracle as ora
import os
import pyupbit
import datetime

# 쿼리 결과를 dictionary형태로 받아오기위한 함수 오버라이딩
def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow

tickers = pyupbit.get_tickers(fiat="KRW")
os.putenv('NLS_LANG', '.UTF8')
conn = ora.connect('c##upbitpy', '1234', 'localhost:1522/XE')
cursor = conn.cursor()

###### table create code
# for item in tickers:
#     qry = """
#         CREATE TABLE "C##UPBITPY"."%s_MIN_1"
#        (	"TIME_IDX" DATE,
#         "OPEN_PRICE" NUMBER,
#         "HIGH_PRICE" NUMBER,
#         "LOW_PRICE" NUMBER,
#         "CLOSE_PRICE" NUMBER,
#         "VOLUME" NUMBER,
#          PRIMARY KEY ("TIME_IDX")
#         )
#     """ % item[4:]
#     cursor.execute(qry)
#
# conn.commit()

###### data insert code

st = datetime.datetime.now().timestamp()
print("호출 시작!!!!", datetime.datetime.now())
df = pyupbit.get_ohlcv("KRW-ELF", "minute1", 10, to="20210915")

ed = datetime.datetime.now().timestamp()
print("호출 종료!!!!", datetime.datetime.now())
print("소요시간 : ", ed - st)

for i, data in enumerate(df.values.tolist()):
    qry = "insert into elf_min_1_data values(" \
          "to_date('%s', 'YYYY-MM-DD HH24:MI:SS'),'%d','%d','%d','%d','%d')" \
          % (df.index[i], data[0], data[1], data[2], data[3], data[4])
#
#
# cursor.execute(qry)
#
# conn.commit()



#
# # 딕셔너리변환 함수 오버라이딩
# cursor.rowfactory = makeDictFactory(cursor)
#
# rows = cursor.fetchall()