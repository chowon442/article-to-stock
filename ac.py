import requests
import json

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer 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",
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

    example = (
        '[{"name": "삼성전자", "comment": "AI 성장 기대, 긍정적"}, '
        '{"name": "LG전자", "comment": "경쟁 심화, 단기 부정적"}]'
    )

    found_data = json.dumps({
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "너는 금융 애널리스트야. 사용자가 제공한 뉴스 본문에 대해 "
                    "아래 예시에 맞게 JSON 형식 리포트를 출력해.\n예시:\n" + example
                )
            },
            {
                "role": "user",
                "content": page_text
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "company_analysis",
                "strict": True,
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "기업 이름"
                            },
                            "comment": {
                                "type": "string",
                                "description": "뉴스기사에 대해 기업의 긍정,부정 평가 및 향후 전망 분석 코멘트, 50자 이내"
                            }
                        },
                        "required": ["name", "comment"],
                        "additionalProperties": False
                    }
                }
            }
        }
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
        content = response.json()['choices'][0]['message']['content']
        if isinstance(content, str):
            return json.loads(content)
        else:
            return content
    
