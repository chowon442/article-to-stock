import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

URL = "https://openrouter.ai/api/v1/chat/completions"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY 설정 없음.")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def report(url):
    start_time = time.time()
    try:
        res = requests.get(url)
        res.raise_for_status()
        page_text = res.text
    except Exception as e:
        print(f"페이지 가져오기 실패: {e}")
        return -1
    end_time = time.time()
    print(f"페이지 가져오기 시간: {end_time - start_time:.2f} 초")

    example = json.dumps({
        "article": {
            "title": "샘플 기사 제목",
            "content": "이것은 샘플 기사 내용입니다. 실제 구현에서는 입력된 URL의 기사 내용이 여기에 표시됩니다."
        },
        "companies": [
            {"name": "삼성전자", "comment": "AI 성장 기대", "impact": "긍정적"},
            {"name": "LG전자", "comment": "경쟁 심화", "impact": "단기 부정적"}
        ]
    })

    found_data = json.dumps({
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "너는 금융 애널리스트야. 사용자가 제공한 내용을 분석해서 다음과 같이 처리해줘:\n"
                    "1. 먼저 제공된 내용이 단일 뉴스 기사 본문인지 판단해. 만약 메인 페이지, 목록 페이지, 여러 뉴스가 섞인 내용, 또는 단일 뉴스 기사가 아닌 경우라면 'is_news_article'을 false로 설정하고 'article.title'에는 'null'을 넣어줘.\n"
                    "2. 단일 뉴스 기사 본문이 맞다면 'is_news_article'을 true로 설정하고, 뉴스 제목을 추출하여 'article.title'에, 본문을 'article.content'에 넣어줘.\n"
                    "3. 뉴스 본문 안 '주식회사'들을 모두 추출하여 'companies' 배열에 기존과 동일한 JSON 형식으로 리포트를 출력해. (주식회사 외에 기업은 추출하지 말아줘. 예를 들어 '경기도' 등은 회사, 기업이 아니니까 추출하면 안돼. '애플파크'처럼 장소명이나 조직명은 추출하지마)\n"
                    "특히, 'impact' 필드는 반드시 명시된 '긍정적', '단기 긍정적', '부정적', '단기 부정적' 값 중 하나로만 채워야 해. 다른 값은 절대 허용되지 않아.\n예시:\n" + example
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
                "name": "company_and_article_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "is_news_article": {
                            "type": "boolean",
                            "description": "제공된 내용이 단일 뉴스 기사 본문인지 여부"
                        },
                        "article": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "기사 제목"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "기사 내용"
                                }
                            },
                            "required": ["title", "content"]
                        },
                        "companies": {
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
                                    },
                                    "impact": {
                                        "type": "string",
                                        "description": "해당 뉴스가 기업에게 긍정/부정적이었는지를 넣어줘 (결과는 '긍정적', '단기 긍정적', '부정적', '단기 부정적' 중에서만 선택할 것)",
                                        "enum": ["긍정적", "단기 긍정적", "부정적", "단기 부정적"]
                                    }
                                },
                                "required": ["name", "comment", "impact"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["is_news_article", "article", "companies"],
                    "additionalProperties": False
                }
            }
        }
    })

    start_time = time.time()
    try:
        print("API 요청 시작...")
        response = requests.post(url=URL, headers=HEADERS, data=found_data)
        print(f"API 응답 상태 코드: {response.status_code}")
        
        if response.status_code != 200:
            print(f"API 요청 실패. 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")
            return -1
            
    except Exception as e:
        print(f"API 요청 중 에러 발생: {e}")
        return -1
    end_time = time.time()
    print(f"API 응답 처리 시간: {end_time - start_time:.2f} 초")

    try:
        response_json = response.json()
        
        if 'choices' not in response_json:
            print(f"API 응답에 'choices' 키가 없습니다. 응답 키들: {list(response_json.keys())}")
            
            # 에러 메시지가 있는지 확인
            if 'error' in response_json:
                print(f"API 에러: {response_json['error']}")
            
            return -1
        
        if not response_json['choices'] or len(response_json['choices']) == 0:
            print("API 응답의 'choices' 배열이 비어있습니다.")
            return -1
            
        choice = response_json['choices'][0]
        if 'message' not in choice:
            print("첫 번째 choice에 'message' 키가 없습니다.")
            return -1
            
        if 'content' not in choice['message']:
            print("message에 'content' 키가 없습니다.")
            return -1
            
        content = choice['message']['content']
        print(f"추출된 내용: {content}")
        
        if isinstance(content, str):
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 실패: {e}")
                print(f"원본 내용: {content}")
                return -1
        else:
            return content
            
    except json.JSONDecodeError as e:
        print(f"API 응답 JSON 파싱 실패: {e}")
        print(f"응답 텍스트: {response.text}")
        return -1
    except Exception as e:
        print(f"응답 처리 중 에러: {e}")
        return -1