from ac import report # 앞선 파일의 URL에서 회사 목록 추출하는 함수 활용
from pykrx import stock # 한국 주식시장 API
from datetime import datetime

# 함수로 국내 주식회사 목록과 비교 후 주가(종가), 변화율, 회사 코드 반환
def analyze(url):

    result = []
    clean_list = []
    today = datetime.today().strftime("%Y%m%d")
    data = report(url)

    if data == -1: #url에서 회사가 추출되지 않았을 때
        print (f"LLM 분석 실패 또는 잘못된 응답입니다.")
        exit()

    for item in data:
        cp = item["name"]
        comment = item["comment"]

        # LLM이 회사명 추출할 때 주식회사(혹은 유한회사, 재단법인, 사단법인)의 명칭을 붙일 때를 대비하여 이를 제거
        for marker in ["(주)", "(유)","(재)", "(사)", "주식회사", "㈜" ]:
            cp = cp.replace(marker, '')
        clean_list.append(cp.strip())

    # 국내 주식 시장 데이터 추출 
    code_name_map = {code: stock.get_market_ticker_name(code)
        for code in stock.get_market_ticker_list(market="ALL")}

    # 해당하는 주식회사의 필요한 정보 추출 및 반환 
    for cp in clean_list:
        for code, company in code_name_map.items():
            if cp == company:
                status = stock.get_market_ohlcv_by_date(today, today, code) # 원하는 주식회사에 대한 주식시장의 정보 모두 가져옴
                if status.empty:
                    continue
                row = status.iloc[0] # 해당 날짜(당일)에 대한 주식 정보
                changes = float(row["등락률"]) # 기본 형식이 실수가 아님
                arrow = "▲" if changes > 0 else "▼" # +- 시각화 기호
                result.append({"name":company, "code":code, "final_price":float(row['종가']), "changes":f"{arrow} {changes:.2f}%", "comment":comment})
    return result 
