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
    SELECT * FROM PLA_MIN_1
    WHERE time_idx > to_date('2021-11-10 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
""")

cursor.rowfactory = makeDictFactory(cursor)
rows = cursor.fetchall()
arr = []
avg_vol = 0
avg_vol_min = []

for i, val in enumerate(rows):
    # 최근 60분간의 데이터로 평균 거래량 구하기
    if i <= 60:
        arr.append(val['VOLUME'])
    else:
        del arr[0]  # 60분 평균값을 구해야하므로 가장 앞의 데이터를 하나씩 지워서 길이 60을 유지
        np_arr = np.array(arr)
        avg_vol = int(np.mean(np_arr))
        # 5분 전까자의 60분 평균거래량을 저장하는 배열에 추가
        avg_vol_min.append(avg_vol)
        if len(avg_vol_min) > 5:
            del avg_vol_min[0]

        arr.append(val['VOLUME'])

        # 최근 60분 평균거래량의 10배가 넘는 거래량이 터지는 지점 포착
        # if val['VOLUME'] > avg_vol*10:
        #     print("TIME_IDX: %s, val['VOLUME'] : %d, avg_vol: %d" % (val['TIME_IDX'], val['VOLUME'], avg_vol))

        # -5분지점부터 60분간 평균거래량의 10배가 넘는 거래량이 터지는 지점 포착
        if val['VOLUME'] > avg_vol_min[0]*10:
            print("-5min -> TIME_IDX: %s, val['VOLUME'] : %d, avg_vol: %d" % (val['TIME_IDX'], val['VOLUME'], avg_vol))
            print(avg_vol_min)


    # print("time: %s, avg_vol: %d" % (val['TIME_IDX'], avg_vol))
