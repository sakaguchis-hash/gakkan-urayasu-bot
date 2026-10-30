import streamlit as st
import os

# 1. ページ基本設定
st.set_page_config(
    page_title="東京学館浦安高等学校 入試広報Gemini AIアシスタント",
    page_icon="🏫",
    layout="centered"
)

# 2. 東京学館浦安高等学校 スクールカラーCSS (紺 #0B2545 / 金 #C5A059)
st.markdown("""
<style>
    .stApp {
        background-color: #F8F9FA;
    }
    .school-header {
        background: linear-gradient(135deg, #0B2545 0%, #134074 100%);
        color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 4px solid #C5A059;
    }
    .school-header h1 {
        font-size: 24px;
        font-weight: bold;
        margin: 0 0 8px 0;
        color: #FFFFFF;
    }
    .motto-badge {
        display: inline-block;
        background-color: #C5A059;
        color: #0B2545;
        font-size: 13px;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 4px 6px;
    }
    .ai-badge {
        display: inline-block;
        background-color: #E8F5E9;
        color: #2E7D32;
        font-size: 12px;
        font-weight: bold;
        padding: 3px 10px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    .support-card {
        background-color: #FFFFFF;
        border: 2px solid #C5A059;
        border-radius: 10px;
        padding: 18px;
        margin-top: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# 3. 学校情報ナレッジベース (Geminiのシステムプロンプトおよびフォールバック用)
SCHOOL_KNOWLEDGE_TEXT = """
【学校基本情報】
学校名: 東京学館浦安高等学校（学校法人鎌形学園）
校訓: 「自主・自学」 — 自分で選び、自分で伸びていく力
スローガン: 「A better me」= 昨日の自分を更新し続ける（カコイチ更新）
教育方針: 1.自己の開発 2.判断と責任 3.相互扶助
所在地: 〒279-0023 千葉県浦安市高洲1-23-1
電話番号: 047-353-8821（広報直通）
メール: kouhou@gakkan-urayasu.ed.jp
アクセス: JR京葉線「新浦安駅」より東京ベイシティバスで約10分「東京学館浦安高校」下車徒歩1分。自転車通学可。

【コース制度（全コース6限授業統一・放課後7限に特別講座や部活動）】
1. 特別進学コース（＋選抜）: 国公立大・難関私大を目指す。定員 特進選抜30名 / 特進70名。
2. 総合進学コース（＋選抜）: 大学・短大・専門・就職まで幅広く対応。文武両道。定員260名。
3. 国際教養コース: 私大文系・留学志望向け。3か月間のニュージーランド留学プログラム有。定員35名。
4. スポーツ進学コース: 高い競技レベルと学業の両立。知性と競技力を備えた運動選手を育成。定員35名。

【令和9年度（2027年度）入試要項・推薦基準（内申点目安）】
募集定員: 計430名
前期選抜日程: 第1期 1/17、第2期 1/18、第3期 1/29
共通条件: 評定に「1」がないこと。
・特別進学選抜: 5教科「20以上」
・特別進学: 5教科「18以上」
・総合進学: 5教科「16以上」 または 9教科「29以上」
・国際教養: 5教科「16以上」 または 英語「4以上」
・スポーツ進学: 9教科「27以上」＋部活動実績
※加点ルール（1項目のみ）: 英検/漢検/数検 準2級以上(+2点)、3級(+1点)、3か年皆勤/生徒会役員/部活3年継続(+1点)

【学費・納入金】
入学時納入金: 計 390,000円（入学金15,0000円、教育振興費100,000円、施設充実費70,000円、後援会入会金20,000円、施設設備協力金50,000円）
月額授業料: 38,000円（国の就学支援金や千葉県授業料軽減制度の対象）

【学校生活・施設】
学食: 本館1階。一番人気「から揚げ丼」、日替わりランチ500円、ラーメン4種。
スマホ: 持参可能（朝SHR〜夕方終礼までは個人のロッカーにて保管）。
端末: 個人での新規購入不要（校内整備端末を利用）。
部活動: 運動部・文化部 全31部・同好会（テニス、ハンドボール、吹奏楽、ダンス、演劇など）。
"""

# Gemini APIクライアント初期化関数
def get_gemini_response(prompt_text, user_message):
    api_key = None
    # 1. Streamlit Secretsからの取得試行
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    # 2. 環境変数からの取得試行
    elif "GEMINI_API_KEY" in os.environ:
        api_key = os.environ["GEMINI_API_KEY"]
    # 3. サイドバー等セッションからの取得試行
    elif "user_gemini_key" in st.session_state and st.session_state.user_gemini_key:
        api_key = st.session_state.user_gemini_key

    if not api_key:
        return None  # APIキーがない場合はフォールバック

    try:
        # 新しい google-genai SDK または google-generativeai の呼び出し
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        system_instruction = f"""
あなたは「東京学館浦安高等学校 入試広報AIアシスタント」です。
保護者や受験生からの質問に対して、丁寧で分かりやすく親しみやすい言葉遣いで回答してください。

以下の【学校公式ナレッジ】を厳密に基づいて回答してください。ナレッジにない情報については想像で答えず、「入試広報部へ直接お問い合わせいただくか、公式Webサイトをご確認ください」と案内してください。

【学校公式ナレッジ】
{SCHOOL_KNOWLEDGE_TEXT}
"""
        response = model.generate_content(f"{system_instruction}\n\n【ユーザーからの質問】\n{user_message}")
        return response.text
    except Exception as e:
        return f"⚠️ Gemini API呼び出し時にエラーが発生しました: {str(e)}"

# 4. ヘッダー表示
st.markdown("""
<div class="school-header">
    <h1>🏫 東京学館浦安高等学校</h1>
    <div>
        <span class="motto-badge">校訓：自主・自学</span>
        <span class="motto-badge">A better me（カコイチ更新）</span>
    </div>
    <p>Gemini AI搭載！入試・コース・学費・学校生活など何でもご質問ください。</p>
</div>
""", unsafe_allow_html=True)

# APIキー設定状況のステータス表示
has_key = ("GEMINI_API_KEY" in st.secrets) or ("GEMINI_API_KEY" in os.environ) or (st.session_state.get("user_gemini_key"))

if has_key:
    st.markdown('<div class="ai-badge">✨ Gemini AIエンジン動作中（高度な自然言語対話モード）</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="ai-badge" style="background-color:#FFF3E0; color:#E65100;">💡 標準応答モード（サイドバーでGemini APIキーを設定すると生成AIモードになります）</div>', unsafe_allow_html=True)

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 設定・カスタマイズ")
    st.info("Google AI Studioで取得したGemini APIキーを設定すると、Gemini生成AIとの対話が可能になります。")
    input_key = st.text_input("Gemini API Key", type="password", key="gemini_key_input")
    if input_key:
        st.session_state.user_gemini_key = input_key
        st.success("APIキーを設定しました！")

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは！東京学館浦安高等学校の入試広報AIコンシェルジュです。どんなことでもお気軽にご質問ください！"}
    ]

# メッセージ履歴表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# チャット入力
if user_input := st.chat_input("質問を入力してください（例：特別進学コースの推薦基準と学費は？）"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Gemini AIが回答を作成中..."):
            ai_reply = get_gemini_response(SCHOOL_KNOWLEDGE_TEXT, user_input)
            
            # APIキー未設定の場合のルールベース・フォールバック
            if not ai_reply:
                if "学食" in user_input or "食堂" in user_input or "から揚げ" in user_input:
                    ai_reply = "【学食案内】本館1階に広く明るい食堂を完備。一番人気は「から揚げ丼」、日替わりランチ500円や4種の学館ラーメンも評判です。"
                elif "推薦" in user_input or "内申" in user_input or "基準" in user_input:
                    ai_reply = "【推薦出願基準（内申点）】全コース評定1なしが条件。\n・特進選抜: 5教科20以上\n・特進: 5教科18以上\n・総進: 5教科16以上/9教科29以上\n・国際教養: 5教科16以上/英語4以上\n・スポーツ: 9教科27以上"
                elif "学費" in user_input or "費用" in user_input or "授業料" in user_input:
                    ai_reply = "【学費案内】入学時納入金: 390,000円 / 月額授業料: 38,000円（国の就学支援金や千葉県授業料軽減制度の対象）"
                else:
                    ai_reply = f"ご質問「{user_input}」についてですね。より詳しい個別のご質問につきましては、入試広報部（TEL: 047-353-8821 / Mail: kouhou@gakkan-urayasu.ed.jp）までお気軽にお問い合わせください。"

            st.markdown(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
