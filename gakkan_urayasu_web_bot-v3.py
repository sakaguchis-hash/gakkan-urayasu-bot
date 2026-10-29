import streamlit as st

# ページ設定
st.set_page_config(
    page_title="東京学館浦安高等学校 自動案内ボット",
    page_icon="🏫",
    layout="centered"
)

st.title("🏫 東京学館浦安高等学校 自動案内ボット")
st.caption("楽天市場風のカテゴリー選択ボタンで、知りたい情報を簡単に探せます。自由入力も可能です！")

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
■ 定員: 特別進学選抜30名 / 特別進学70名""",
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
        {"role": "assistant", "content": "こんにちは！東京学館浦安高等学校の自動応答ボットです。\n知りたい分野や項目を下の選択肢ボタンから選んでください。直接質問を入力することも可能です！"}
    ]

if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# 過去のメッセージ表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

st.markdown("---")
st.subheader("💡 項目から選んで質問する（選択肢ナビゲーション）")

# ステップ1: 大カテゴリー選択ボタン
col1, col2 = st.columns(2)
categories = list(KNOWLEDGE_BASE.keys())

for idx, cat_name in enumerate(categories):
    cat_data = KNOWLEDGE_BASE[cat_name]
    btn_label = f"{cat_data['icon']} {cat_name}"
    
    target_col = col1 if idx % 2 == 0 else col2
    if target_col.button(btn_label, use_container_width=True, key=f"cat_{idx}"):
        st.session_state.selected_category = cat_name
        st.rerun()

# ステップ2: 選択された大カテゴリー内の小項目ボタンを表示
if st.session_state.selected_category:
    selected_cat = st.session_state.selected_category
    cat_data = KNOWLEDGE_BASE[selected_cat]
    
    st.info(f"📂 **選択中: {cat_data['icon']} {selected_cat}** — {cat_data['description']}")
    
    sub_items = list(cat_data["items"].keys())
    
    st.write("▼ 知りたい項目をクリックしてください:")
    for sub_key in sub_items:
        if st.button(f"👉 {sub_key}", use_container_width=True, key=f"sub_{sub_key}"):
            answer_text = cat_data["items"][sub_key]
            
            st.session_state.messages.append({"role": "user", "content": f"【選択】{sub_key}"})
            st.session_state.messages.append({"role": "assistant", "content": answer_text})
            
            st.session_state.selected_category = None
            st.rerun()

    if st.button("🔄 最初に戻る（カテゴリー選択を解除）", type="secondary"):
        st.session_state.selected_category = None
        st.rerun()

st.markdown("---")

# 自由入力チャット
if user_input := st.chat_input("自由なキーワードや質問を入力できます（例：学食の人気メニューは？）"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    matched_answer = None
    for cat_name, cat_data in KNOWLEDGE_BASE.items():
        for sub_name, detail in cat_data["items"].items():
            if "学食" in user_input and "学食" in sub_name:
                matched_answer = detail
                break
            elif "コース" in user_input and "コース" in cat_name:
                matched_answer = detail
                break
            elif any(k in user_input for k in ["推薦", "内申", "基準", "入試"]) and "入試" in cat_name:
                matched_answer = detail
                break
            elif any(k in user_input for k in ["学費", "費用", "授業料"]) and "学費" in cat_name:
                matched_answer = detail
                break
            elif any(k in user_input for k in ["アクセス", "場所", "バス"]) and "アクセス" in cat_name:
                matched_answer = detail
                break

    if not matched_answer:
        matched_answer = f"「{user_input}」についてですね！上のボタンからカテゴリー（【コース・教育方針】【入試・出願・推薦基準】【学費・納入金】【学校生活】など）を選択いただくと、より詳しい情報をご確認いただけます。"

    st.session_state.messages.append({"role": "assistant", "content": matched_answer})
    st.rerun()
