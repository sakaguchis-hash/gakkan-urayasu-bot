import streamlit as st
import sys
import os

# 既存のボットロジックを読み込み（または同一ナレッジを保持）
KNOWLEDGE = {
    "理念": """【校訓・教育理念】
■ 校訓: 「自主・自学」 — 自分で選び、自分で伸びていく力
■ スローガン: 「A better me」= 昨日の自分を更新し続ける（カコイチ更新）
他人との比較ではなく、自分自身の興味や目標に向き合い、考え、行動し、振り返る力を育てます。
■ 3つの教育方針:
 1. 自己の開発（個性の尊重と伸長）
 2. 判断と責任（主体的な行動と責任感）
 3. 相互扶助（思いやりの心と協調性）""",

    "コース": """【4つのコース紹介】
東京学館浦安高校は全コース6限授業で統一されています。7限目の時間は補習・部活動・自習・個別指導など柔軟に活用できます。

1. 特別進学コース＋選抜（特進）
   - 国公立大学や難関私立大学の合格を目指すコース。
   - 習熟度別授業や手厚い進学指導を実施。

2. 総合進学コース＋選抜（総進）
   - 大学・短大・専門学校への進学から就職まで、多様な進路に対応。
   - 2年次より文系・理系・芸術系などの系列・選択科目が充実。

3. 国際教養コース（国教）
   - 語学力と国際感覚を養うコース。私立文系大学や海外大学に対応。
   - 希望者は全員参加可能なニュージーランドへの3か月留学プログラムを実施。

4. スポーツ進学コース（スポ科）
   - 運動能力と学力を兼ね備えた優れた競技者の育成を目指すコース。
   - 各部活動で全国大会や関東大会を目指し、スポーツ科学等の専門科目も展開。""",

    "部活動": """【部活動・同好会紹介】
運動系・文化系合わせて31の部活動・同好会が活発に活動しています。

■ 運動系（抜粋）:
  - テニス部（全国レベルの強豪）
  - ハンドボール部
  - バスケットボール部
  - サッカー部
  - 陸上競技部
  - 剣道部・柔道部・バレーボール部など

■ 文化系（抜粋）:
  - 吹奏楽部
  - 演劇部
  - 美術部
  - 書道部
  - パソコン部
  - インターアクト部など""",

    "アクセス": """【基本情報・アクセス】
■ 学校名: 東京学館浦安高等学校（学校法人鎌形学園）
■ 所在地: 〒279-0023 千葉県浦安市高洲1-23-1
■ 交通アクセス:
  - JR京葉線「新浦安駅」よりバス約10分（または徒歩約20分）
■ 連絡先:
  - TEL: 047-353-8821
  - FAX: 047-355-1123
  - Email: kouhou@gakkan-urayasu.ed.jp""",

    "進路": """【進路支援・学習サポート】
■ 主な学習サポート体系:
  - 全コース6限授業（放課後の7限目は補習・自習・部活動に活用）
  - スタディサプリ導入による自学自習の促進
  - 定期的な到達度テストや模試の実施
  - 長期休業（夏期・冬期）中の進学講習・特進合宿"""
}

def get_bot_response(user_input: str) -> str:
    user_input = user_input.strip()
    if not user_input:
        return "質問を入力してください。"

    keywords_map = {
        ("コース", "学科", "特進", "総進", "国際", "スポーツ", "授業", "6限", "選抜"): KNOWLEDGE["コース"],
        ("理念", "校訓", "方針", "スローガン", "教育", "自主", "自学"): KNOWLEDGE["理念"],
        ("部活", "運動", "文化", "テニス", "吹奏楽", "クラブ"): KNOWLEDGE["部活動"],
        ("場所", "アクセス", "住所", "電話", "問い合わせ", "行き方", "新浦安", "駅"): KNOWLEDGE["アクセス"],
        ("進路", "大学", "合格", "講習", "補習", "スタサプ", "サポート", "留学", "ニュージーランド"): KNOWLEDGE["進路"]
    }

    matched_responses = []
    for keywords, response in keywords_map.items():
        if any(kw in user_input for kw in keywords):
            matched_responses.append(response)

    if matched_responses:
        return "\n\n-------------------------\n\n".join(matched_responses)
    else:
        return f"ご質問「{user_input}」に関する直接のキーワードが見つかりませんでした。\nサイドバーのボタンから気になる項目を選ぶか、「コース」「部活」「校訓」「アクセス」「進路」などのキーワードを含めて再度質問してみてください！"

# Streamlit UI 設定
st.set_page_config(page_title="東京学館浦安高等学校 Q&Aボット", page_icon="🏫", layout="wide")

st.title("🏫 東京学館浦安高等学校 公式Q&Aボット")
st.caption("公式サイトの情報に基づき、学校のコース、部活、校訓、アクセスなどの質問にお答えします。")

# サイドバー
with st.sidebar:
    st.header("📌 Quick Menu")
    st.markdown("気になるトピックをワンタップで質問できます：")
    
    if st.button("🏫 4つのコースについて"):
        st.session_state.quick_query = "コースについて教えて"
    if st.button("🌟 校訓・教育スローガン"):
        st.session_state.quick_query = "校訓やスローガンについて教えて"
    if st.button("⚽ 部活動一覧"):
        st.session_state.quick_query = "どんな部活動がありますか？"
    if st.button("📍 所在地・アクセス"):
        st.session_state.quick_query = "学校の場所やアクセス方法は？"
    if st.button("🎓 進路・学習サポート"):
        st.session_state.quick_query = "進路指導やサポート体制は？"
        
    st.divider()
    st.markdown("**学校基本情報**")
    st.text("〒279-0023 千葉県浦安市高洲1-23-1\nTEL: 047-353-8821")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは！東京学館浦安高等学校の案内ボットです。学校生活やコース、部活動などについて何でもお尋ねください。"}
    ]

# Quick Menuからの入力処理
prompt_input = None
if "quick_query" in st.session_state and st.session_state.quick_query:
    prompt_input = st.session_state.quick_query
    st.session_state.quick_query = None

# チャット履歴表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# チャット入力
user_query = st.chat_input("質問を入力してください（例：コースの種類は？、部活は何がある？）")
if user_query:
    prompt_input = user_query

if prompt_input:
    # ユーザー発言表示
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    # ボット応答生成＆表示
    response = get_bot_response(prompt_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
