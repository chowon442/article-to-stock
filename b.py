from ac import report 
from pykrx import stock
from datetime import datetime

def analyize(url):

    raw_list = []
    result = []

    clean_list = []
    today = datetime.today().strftime("%Y%m%d")
    data = report(url)

    if data == -1:
        print (f"LLM 분석 실패 또는 잘못된 응답입니다.")
        exit()

    for d in data:
        d_name = d.get("name")
        raw_list.append(d_name)

    for cp in raw_list:
        for marker in ["(주)", "(유)","(재)", "(사)", "주식회사", "㈜" ]:
            cp = cp.replace(marker, '')
        clean_list.append(cp.strip())

    code_name_map = {code: stock.get_market_ticker_name(code)
        for code in stock.get_market_ticker_list(market="ALL")}

    for cp in clean_list:
        for code, company in code_name_map.items():
            if cp == company:
                status = stock.get_market_ohlcv_by_date(today, today, code)
                if status.empty:
                    continue
                row = status.iloc[0]
                changes = float(row["등락률"])
                arrow = "▲" if changes > 0 else "▼"
                result.append({"name":company, "code":code, "final_price":float(row['종가']), "changes":f"{arrow} {changes:.2f}%"})

    print (result)
    return result 
