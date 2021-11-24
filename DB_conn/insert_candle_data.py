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
#         print("creating table %s_min_1..." % ticker[:4])
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
# for ticker in tickers:
#     target_table = "%s_MIN_1" % ticker[4:]
#     print("now table : ", target_table)
#     qry = "SELECT max(time_idx) lt FROM %s" % target_table
#     cursor.execute(qry)
#     cursor.rowfactory = makeDictFactory(cursor)
#     last_row = cursor.fetchall()
#     last_date = last_row[0]['LT']
#
#     # 현재시간과의 차이 구하기
#     now = datetime.now()
#     diff = now - last_date
#     diff_min = int(diff.seconds / 60)
#     # diff_min = 4320
#
#     # 차이만큼의 분봉데이터 받아오기
#     df = pyupbit.get_ohlcv(ticker, "minute1", diff_min)
#
#     # 차이만큼의 과거 데이터 삭제
#     qry = "DELETE FROM %s " \
#             "WHERE TIME_IDX in (" \
#             "	SELECT TIME_IDX FROM LOOM_MIN_1" \
#             "	WHERE rownum <= %d)" % (target_table, diff_min)
#
#     cursor.execute(qry)
#     # conn.commit()
#
#     # 삭제된만큼 새로 받아온 데이터 추가하기
#     for i, data in enumerate(df.values.tolist()):
#         qry = "insert into %s values(" \
#               "to_date('%s', 'YYYY-MM-DD HH24:MI:SS'),'%d','%d','%d','%d','%d')" \
#               % (target_table, df.index[i], data[0], data[1], data[2], data[3], data[4])
#         cursor.execute(qry)
#         if i % 1000 == 0:
#             print("%d rows insert complete..." % i)
#
#     conn.commit()


### table명 숫자로 시작시 invalid table_name err 발생..
### 현재 1inch네트워크 db조작 불가. 네이밍룰 재정의 해야할듯.


###### data insert code
st = datetime.now().timestamp()
print("호출 시작!!!!", datetime.now())
target = "ALGO"
# df = pyupbit.get_ohlcv("KRW-ELF", "minute1", 1000, to="20210915")
df = pyupbit.get_ohlcv("KRW-%s" % target, "minute1", 4320)
# df = pyupbit.get_ohlcv("KRW-BCHA", "minute1", 4320)

ed = datetime.now().timestamp()
print("호출 종료!!!!", datetime.now())
print("소요시간 : ", ed - st)

for i, data in enumerate(df.values.tolist()):
    qry = "insert into %s_min_1 values(" \
          "to_date('%s', 'YYYY-MM-DD HH24:MI:SS'),'%d','%d','%d','%d','%d')" \
          % (target, df.index[i], data[0], data[1], data[2], data[3], data[4])

    cursor.execute(qry)
    if i % 1000 == 0:
        print("%d rows insert complete..." % i)

conn.commit()

#
# # 딕셔너리변환 함수 오버라이딩
# cursor.rowfactory = makeDictFactory(cursor)
#
# rows = cursor.fetchall()