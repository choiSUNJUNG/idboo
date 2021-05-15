import time
import pyupbit
import datetime
import openpyxl

access = "ZRKNRsIjvtcfCIot8GWebGMRtJdr2evQKee5xkQL"          # 본인 값으로 변경
secret = "NxhFIxaVJ3iUZPvy3zirrBaSaq9hxyfbNtSDx4RX"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2) # 전일 데이터까지만 인출
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# def get_ma15(ticker):
#     """15일 이동 평균선 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
#     ma15 = df['close'].rolling(15).mean().iloc[-1]
#     return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    # print(balances)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

def get_daily_gap(ticker):
#     """하루 가격차의 50% 산출"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    # prev_low = df['low'].shift(1)
    df['prev_low'] = df['low'].shift(1)
    df['decision_price'] = df['high'] - ((df['high'] - df['low']) * 0.5) 
    return df

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# excel table 생성
wb = openpyxl.Workbook()
wb.save('upbit_deal_data.xlsx')
sheet = wb.active
# cell name : time, cur_pr, high, low, k, ref_pr, prev_low, sell 
sheet.append(['time', 'cur_price', 'high', 'low', 'k', 'ref_price', 'prev_low', 'buy-sell'])
wb.save('upbit_deal_data.xlsx')

# 자동매매 시작

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-DOGE") #날짜 바뀌는 것 실시간 업데이트
        end_time = start_time + datetime.timedelta(days=1)
        df = get_daily_gap("KRW-DOGE")  # 하루 중 계속 변활 수 있는 값으로 실시간 도출 필요
        current_price = get_current_price("KRW-DOGE")
        high = df.iloc[-1]['high']
        low = df.iloc[-1]['low']
        ref_price = df.iloc[-1]['decision_price'] 
        prev_low = df.iloc[-1]['prev_low']
        if start_time < now < end_time - datetime.timedelta(seconds=300):
        # if start_time < now < end_time - datetime.timedelta(seconds=100):
            target_price = get_target_price("KRW-DOGE", 0.5)
            # ma15 = get_ma15("KRW-DOGE")
           
            if target_price < current_price: 
            # if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-DOGE", krw*0.9)     # 원화의 90% 금액으로 buy
                    sheet.append([now, current_price, high, low, '0.5', ref_price, prev_low, 'buy'])
                    wb.save('upbit_deal_data.xlsx')
            else:
                pass
            #     print("현재가({0})가 목표가({1})보다 낮다. buy조건 불성립".format(current_price, target_price))

        elif current_price > df.iloc[-1]['decision_price'] and current_price > df.iloc[-1]['prev_low']:
            
            # 현재가가 최고가 대비 하루 변동폭의 50% 이상인 경우 no sell
            # 이 경우 다음날 폭락있을 경우에도 현재가가 최고가 대비 변동폭 50% 범위내에 있을 경우 계속 홀딩하게 됨
            # 따라서 현재 가격이 전일 최저가 이상일 경우에만 홀딩 조치 
            
            # 매도는 당일 결정가 기준 및 전일 저가 기준으로 결정
            # print("현재가({0})가 매도기준가({1})보다 높거나 전일저가({2})보다 높아 sell조건 \
            #       불성립".format(current_price, df.iloc[-1]['decision_price'], df.iloc[-1]['prev_low']))
            # df.to_excel("test5.xlsx")
            # log 남기기(현재가, 기준가, 전일저가, no sell 기록 남기기)
            
            pass
        else:
            coin = get_balance("DOGE")
            if coin > 1:
                upbit.sell_market_order("KRW-DOGE", coin*0.9995)
                sheet.append([now, current_price, high, low, '0.5', ref_price, prev_low, 'sell'])
                wb.save('upbit_deal_data.xlsx')
                # log 남기기(현재가, 기준가, 전일저가, sell 기록 남기기)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)









