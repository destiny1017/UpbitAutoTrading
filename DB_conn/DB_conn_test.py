import cx_Oracle as ora
import os
import pyupbit


# 쿼리 결과를 dictionary형태로 받아오기위한 함수 오버라이딩
def makeDictFactory(cursor):
    columnNames = [d[0] for d in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow


# 인코딩 설정
os.putenv('NLS_LANG', '.UTF8')

# DB연결
conn = ora.connect('c##upbitpy', '1234', 'localhost:1522/XE')

# 커서 할당
cursor = conn.cursor()

# 쿼리 실행
cursor.execute("""
    select tname
    from tab
""")

# 딕셔너리변환 함수 오버라이딩
cursor.rowfactory = makeDictFactory(cursor)

# 오버라이딩한 함수로 쿼리 결과 받아오기
rows = cursor.fetchall()

# 결과 출력
for row in rows:
    print(row)
