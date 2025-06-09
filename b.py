from ac import report 
from pykrx import stock
<<<<<<< HEAD
from datetime import datetime, timedelta
=======
from datetime import datetime
>>>>>>> 63e5c367bfda01c088a140be1c1d89460a64cdc3

def analyze(url):

    processed_companies = []
<<<<<<< HEAD
    today = datetime.today()
    
    # 최근 5일 내 거래일 찾기 (주말/공휴일 대응)
    recent_dates = []
    for i in range(5):
        date = (today - timedelta(days=i)).strftime("%Y%m%d")
        recent_dates.append(date)
    
    data = report(url)

    if data == -1:
        print(f"LLM 분석 실패 또는 잘못된 응답입니다.")
        return -1
=======
    today = datetime.today().strftime("%Y%m%d")
    data = report(url)

    if data == -1:
        print (f"LLM 분석 실패 또는 잘못된 응답입니다.")
        exit()
>>>>>>> 63e5c367bfda01c088a140be1c1d89460a64cdc3

    article_data = data.get("article", {"title": "", "content": ""})
    companies_data = data.get("companies", [])

    for item in companies_data:
        cp = item["name"]
        comment = item["comment"]
        impact = item["impact"]

        # 기업명 정제
        for marker in ["(주)", "(유)","(재)", "(사)", "주식회사", "㈜" ]:
            cp = cp.replace(marker, '')
        cleaned_cp = cp.strip()
        processed_companies.append({"cleaned_name": cleaned_cp, "comment": comment, "impact": impact})

<<<<<<< HEAD
    # 한국 거래소 데이터 로드
    try:
        code_name_map = {code: stock.get_market_ticker_name(code)
            for code in stock.get_market_ticker_list(market="ALL")}
    except Exception as e:
        print(f"주식 데이터 로드 실패: {e}")
        code_name_map = {}
=======
    code_name_map = {code: stock.get_market_ticker_name(code)
        for code in stock.get_market_ticker_list(market="ALL")}
>>>>>>> 63e5c367bfda01c088a140be1c1d89460a64cdc3

    print(f"processed_companies: {processed_companies}")

    result = []
    for company_item in processed_companies:
        cleaned_cp = company_item["cleaned_name"]
        comment = company_item["comment"]
        impact = company_item["impact"]
<<<<<<< HEAD
        
        found_match = False
        
        # 한국 거래소에서 매칭 시도
        for code, company_name in code_name_map.items():
            # 완전 일치 또는 부분 일치 확인
            if (cleaned_cp == company_name or
                company_name in cleaned_cp):
                
                # 최근 거래일 데이터 찾기
                stock_data = None
                for date_str in recent_dates:
                    try:
                        status = stock.get_market_ohlcv_by_date(date_str, date_str, code)
                        if not status.empty:
                            stock_data = status.iloc[0]
                            break
                    except:
                        continue
                
                if stock_data is not None:
                    changes = float(stock_data["등락률"])
                    arrow = "▲" if changes > 0 else "▼"
                    result.append({
                        "name": cleaned_cp,
                        "code": code,
                        "final_price": float(stock_data['종가']),
                        "changes": f"{arrow} {changes:.2f}%",
                        "comment": comment,
                        "impact": impact
                    })
                    print(f"매칭 성공: {result[-1]}")
                    found_match = True
                    break
        
        # 한국 거래소에서 매칭되지 않은 경우도 결과에 포함 (해외 기업, 비상장 기업 등)
        if not found_match:
            result.append({
                "name": cleaned_cp,
                "code": None,
                "final_price": None,
                "changes": "거래소 정보 없음",
                "comment": comment,
                "impact": impact
            })
            print(f"거래소 정보 없음: {cleaned_cp}")
=======

        for code, company_name in code_name_map.items():
            # 기업명 일치
            if cleaned_cp == company_name:
                status = stock.get_market_ohlcv_by_date(today, today, code)
                if status.empty:
                    continue
                row = status.iloc[0]
                changes = float(row["등락률"])
                arrow = "▲" if changes > 0 else "▼"
                result.append({"name":company_name, "code":code, "final_price":float(row['종가']), "changes":f"{arrow} {changes:.2f}%", "comment":comment, "impact":impact})
                print(result[-1])
>>>>>>> 63e5c367bfda01c088a140be1c1d89460a64cdc3

    final_result = {
        "article": article_data,
        "companies": result
    }

    print(f"final_result: {final_result}")

    return final_result 
