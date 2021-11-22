import cx_Oracle as ora
import os
import pyupbit
from datetime import datetime

# 쿼리 결과를 dictionary형태로 받아오기위한 함수 오버라이딩
def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow


# KRW 전체 종목 정보 받아오기
tickers = pyupbit.get_tickers(fiat="KRW")
os.putenv('NLS_LANG', '.UTF8')

# DB Connection
conn = ora.connect('c##upbitpy', '1234', 'localhost:1522/XE')
cursor = conn.cursor()


# 현재 DB계정의 테이블리스트 조회
# sel_qry = "select tname from tab"
# cursor.execute(sel_qry)
# cursor.rowfactory = makeDictFactory(cursor)
# table_list = cursor.fetchall()
#
# for ticker in tickers:
#     exist = 0
#     for table in table_list:
#         table = table["TNAME"]
#         if table.split("_")[0] == ticker[4:]:
#             exist = 1
#             break
#
#     # 받아온 종목 중 현재 테이블이 생성 안 된 종목이 있으면 생성
#     if exist != 1:
#         create_qry = """
#             CREATE TABLE "C##UPBITPY"."%s_MIN_1"
#            (	"TIME_IDX" DATE,
#             "OPEN_PRICE" NUMBER,
#             "HIGH_PRICE" NUMBER,
#             "LOW_PRICE" NUMBER,
#             "CLOSE_PRICE" NUMBER,
#             "VOLUME" NUMBER,
#              PRIMARY KEY ("TIME_IDX")
#             )
#         """ % ticker[4:]
#         cursor.execute(create_qry)
#
# conn.commit()


######  DB의 마지막 시간과 현재 시간까지의 차이를 구해 차이만큼의 분봉 데이터 받아오기
qry = "SELECT max(time_idx) lt FROM LOOM_MIN_1"
cursor.execute(qry)
cursor.rowfactory = makeDictFactory(cursor)
last_row = cursor.fetchall()
last_date = last_row[0]['LT']

# 현재시간과의 차이 구하기
now = datetime.now()
diff = now - last_date
diff_min = int(diff.seconds / 60)

# 차이만큼의 분봉데이터 받아오기
df = pyupbit.get_ohlcv("KRW-LOOM", "minute1", diff_min)

# 차이만큼의 과거 데이터 삭제
qry = "DELETE FROM LOOM_MIN_1 " \
        "WHERE TIME_IDX in (" \
        "	SELECT TIME_IDX FROM LOOM_MIN_1" \
        "	WHERE rownum <= %d)" % diff_min

cursor.execute(qry)
conn.commit()

# 삭제된만큼 새로 받아온 데이터 추가하기
for i, data in enumerate(df.values.tolist()):
    qry = "insert into loom_min_1 values(" \
          "to_date('%s', 'YYYY-MM-DD HH24:MI:SS'),'%d','%d','%d','%d','%d')" \
          % (df.index[i], data[0], data[1], data[2], data[3], data[4])
    cursor.execute(qry)
    if i % 1000 == 0:
        print("%d rows insert complete..." % i)

conn.commit()




###### data insert code
# st = datetime.datetime.now().timestamp()
# print("호출 시작!!!!", datetime.datetime.now())
# # df = pyupbit.get_ohlcv("KRW-ELF", "minute1", 1000, to="20210915")
# df = pyupbit.get_ohlcv("KRW-LOOM", "minute1", 4320)
#
# ed = datetime.datetime.now().timestamp()
# print("호출 종료!!!!", datetime.datetime.now())
# print("소요시간 : ", ed - st)
#
# for i, data in enumerate(df.values.tolist()):
#     qry = "insert into loom_min_1 values(" \
#           "to_date('%s', 'YYYY-MM-DD HH24:MI:SS'),'%d','%d','%d','%d','%d')" \
#           % (df.index[i], data[0], data[1], data[2], data[3], data[4])
#     cursor.execute(qry)
#     if i % 1000 == 0:
#         print("%d rows insert complete..." % i)
#
# conn.commit()

#
# # 딕셔너리변환 함수 오버라이딩
# cursor.rowfactory = makeDictFactory(cursor)
#
# rows = cursor.fetchall()