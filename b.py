from pykrx import stock
from datetime import datetime

def get_stock_code_by_name(name: str) -> str:
    df = stock.get_market_ticker_list(market="ALL")
    for code in df:
        if stock.get_market_ticker_name(code) == name:
            return code
    return None

# 테스트
code = get_stock_code_by_name("삼성전자")
print("삼성전자 코드:", code)
