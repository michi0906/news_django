import os
import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .services import fetch_news_titles, generate_ogiri_prompt_ai

import google.generativeai as genai

# Gemini の設定：環境変数から API キーを読む
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_ogiri_prompt_from_title(title: str) -> str:
    """
    1つのニュースタイトルから、大喜利お題を1つ生成して返す。
    失敗したら、 fallback のメッセージを返す。
    """
    if not GEMINI_API_KEY:
        # APIキーが無いときは実行できないので固定文
        return "（お題生成用のAIキーが設定されていません。）"

    # 大喜利お題用のプロンプト
    system_prompt = f"""
あなたは大喜利のお題職人です。
以下のニュースタイトルをもとに、ユーモアのある大喜利のお題を1つ作成してください。

▼ルール
- ニュースの事実をそのまま説明しない
- 「○○とは？」「どんな○○？」など質問文で終わる形にする
- 20〜40文字程度
- ひねりやギャップを入れて、ボケやすいお題にする
- ニュースタイトルに出てくる固有名詞はそのまま使ってOK

▼ニュースタイトル
「{title}」

▼出力フォーマット
大喜利お題のみを1行で出力してください。
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(system_prompt)
        text = (response.text or "").strip()
        if not text:
            return "（お題の生成に失敗しました。自分でボケてみてください。）"
        return text
    except Exception:
        # 例外が出た場合もアプリが落ちないようにする
        return "（お題の生成に失敗しました。自分でボケてみてください。）"


@login_required
def news_list(request):
    category = request.GET.get("category", "politics")
    titles = fetch_news_titles(category, page_size=100)

    ogiri_pairs: list[dict] = []

    if titles:
        sample_titles = random.sample(titles, k=min(3, len(titles)))
    else:
        sample_titles = []

    # ★ここが本番の保証処理：必ずlen==3になるよう埋めてる
    while len(sample_titles) < 3:
        sample_titles.append("ニュース消失！今どんなボケしてくれる？")

    for t in sample_titles[:3]:
        ogiri = generate_ogiri_prompt_ai(t)
        ogiri_pairs.append({"title": t, "prompt": ogiri})

    context = {
        "titles": titles,
        "selected_category": category,
        "ogiri_pairs": ogiri_pairs[:3],  # ★断定の3個保証
    }
    return render(request, "newsapp/news_list.html", context)

