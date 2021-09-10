import pyupbit
import numpy as np

# 변동성 돌파 전략 백테스팅

# ohlcv(open, high, low, close, volume) 시가, 고가, 저가, 종가, 거래량 데이터 받아오기
df = pyupbit.get_ohlcv("KRW-BTC")

# 변동폭 * k 계산 -> (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.5

# target(매수가), range 컬럼을 한 칸씩 밑으로 내림(.shift(n))
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0005  # 거래 수수료

# np.where(조건, true 반환값, false 반환값) -> 3항연산자와 같은 기능
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
# 누적 곱 계산(cumprod) => 누적수익률
df['hpr'] = df['ror'].cumprod()

# Drow Down 계산 (누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# MDD계산
print("MDD(%): ", df['dd'].max())

# 엑셀로 저장
df.to_excel("dd.xlsx")

