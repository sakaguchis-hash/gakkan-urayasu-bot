import streamlit as st

# ページ基本設定（スマホ・タブレット対応：サイドバーは使わず、狭い画面でも読みやすい中央寄せレイアウト）
st.set_page_config(
    page_title="東京学館浦安高等学校 入試広報AIアシスタント",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 東京学館浦安高等学校 ブランドカラーCSS定義 (紺 #0B2545 / 金 #C5A059 / 白 #FFFFFF)
st.markdown("""
<style>
/* ===== 全体 ===== */
.stApp {
    background-color: #F8F9FA;
}
/* 画面幅いっぱいに使い、下部のチャット入力欄に隠れないよう余白を確保 */
.block-container {
    padding-top: 1.2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: calc(6rem + env(safe-area-inset-bottom, 0px));
    max-width: 760px;
}
/* 画像・表・コードなどのはみ出し防止 */
img, video, iframe { max-width: 100%; height: auto; }
[data-testid="stMarkdownContainer"] { overflow-wrap: anywhere; word-break: normal; }
[data-testid="stMarkdownContainer"] code { white-space: normal; }

/* ===== ヘッダーカード ===== */
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
    padding: 0;
    color: #FFFFFF;
    letter-spacing: 1px;
    line-height: 1.4;
}
.school-header .motto-badge {
    display: inline-block;
    background-color: #C5A059;
    color: #0B2545;
    font-size: 13px;
    font-weight: bold;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 4px 6px;
    line-height: 1.5;
}
.school-header p {
    font-size: 14px;
    color: #E0E1DD;
    margin-top: 10px;
    margin-bottom: 0;
    line-height: 1.7;
}

/* ===== サポート窓口カード ===== */
.support-card {
    background-color: #FFFFFF;
    color: #1F2933;
    border: 2px solid #C5A059;
    border-radius: 10px;
    padding: 18px;
    margin-top: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.support-card h4 {
    color: #0B2545;
    margin-top: 0;
    font-size: 16px;
    border-bottom: 2px solid #F0F2F5;
    padding-bottom: 8px;
}
.support-card ul { padding-left: 1.2rem; }
.support-card li { margin-bottom: 0.6rem; line-height: 1.7; }
.support-card a { color: #134074; font-weight: bold; }

/* ===== ボタン（指で押しやすい大きさ・長い文言は折り返す） ===== */
.stButton>button, .stFormSubmitButton>button {
    border-radius: 8px;
    font-weight: 600;
    min-height: 48px;
    height: auto;
    padding: 0.6rem 0.9rem;
    white-space: normal;
    line-height: 1.5;
}
.stButton>button p, .stFormSubmitButton>button p { white-space: normal; }

/* ===== スマートフォン（幅640px以下） ===== */
@media (max-width: 640px) {
    .block-container {
        padding-top: 0.8rem;
        padding-left: 0.6rem;
        padding-right: 0.6rem;
    }
    .school-header { padding: 16px 12px; margin-bottom: 14px; }
    .school-header h1 { font-size: 19px; letter-spacing: 0; }
    .school-header .motto-badge {
        display: block;
        font-size: 12px;
        margin: 6px auto;
        max-width: 100%;
    }
    .school-header p { font-size: 13px; }
    .support-card { padding: 14px 12px; }
    .support-card h4 { font-size: 15px; }
    /* チャット：余白とアイコンをコンパクトに */
    [data-testid="stChatMessage"] { padding: 0.6rem 0.3rem; gap: 0.5rem; }
    [data-testid="stChatMessage"] [data-testid^="stChatMessageAvatar"] {
        width: 2rem; height: 2rem; min-width: 2rem;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { font-size: 15px; line-height: 1.8; }
    /* iPhoneで入力時に画面が勝手に拡大されるのを防止（16px以上） */
    input, textarea, [data-testid="stChatInput"] textarea { font-size: 16px !important; }
    h3 { font-size: 1.1rem !important; }
}

/* ===== タブレット（幅641〜1024px） ===== */
@media (min-width: 641px) and (max-width: 1024px) {
    .block-container { max-width: 820px; padding-left: 1.5rem; padding-right: 1.5rem; }
    .school-header h1 { font-size: 26px; }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { font-size: 16px; line-height: 1.8; }
    input, textarea { font-size: 16px !important; }
}

/* ===== 横向きスマホなど高さが低い画面 ===== */
@media (max-height: 480px) {
    .school-header { padding: 12px; }
}
</style>
""", unsafe_allow_html=True)

# 学校ブランド・ヘッダー表示
st.markdown("""
<div class="school-header">
    <h1>🏫 東京学館浦安高等学校</h1>
    <div>
        <span class="motto-badge">校訓：自主・自学</span>
        <span class="motto-badge">スローガン：A better me（カコイチ更新）</span>
    </div>
    <p>入試広報部 AIナビゲーターへようこそ！受験・コース・学費など何でもご質問ください。</p>
</div>
""", unsafe_allow_html=True)

# 知識データベース (Q&Aデータ)
KNOWLEDGE_BASE = {
    "コース・教育方針": {
        "icon": "📚",
        "description": "4つのコースの特徴や教育目標についてのご案内です。",
        "items": {
            "特別進学コース（＋選抜）": """【特別進学コース（＋選抜）】
■ 概要: 国公立大学や難関私立大学の合格を目指すコースです。
■ 特徴:
・1年次から実践的なカリキュラムを展開。
・成績優秀者で編成される「特進選抜クラス」を設置。
・7限目の特別講座や長期休業中の講習で高い学力を錬成します。
■ 定員: 特別進学選抜 30名 / 特別進学 70名""",
            "総合進学コース（＋選抜）": """【総合進学コース（＋選抜）】
■ 概要: 大学・短大・専門学校進学から就職まで、幅広い進路に対応するメインコースです。
■ 特徴:
・基礎学力の定着から応用力強化まできめ細かく指導。
・2年次より文系・理系・特進選抜文理など希望に応じた選択が可能。
・部活動と勉強の両立（文武両道）を全力でバックアップ。
■ 定員: 260名""",
            "国際教養コース": """【国際教養コース】
■ 概要: 私大文系進学や海外留学、グローバル社会で活躍したい生徒向けのコースです。
■ 特徴:
・外国人講師による少人数英会話やネイティブ教員の副副担任制。
・希望者対象の「3か月間ニュージーランド留学プログラム」実施。
・英検・TOEIC等の資格取得サポートが充実。
■ 定員: 35名""",
            "スポーツ進学コース": """【スポーツ進学コース】
■ 概要: 学業と高い競技レベルのスポーツを両立させるコースです。
■ 特徴:
・全国大会レベルを目指す運動部に所属する生徒が中心。
・知性と競技力を備えた「優れたスポーツマン」を育成。
・スポーツ理論やトレーナー講習なども実施。
■ 定員: 35名""",
            "校訓・教育方針・スローガン": """【校訓・教育方針】
■ 校訓: 「自主・自学」 — 自分で選び、自分で伸びていく力
■ スローガン: 「A better me」= 昨日の自分を更新し続ける（カコイチ更新）
■ 3つの教育方針:
1. 自己の開発（個性の尊重と能力の伸長）
2. 判断と責任（正しい判断力と自己責任の確立）
3. 相互扶助（思いやりの心と協調性）"""
        }
    },
    "入試・出願・推薦基準": {
        "icon": "📝",
        "description": "令和9年度（2027年度）入試の要項や出願基準です。",
        "items": {
            "推薦入試の出願基準（内申点）": """【推薦入試 出願基準（内申点目安）】
全コース共通条件: 評定に「1」がないこと。
■ 特別進学選抜: 5教科「20以上」
■ 特別進学: 5教科「18以上」
■ 総合進学: 5教科「16以上」 または 9教科「29以上」
■ 国際教養: 5教科「16以上」 または 英語「4以上」
■ スポーツ進学: 9教科「27以上」＋部活動実績・運動適性
※加点ルール（1項目適用可能）:
・英検/漢検/数検 準2級以上: ＋2点
・英検/漢検/数検 3級: ＋1点
・3か年皆勤 / 生徒会役員 / 部活動3年継続（単願のみ）: ＋1点""",
            "試験日程・募集定員": """【試験日程・募集定員】
■ 募集定員: 計 430名
・特別進学選抜 30名 / 特別進学 70名 / 総合進学 260名 / 国際教養 35名 / スポーツ進学 35名
■ 入試日程（前期選抜）:
・第1期: 1月17日（単願推薦・併願推薦）
・第2期: 1月18日（単願推薦・併願推薦・一般）
・第3期: 1月29日（一般・追試験）""",
            "特待生制度": """【特待生制度（学費免除）】
入試成績および人物優秀者を対象とした特待生制度を用意しています。
■ 特待Ⅰ（A特待）:
・特典: 入学金・施設費および年間授業料の全額免除
■ 特待Ⅱ（B特待）:
・特典: 入学金の全額免除
※特進コース・スポーツコース等で基準を満たした生徒が対象となります。"""
        }
    },
    "学費・納入金": {
        "icon": "💰",
        "description": "入学時納入金や毎月の学費に関する情報です。",
        "items": {
            "入学時納入金の内訳": """【入学時納入金】合計 390,000円
■ 内訳:
・入学金: 150,000円
・教育振興費: 100,000円
・施設充実費: 70,000円
・後援会入会金: 20,000円
・施設設備協力金: 50,000円""",
            "月額費用と就学支援金": """【月額費用・就学支援金】
■ 月額授業料: 38,000円
■ 諸会費・積立金等: 別途（コースや学年により異なります）
※「高等学校等就学支援金（国の制度）」や千葉県の「授業料等軽減制度」が適用されると、世帯年収に応じて授業料負担が実質無料または大幅軽減されます。"""
        }
    },
    "学校生活・施設・学食": {
        "icon": "🍱",
        "description": "学食メニュー、校則、施設、部活動などのご案内です。",
        "items": {
            "学食・カフェテリア": """【学食・カフェテリア】
本館1階に広く明るい食堂を完備しています。
■ 一番人気: 「から揚げ丼」
■ 定番ランチ: 日替わりランチ（500円）
■ その他: 4種の学館ラーメン、カレーライス、うどん・そば、ドリンク・アイス自販機など""",
            "部活動一覧": """【部活動（全31部・同好会）】
運動部・文化部ともに活発に活動しています。
■ 運動部: テニス部、ハンドボール部、バスケットボール部、陸上競技部、サッカー部、ダンス部、野球部、剣道部 など
■ 文化部: 吹奏楽部、演劇部、書道部、美術部、パソコン部、インターアクトクラブ、軽音楽部 など""",
            "校則・持ち物・日課": """【校則・生活ルール・日課】
■ スマートフォン: 持ち込み可能（朝のSHR〜終礼までは個人のロッカーにて保管）
■ タブレット・端末: 個人で購入の必要はありません（校内整備端末を活用）
■ 登校時間: 朝のSHR 8:30開始 / 6限終了 15:20（放課後は部活・補習・自習スペース利用）"""
        }
    },
    "アクセス・問い合わせ": {
        "icon": "📍",
        "description": "所在地や交通アクセス、お問い合わせ先です。",
        "items": {
            "所在地・電話番号・メール": """【基本情報・お問い合わせ】
■ 学校名: 東京学館浦安高等学校
■ 所在地: 〒279-0023 千葉県浦安市高洲1-23-1
■ 電話番号: 047-353-8821（広報直通）
■ メール: kouhou@gakkan-urayasu.ed.jp""",
            "交通アクセス（最寄り駅）": """【交通アクセス】
■ JR京葉線「新浦安駅」より:
・東京ベイシティバス（高洲線等）で約10分、「東京学館浦安高校」下車徒歩1分。
■ 自転車通学: 浦安市内や近隣エリアからの自転車通学も可能です（敷地内駐輪場あり）。"""
        }
    }
}

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "こんにちは！東京学館浦安高等学校 入試広報ナビゲーターです。\n気になるカテゴリーを選択するか、キーワードを自由に入力しておたずねください！"}
    ]
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "show_support" not in st.session_state:
    st.session_state.show_support = False
if "scroll_latest" not in st.session_state:
    st.session_state.scroll_latest = False


def fmt(text):
    """改行を保持して表示（スマホの狭い画面でも項目ごとに行が分かれる）"""
    return text.replace("\n", "  \n")


def add_exchange(user_text, answer_text):
    """やり取りを履歴へ追加し、次の描画で最新の回答へ自動スクロールする"""
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.messages.append({"role": "assistant", "content": answer_text})
    st.session_state.scroll_latest = True


def scroll_to_latest():
    """スマホでは回答が画面の上側に表示されるため、最新の回答位置へスクロールする"""
    script = """
    <script>
    setTimeout(function () {
      try {
        var doc = window.parent.document;
        var msgs = doc.querySelectorAll('[data-testid="stChatMessage"]');
        if (msgs.length) {
          msgs[msgs.length - 1].scrollIntoView({behavior: 'smooth', block: 'start'});
        }
      } catch (e) {}
    }, 200);
    </script>
    """
    if hasattr(st, "iframe"):  # 新しいStreamlit
        st.iframe(script, height=1)
    else:  # 旧バージョン
        import streamlit.components.v1 as components
        components.html(script, height=0)


# メッセージ履歴表示
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(fmt(msg["content"]))

if st.session_state.scroll_latest:
    scroll_to_latest()
    st.session_state.scroll_latest = False


# 解決しなかった場合の個別サポート窓口（カード形式表示）
def render_support_widget():
    st.markdown("""
    <div class="support-card">
        <h4>🏫 入試広報部 相談・お問い合わせサポート</h4>
        <p>AIボットで解決しなかった疑問や、個別の事情（内申点のご相談、帰国生入試、個別相談会のご予約など）については、入試広報部の担当者が直接丁寧にお答えいたします。</p>
        <ul>
            <li>📞 <b>お電話でのご相談</b>: <a href="tel:0473538821">047-353-8821</a>（受付: 平日9:00〜16:30 / 土曜9:00〜13:00）</li>
            <li>📧 <b>メールでのお問い合せ</b>: <a href="mailto:kouhou@gakkan-urayasu.ed.jp">kouhou@gakkan-urayasu.ed.jp</a></li>
            <li>🏫 <b>学校説明会・個別相談会</b>: 実際の校舎見学や個別相談のご予約は公式HPより受付中</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📝 入試広報部へ直接質問・メッセージを送信する"):
        with st.form(key="unresolved_form"):
            user_name = st.text_input("お名前（任意）")
            contact_info = st.text_input("ご連絡先（メールアドレスまたはお電話番号）")
            question_detail = st.text_area("ご質問・ご相談内容", placeholder="例：特進コースの併願推薦基準について詳しく聞きたいです。")
            submit_btn = st.form_submit_button("入試広報部へ送信する", use_container_width=True)

            if submit_btn:
                if question_detail:
                    st.success("✅ 送信が完了しました。入試広報部の担当者より追ってご連絡いたします。")
                else:
                    st.warning("⚠️ ご質問内容を入力してください。")


if st.session_state.show_support:
    render_support_widget()

st.markdown("---")

# 未解決サポートボタン
# （スマホでは自動で縦並びになる。ボタンは常に横幅いっぱいで押しやすくする）
col_supp1, col_supp2 = st.columns([2, 1])
with col_supp1:
    st.write("💡 **疑問が解決しない・個別に相談したい場合**")
with col_supp2:
    if st.button("❓ 担当者に直接相談する", type="secondary", use_container_width=True):
        st.session_state.show_support = not st.session_state.show_support
        st.rerun()

st.markdown("### 💡 カテゴリーから探す（選択ナビゲーション）")

# ステップ1: 大カテゴリー選択ボタン
# （PC・タブレットは2列、スマホは自動で1列表示）
col1, col2 = st.columns(2)
categories = list(KNOWLEDGE_BASE.keys())
for idx, cat_name in enumerate(categories):
    cat_data = KNOWLEDGE_BASE[cat_name]
    btn_label = f"{cat_data['icon']} {cat_name}"
    target_col = col1 if idx % 2 == 0 else col2
    if target_col.button(btn_label, use_container_width=True, key=f"cat_{idx}"):
        st.session_state.selected_category = cat_name
        st.session_state.show_support = False
        st.rerun()

# ステップ2: 選択された大カテゴリー内の小項目ボタンを表示
if st.session_state.selected_category:
    selected_cat = st.session_state.selected_category
    cat_data = KNOWLEDGE_BASE[selected_cat]
    st.info(f"📂 **選択中: {cat_data['icon']} {selected_cat}** — {cat_data['description']}")

    sub_items = list(cat_data["items"].keys())
    st.write("▼ 知りたい項目をタップしてください:")

    for sub_key in sub_items:
        if st.button(f"👉 {sub_key}", use_container_width=True, key=f"sub_{sub_key}"):
            answer_text = cat_data["items"][sub_key]
            add_exchange(f"【選択】{sub_key}", answer_text)
            st.session_state.selected_category = None
            st.rerun()

    if st.button("🔄 最初に戻る（カテゴリー選択を解除）", type="secondary", use_container_width=True):
        st.session_state.selected_category = None
        st.rerun()

st.markdown("---")

# 自由入力チャット
if user_input := st.chat_input("キーワードや質問を入力（例：推薦基準の内申点は？）"):
    matched_answer = None

    for cat_name, cat_data in KNOWLEDGE_BASE.items():
        for sub_name, detail in cat_data["items"].items():
            if ("学食" in user_input or "食堂" in user_input or "ランチ" in user_input) and "学食" in sub_name:
                matched_answer = detail
                break
            elif ("コース" in user_input or "特進" in user_input or "総進" in user_input or "国際" in user_input or "スポーツ" in user_input) and "コース" in cat_name:
                matched_answer = detail
                break
            elif any(k in user_input for k in ["推薦", "内申", "基準", "出願", "入試", "併願", "単願"]) and "入試" in cat_name:
                matched_answer = detail
                break
            elif any(k in user_input for k in ["学費", "費用", "授業料", "納入金", "就学支援金"]) and "学費" in cat_name:
                matched_answer = detail
                break
            elif any(k in user_input for k in ["アクセス", "場所", "バス", "駅", "住所", "電話"]) and "アクセス" in cat_name:
                matched_answer = detail
                break

    if not matched_answer:
        matched_answer = f"ご質問「{user_input}」に関する詳しい情報が見つかりませんでした。\n\n上のカテゴリーボタンから該当する項目をお探しいただくか、下の**「❓ 担当者に直接相談する」**ボタンより入試広報部へお電話・メール・お問い合わせフォームにて直接ご相談いただけます。"
        st.session_state.show_support = True

    add_exchange(user_input, matched_answer)
    st.rerun()
