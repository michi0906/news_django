import os
import requests
from random import choice
import google.generativeai as genai

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

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
あなたは日本のお笑い芸人です。
以下のニュースタイトルを元に、大喜利のお題を１つだけ作ってください。

条件:
- 日本語
- できるだけ短くシンプル
- ひねりのある、ボケやすいお題
- 出力はお題の文章だけ（前置きや説明は書かない）

ニュースタイトル: 「{title}」
"""

    try:
        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        if not text:
            return f"【大喜利】『{title}』というニュースから、自由にボケてください。"
        return text
    except Exception:
        # 何かあったらフォールバック
        return f"【大喜利】『{title}』というニュースから、自由にボケてください。"""
