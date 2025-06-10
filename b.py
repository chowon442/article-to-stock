from ac import report # 기사 URL 기업 추출 함수 호출
from pykrx import stock # 한국 주식시장 api
from datetime import datetime, timedelta

def analyze(url):

    processed_companies = []
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

    # 뉴스 기사 여부 확인
    is_news_article = data.get("is_news_article", False)
    print(is_news_article, type(is_news_article))
    if not is_news_article:
        print(f"제공된 URL이 단일 뉴스 기사가 아닙니다. 처리를 건너뜁니다.")
        return {
            "is_news_article": False,
            "article": {"title": "null", "content": "단일 뉴스 기사가 아님"},
            "companies": []
        }

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

    # 한국 거래소 데이터 로드
    try:
        code_name_map = {code: stock.get_market_ticker_name(code)
            for code in stock.get_market_ticker_list(market="ALL")}
    except Exception as e:
        print(f"주식 데이터 로드 실패: {e}")
        code_name_map = {}

    print(f"processed_companies: {processed_companies}")

    result = []
    for company_item in processed_companies:
        cleaned_cp = company_item["cleaned_name"]
        comment = company_item["comment"]
        impact = company_item["impact"]
        
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

    final_result = {
        "is_news_article": data.get("is_news_article", False),
        "article": article_data,
        "companies": result
    }

    print(f"final_result: {final_result}")

    return final_result 
