
import streamlit as st
import openai
import random

st.set_page_config(page_title="AIツイート自動生成ツール", layout="centered")

st.title("1ツイート煽り系/共感系ジェネレーター（AI自動生成）")
st.caption("特徴とURLを入れて、APIキーを貼るだけ。毎回違うツイートが最大10個自動生成されます。")

# 入力欄
api_key = st.text_input("【必須】OpenAI APIキー", type="password")
url = st.text_input("動画URL（例：https://gofile.io/d/xxxxxx）")
note1 = st.text_input("特徴1（例：制服で無言腰ふり）")
note2 = st.text_input("特徴2（例：カメラ目線で見せつけ）")

tone = st.selectbox("トーンを選んでください", ["煽り系", "共感系"])
count = st.slider("生成するツイート数", 5, 10, 5)

tiny_choices = [
    "ランダムにする",
    "リンクを付けない",
    "http://tiny.cc/gyo1",
    "http://tiny.cc/gyo2",
    "http://tiny.cc/penyo",
    "http://tiny.cc/penyo2",
    "http://tiny.cc/mute1",
    "http://tiny.cc/mute2",
    "http://tiny.cc/re858",
    "http://tiny.cc/re8582",
    "http://tiny.cc/zoryo",
    "http://tiny.cc/zoryo2",
    "http://tiny.cc/kuna663",
    "http://tiny.cc/kuna6634",
    "http://tiny.cc/chap2",
    "http://tiny.cc/chap1",
    "http://tiny.cc/m4vf001",
    "http://tiny.cc/o4vf001",
    "http://tiny.cc/w4vf001",
    "http://tiny.cc/y4vf001",
    "http://tiny.cc/haruka694",
    "http://tiny.cc/05vf001"
]

selected_tiny = st.selectbox("TinyURLを選んでください（または付けない）", tiny_choices)

def get_final_tiny():
    if selected_tiny == "ランダムにする":
        return random.choice(tiny_choices[2:])
    elif selected_tiny == "リンクを付けない":
        return ""
    else:
        return selected_tiny

def call_openai(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"エラー: {str(e)}"

def generate_prompt(note1, note2, url, tone, count, tiny):
    return f"""
あなたは短文ツイートライターです。
以下の条件を使って、Twitter向けの1行ツイートを{count}個、日本語で生成してください。

# 条件
・トーンは「{tone}」で統一
・note1：「{note1}」
・note2：「{note2}」
・URL：「{url}」
・短く強く、ツイート1本 = 1行構成、語尾に {tiny} を追加してください
・全て異なる構文で

# 出力形式
1. ツイート文
2. ツイート文
...
{count}個まで
"""

# 実行ボタン
if st.button("ツイート文を生成する"):
    if not api_key or not url or not note1 or not note2:
        st.error("全ての項目を入力してください（APIキーも必須）")
    else:
        tiny = get_final_tiny()
        prompt = generate_prompt(note1, note2, url, tone, count, tiny)
        with st.spinner("AIがツイートを考え中..."):
            result = call_openai(prompt, api_key)
        st.success("生成されたツイート文：")
        st.code(result, language="markdown")
