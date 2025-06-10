import time
from b import analyze

url = input("주식 정보가 필요한 url을 입력하세요:")
start_time = time.time()
result = analyze(url)
end_time = time.time()
execution_time = end_time - start_time
print(f"analyze 함수 실행 시간: {execution_time:.2f} 초")

if result == -1:
    print("LLM 분석 실패 또는 잘못된 응답입니다.")
else:
    article_info = result.get("article", {})
    companies_info = result.get("companies", [])

    print("\n--- 기사 정보 ---")
    print(f"제목: {article_info.get('title', '제목 없음')}")
    print(f"내용: {article_info.get('content', '내용 없음')}")

    print("\n--- 기업 분석 결과 ---")
    if companies_info:
        for company in companies_info:
            print(company)
    else:
        print("분석된 기업 정보가 없습니다.")

# if len(result)  
