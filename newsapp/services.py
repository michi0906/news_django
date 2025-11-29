import os
import requests
# from random import choice
# import google.generativeai as genai
import requests


NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"


def fetch_news_titles(category: str, page_size: int = 100) -> list[str]:
    """
    指定カテゴリのニュースタイトルを最大 page_size 件返す。
    取得に失敗したら空リストを返す。
    """
    if not NEWSAPI_KEY:
        return []

    page_size = min(page_size, 100)

    # すべて everything で検索キーワード方式
    if category == "sports":
        url = EVERYTHING_URL
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": "sports OR スポーツ",
            "language": "jp",
            "pageSize": page_size,
        }
    elif category == "entertainment":
        url = EVERYTHING_URL
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": "entertainment OR 芸能",
            "language": "jp",
            "pageSize": page_size,
        }
    elif category == "politics":
        url = EVERYTHING_URL
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": "politics OR 政治",
            "language": "jp",
            "pageSize": page_size,
        }
    elif category == "anime":
        url = EVERYTHING_URL
        params = {
            "apiKey": NEWSAPI_KEY,
            "q": "anime OR アニメ",
            "language": "jp",
            "pageSize": page_size,
        }
    else:
        return []

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return []
    except requests.RequestException:
        return []

    articles = response.json().get("articles", [])
    titles = [a.get("title") for a in articles if a.get("title")]

    return titles[:page_size]


def generate_ogiri_prompt_ai(title: str) -> str:
    """
    Gemini にニュースタイトルを渡し、面白い大喜利のお題を生成してもらう。
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return f"【エラー】GEMINI_API_KEY が設定されていません。（タイトル: {title}）"

    # genai.configure(api_key=api_key)

    # model = genai.GenerativeModel("gemini-1.5-flash")

     # ✅ REST APIのURL（SDKではなくrequestsで叩く）
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}

    # ✅ リクエスト内容（JSON形式）
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
ニュースタイトル『{title}』をもとに、
日本語で面白い大喜利のお題を1つだけ作ってください。

条件:
- シンプルでひねりがある
- 前置きや説明は不要
- お題文のみを返す
"""
                    }
                ]
            }
        ]
    }
    try:
        # ✅ HTTP POST でリクエストを送信
        response = requests.post( url, headers=headers, json=payload, params={"key": api_key})


        result = response.json()

        # デバッグ用にレスポンス全体を出力（開発中のみ）
        print("Geminiレスポンス:", result)

        # ✅ candidatesが存在する場合だけ抽出
        if "candidates" in result:
            text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            return text if text else f"【大喜利】『{title}』というニュースから、自由にボケてください。"
        else:
            # エラーレスポンスの場合
            err = result.get("error", {}).get("message", "不明なエラー")
            print("Geminiエラー内容:", err)
            return f"【Geminiエラー】お題生成に失敗しました（{err}）"

        # if not text:
        #     return f"【大喜利】『{title}』というニュースから、自由にボケてください。"
        # return text
    except Exception as e:
        print("Geminiエラー:", e)
        return f"【大喜利】『{title}』というニュースから、自由にボケてください。"
