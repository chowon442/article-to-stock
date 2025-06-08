import requests
import json

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer api-key",
    "Content-Type": "application/json"
}

def report(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        page_text = res.text
    except Exception as e:
        print(e)
        return -1
    example = '뉴스 분석 리포트\n\n기업1 : 50글자 이내의 긍정적,부정적 분석 및 향후 전망 분석 리포트\n기업2 : ...'
    found_data = json.dumps({
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "system", "content": '애널리스트로서 내용에 대해 예시에 맞게 출력\n예시 : ' + example},
            {"role": "user", "content": page_text}
        ]
    })
    try:
        response = requests.post(url=URL, headers=HEADERS, data=found_data)
        response.raise_for_status()
    except Exception as e:
        print(e)
        return -1
    
    if response.status_code != 200:
        print(response.status_code)
        return -1
    else:
        return response.json()['choices'][0]['message']['content']
