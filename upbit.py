import pyupbit
# print(pyupbit.get_tickers())

access = "ZRKNRsIjvtcfCIot8GWebGMRtJdr2evQKee5xkQL"          # 본인 값으로 변경
secret = "NxhFIxaVJ3iUZPvy3zirrBaSaq9hxyfbNtSDx4RX"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))
print(upbit.get_balance("KRW-DOGE"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회