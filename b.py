from ac import report 

clean_list = []
raw_list = []

url = input("url :")
data = report(url)

if data == -1:
    print (f"LLM 분석 실패 또는 잘못된 응답입니다.")
    exit()

for company in data:
    company_name = company.get("name")
    raw_list.append(company_name)

for cp in raw_list:
    for marker in ['(주)', '(유)','(재)', '(사)', '주식회사', '㈜' ]:
        cp = cp.replace(marker, '')
    clean_list.append(cp.strip())
print (clean_list)
