import streamlit as st
import re
import difflib

# ページ基本設定
st.set_page_config(
    page_title="東京学館浦安高等学校 AI入試広報ナビ",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 洗練されたエンタープライズ風カスタムCSS（Intercom / Zendesk / LINE AI風）
st.markdown("""
<style>
    /* 全体スタイリング */
    .stApp {
        background-color: #F4F6F9;
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
    }
    
    /* ブランドヘッダー */
    .brand-header {
        background: linear-gradient(135deg, #0B2545 0%, #134074 100%);
        color: #FFFFFF;
        padding: 24px 20px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(11, 37, 69, 0.15);
        text-align: center;
        margin-bottom: 24px;
        border-bottom: 4px solid #C5A059;
        position: relative;
    }
    .brand-header h1 {
        font-size: 22px;
        font-weight: 800;
        margin: 0 0 10px 0;
        color: #FFFFFF;
        letter-spacing: 0.8px;
    }
    .motto-pill {
        display: inline-block;
        background: rgba(197, 160, 89, 0.2);
        border: 1px solid #C5A059;
        color: #F3E5AB;
        font-size: 12px;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin: 2px 4px;
    }
    .brand-subtitle {
        font-size: 13px;
        color: #E0E1DD;
        margin-top: 10px;
    }

    /* AIステータスバッジ */
    .ai-badge {
        display: inline-flex;
        align-items: center;
        background-color: #EBF3FF;
        color: #0B2545;
        border: 1px solid #B8D5FF;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .ai-badge span {
        height: 8px;
        width: 8px;
        background-color: #28A745;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(40, 167, 69, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }
    }

    /* クイックアクションチップ */
    .quick-chip-title {
        font-size: 13px;
        font-weight: bold;
        color: #555555;
        margin-bottom: 8px;
    }

    /* フィードバックカード */
    .feedback-box {
        background-color: #FFFFFF;
        border-left: 4px solid #C5A059;
        padding: 12px 16px;
        border-radius: 8px;
        margin-top: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        font-size: 13px;
    }

    /* お問い合わせカード */
    .escalation-card {
        background-color: #FFFFFF;
        border: 2px solid #0B2545;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .escalation-card h3 {
        color: #0B2545;
        font-size: 16px;
        margin-top: 0;
        border-bottom: 2px solid #F0F2F5;
        padding-bottom: 8px;
    }

    /* ボタンカスタマイズ */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# ヘッダー表示
st.markdown("""
<div class="brand-header">
    <h1>🏫 東京学館浦安高等学校</h1>
    <div>
        <span class="motto-pill">校訓：自主・自学</span>
        <span class="motto-pill">スローガン：A better me（カコイチ更新）</span>
    </div>
    <div class="brand-subtitle">入試広報部 スマートAIコンシェルジュ</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ai-badge">
    <span></span> AI自然言語解析エンジン稼働中（2027年度最新要項対応）
</div>
""", unsafe_allow_html=True)

# 知識データベース (Q&Aデータ＋タグ＋関連Q&Aマッピング)
KNOWLEDGE_BASE = {
    "コース・教育方針": {
        "icon": "📚",
        "description": "4つのコースの特徴・教育目標・カリキュラムのご案内です。",
        "items": {
            "特別進学コース（＋選抜）": {
                "answer": """【特別進学コース（＋選抜）】
■ 概要: 国公立大学や難関私立大学（早慶上理・GMARCH等）の現役合格を目指す高水準カリキュラム。
■ 主な特徴:
  ・1年次から実践的演習を実施。成績優秀者による「特進選抜クラス」を編成。
  ・7限目の特別補習講座や長期休業中の集中講習を無料開講。
  ・国公立文系・理系、私立文系・理系の細やかな選択が可能。
■ 募集定員: 特進選抜 30名 / 特進 70名""",
                "tags": ["特進", "選抜", "大学受験", "国公立", "難関私大", "勉強", "講習"],
                "related": ["推薦入試の出願基準（内申点）", "特待生制度", "校訓・教育方針・スローガン"]
            },
            "総合進学コース（＋選抜）": {
                "answer": """【総合進学コース（＋選抜）】
■ 概要: 大学・短大・専門学校・就職まで、幅広い進路に対応する本校のメインコースです。
■ 主な特徴:
  ・基礎学力の定着から応用力強化まで丁寧な段階指導。
  ・2年次より「文系・理系・特進選抜文理」など多様な志向に合わせ選択。
  ・部活動（全国レベル含む）と勉強の両立（文武両道）を全力サポート。
■ 募集定員: 260名""",
                "tags": ["総進", "総合進学", "部活両立", "文武両道", "大学進学", "専門学校"],
                "related": ["推薦入試の出願基準（内申点）", "部活動一覧", "学食・カフェテリア"]
            },
            "国際教養コース": {
                "answer": """【国際教養コース】
■ 概要: 私大文系進学、海外大学、グローバル社会で活躍を目指す英語重視コースです。
■ 主な特徴:
  ・外国人講師による少人数実践英会話やネイティブ教員の副副担任制。
  ・希望者対象の「3か月間ニュージーランド留学プログラム」（単位認定可）。
  ・英検・TOEIC資格取得に向けた専用対策講座。
■ 募集定員: 35名""",
                "tags": ["国際", "英語", "留学", "ニュージーランド", "英検", "海外"],
                "related": ["推薦入試の出願基準（内申点）", "特別進学コース（＋選抜）", "校訓・教育方針・スローガン"]
            },
            "スポーツ進学コース": {
                "answer": """【スポーツ進学コース】
■ 概要: 学業とトップレベルのスポーツ競技力を高度に両立させるコースです。
■ 主な特徴:
  ・全国大会・関東大会を目指す各運動部に所属する生徒が中心。
  ・知性と競技力を兼ね備えた「優れたアスリート」を育成。
  ・スポーツ理論、コンディショニング、トレーナー実習等も展開。
■ 募集定員: 35名""",
                "tags": ["スポーツ", "部活", "運動部", "アスリート", "全国大会", "野球", "テニス"],
                "related": ["部活動一覧", "推薦入試の出願基準（内申点）", "特待生制度"]
            },
            "校訓・教育方針・スローガン": {
                "answer": """【校訓・教育方針・スローガン】
■ 校訓: 「自主・自学」 — 自分で選び、自分で伸びていく自立した力
■ スローガン: 「A better me」= 昨日の自分を更新し続ける（カコイチ更新）
■ 3つの教育方針:
  1. 自己の開発（個性の尊重と隠れた能力の伸長）
  2. 判断と責任（正しい判断力と自己責任感の育成）
  3. 相互扶助（思いやりの心と豊かな協調性）""",
                "tags": ["校訓", "教育方針", "スローガン", "自主自学", "Abetterme", "理念"],
                "related": ["特別進学コース（＋選抜）", "総合進学コース（＋選抜）", "校則・持ち物・日課"]
            }
        }
    },
    "入試・出願・推薦基準": {
        "icon": "📝",
        "description": "令和9年度（2027年度）最新の入試要項・内申点基準・特待制度です。",
        "items": {
            "推薦入試の出願基準（内申点）": {
                "answer": """【推薦入試 出願基準（内申点目安）】
※全コース共通必須条件: 評定に「1」がないこと。

■ 特別進学選抜: 5教科「20以上」
■ 特別進学: 5教科「18以上」
■ 総合進学: 5教科「16以上」 または 9教科「29以上」
■ 国際教養: 5教科「16以上」 または 英語評定「4以上」
■ スポーツ進学: 9教科「27以上」＋運動部実績・適性審査

※加点優遇制度（1項目適用可能）:
  ・英検/漢検/数検 準2級以上: ＋2点
  ・英検/漢検/数検 3級: ＋1点
  ・3か年皆勤 / 生徒会役員 / 部活動3年間継続（単願のみ）: ＋1点
  ・数学または英語の評定「5」保有者: 各＋1点加点可""",
                "tags": ["推薦", "内申", "基準", "出願", "単願", "併願", "加点", "英検", "テスト"],
                "related": ["試験日程・募集定員", "特待生制度", "特別進学コース（＋選抜）"]
            },
            "試験日程・募集定員": {
                "answer": """【試験日程・募集定員】
■ 募集定員: 合計 430名
  （特進選抜 30名 / 特進 70名 / 総進 260名 / 国際 35名 / スポーツ 35名）

■ 入試日程（前期選抜）:
  ・第1期: 1月17日（単願推薦・併願推薦）
  ・第2期: 1月18日（単願推薦・併願推薦・一般）
  ・第3期: 1月29日（一般入試・追試験）

■ 選考方法: 調査書、学科試験（国・数・英）、面接（単願推奨）""",
                "tags": ["日程", "試験", "定員", "1月", "面接", "併願", "一般入試"],
                "related": ["推薦入試の出願基準（内申点）", "入学時納入金の内訳", "特待生制度"]
            },
            "特待生制度": {
                "answer": """【特待生制度（学費免除）】
本校では学業成績およびスポーツ実績が優秀な生徒を対象に特待生制度を用意しています。

■ 特待Ⅰ（A特待）:
  ・特典: 入学金・施設費および年間授業料の全額免除
■ 特待Ⅱ（B特待）:
  ・特典: 入学金の全額免除

※特進コースの学業優秀者およびスポーツ進学コースの競技実績優秀者が対象となります。""",
                "tags": ["特待生", "免除", "学費免除", "奨学金", "特待", "成績優秀"],
                "related": ["推薦入試の出願基準（内申点）", "入学時納入金の内訳", "月額費用と就学支援金"]
            }
        }
    },
    "学費・納入金": {
        "icon": "💰",
        "description": "入学金、施設費、月額授業料、就学支援金についてのご案内です。",
        "items": {
            "入学時納入金の内訳": {
                "answer": """【入学時納入金】合計 390,000円
■ 内訳:
  ・入学金: 150,000円
  ・教育振興費: 100,000円
  ・施設充実費: 70,000円
  ・後援会入会金: 20,000円
  ・施設設備協力金: 50,000円

※合格発表後、指定期日までに入金手続きを行っていただきます。""",
                "tags": ["入学金", "納入金", "施設費", "費用", "振込", "手続き"],
                "related": ["月額費用と就学支援金", "特待生制度", "試験日程・募集定員"]
            },
            "月額費用と就学支援金": {
                "answer": """【月額費用・就学支援金】
■ 月額授業料: 38,000円
■ 諸会費・積立金等: 別途（コース・学年により異なります）

※【公的支援制度】:
  国の「高等学校等就学支援金」や千葉県の「授業料等軽減制度」が適用された場合、世帯年収に応じて授業料負担が「実質0円」または大幅軽減されます。""",
                "tags": ["授業料", "月額", "就学支援金", "軽減", "無料", "実質無償化", "学費"],
                "related": ["入学時納入金の内訳", "特待生制度", "学食・カフェテリア"]
            }
        }
    },
    "学校生活・施設・学食": {
        "icon": "🍱",
        "description": "学食メニュー、31の部活動、校則や日課についてのご案内です。",
        "items": {
            "学食・カフェテリア": {
                "answer": """【学食・カフェテリア（本館1階）】
明るく広々としたカフェテリアで、温かい手作りメニューを提供しています。

■ 名物・一番人気: 「から揚げ丼」
■ 日替わりランチ: 500円（ワンコイン）
■ その他人気メニュー: 4種の学館ラーメン、カツカレー、うどん・そば、フライドポテト
■ 設備: ドリンク自販機、アイス自販機、電子レンジ完備""",
                "tags": ["学食", "食堂", "から揚げ丼", "ランチ", "ラーメン", "昼食", "自販機"],
                "related": ["校則・持ち物・日課", "部活動一覧", "総合進学コース（＋選抜）"]
            },
            "部活動一覧": {
                "answer": """【部活動（全31部・同好会）】
文武両道を掲げ、多くの生徒が部活動に参加しています。

■ 運動部（全17部）:
  テニス部、ハンドボール部、バスケットボール部、陸上競技部、サッカー部、ダンス部、硬式野球部、剣道部、バレーボール部、バドミントン部 など
■ 文化部（全14部）:
  吹奏楽部、演劇部、書道部、美術部、パソコン部、インターアクトクラブ、軽音楽部、茶道部 など""",
                "tags": ["部活", "部活動", "運動部", "文化部", "テニス", "吹奏楽", "野球", "ハンドボール"],
                "related": ["スポーツ進学コース", "学食・カフェテリア", "校則・持ち物・日課"]
            },
            "校則・持ち物・日課": {
                "answer": """【校則・生活ルール・日課】
■ スマートフォン: 持参可能（朝のSHR〜終礼までは個人の施錠ロッカーにて保管）
■ 学習端末（タブレット）: 校内にWi-Fiおよび整備端末があるため、高額な個人購入は不要。
■ 登校・日課:
  ・朝のSHR 8:30開始
  ・6限終了 15:20（全コース6限統一。放課後は部活・補習・自習スペース利用）""",
                "tags": ["校則", "スマホ", "携帯", "タブレット", "登校時間", "日課", "校舎"],
                "related": ["アクセス・所在地", "学食・カフェテリア", "校訓・教育方針・スローガン"]
            }
        }
    },
    "アクセス・所在地": {
        "icon": "📍",
        "description": "所在地、最寄り駅、バス案内、お問い合わせ先です。",
        "items": {
            "アクセス・所在地・連絡先": {
                "answer": """【基本情報・アクセス】
■ 学校名: 東京学館浦安高等学校（学校法人鎌形学園）
■ 所在地: 〒279-0023 千葉県浦安市高洲1-23-1
■ 電話番号: 047-353-8821（入試広報直通）
■ メール: kouhou@gakkan-urayasu.ed.jp

■ 交通アクセス:
  ・JR京葉線「新浦安駅」南口より東京ベイシティバス（高洲線等）で約10分、「東京学館浦安高校」バス停下車徒歩1分。
  ・浦安市内・市川市・江戸川区等からの自転車通学も可能（敷地内駐輪場完備）。""",
                "tags": ["アクセス", "場所", "住所", "新浦安", "バス", "電話", "メール", "行き方", "駐輪場"],
                "related": ["試験日程・募集定員", "校則・持ち物・日課", "学食・カフェテリア"]
            }
        }
    }
}

# 自然言語AIマッチングエンジン（スコアリングアルゴリズム）
def find_best_answers(query_text, top_n=3):
    query_text_clean = query_text.lower().strip()
    scores = []
    
    for cat_name, cat_data in KNOWLEDGE_BASE.items():
        for item_title, item_data in cat_data["items"].items():
            score = 0.0
            
            # 1. タイトル完全/部分一致
            if query_text_clean in item_title.lower():
                score += 5.0
            
            # 2. タグ一致（重み高）
            for tag in item_data["tags"]:
                if tag.lower() in query_text_clean or query_text_clean in tag.lower():
                    score += 3.5
            
            # 3. 本文類似度（文字n-gram・部分一致）
            for line in item_data["answer"].split("\n"):
                if any(w in line for w in query_text_clean.split()):
                    score += 1.0
            
            # 4. difflib シーケンスマッチ
            ratio = difflib.SequenceMatcher(None, query_text_clean, item_title).ratio()
            score += ratio * 2.0
            
            if score > 0.8:
                scores.append({
                    "title": item_title,
                    "category": cat_name,
                    "answer": item_data["answer"],
                    "related": item_data["related"],
                    "score": score
                })
                
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_n]

# セッション状態初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "こんにちは！東京学館浦安高等学校 入試広報AIアシスタントです。🤖\n\nコース・内申点基準・学費・学食・部活動など、知りたいことを下のクイックボタンか入力欄からお気軽におたずねください！",
            "feedback": None
        }
    ]

if "show_escalation" not in st.session_state:
    st.session_state.show_escalation = False

# メッセージ履歴表示
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # アシスタント回答へのEnterprise風フィードバックUI（役に立ちましたか？ 👍 👎）
        if msg["role"] == "assistant" and idx > 0:
            col_fb1, col_fb2, col_fb3 = st.columns([3, 1, 1])
            with col_fb1:
                st.caption("この回答は役に立ちましたか？")
            with col_fb2:
                if st.button("👍 役に立った", key=f"thumb_up_{idx}"):
                    st.toast("フィードバックありがとうございます！", icon="✨")
            with col_fb3:
                if st.button("👎 解決しない", key=f"thumb_down_{idx}"):
                    st.session_state.show_escalation = True
                    st.toast("直接相談窓口をご案内いたします。", icon="ℹ️")
                    st.rerun()

# 解決しなかった場合の問い合わせ（エスカレーション）カード
if st.session_state.show_escalation:
    st.markdown("""
    <div class="escalation-card">
        <h3>🏫 入試広報部へ直接ご相談・お問い合わせ</h3>
        <p>AIボットで解決しなかった疑問や個別の内申点のご相談・学校見学のご予約は、入試広報スタッフが迅速に対応いたします。</p>
        <ul>
            <li>📞 <b>お電話（直通）</b>: <code>047-353-8821</code>（受付: 平日9:00〜16:30 / 土曜9:00〜13:00）</li>
            <li>📧 <b>メールアドレス</b>: <a href="mailto:kouhou@gakkan-urayasu.ed.jp">kouhou@gakkan-urayasu.ed.jp</a></li>
            <li>🌐 <b>公式Web予約</b>: 学校説明会・個別相談会のご予約はHPより受付中</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📝 メッセージ・相談内容を送信する"):
        with st.form(key="contact_form"):
            name = st.text_input("お名前（保護者様・受験生）")
            contact = st.text_input("ご連絡先（メールまたはお電話番号）")
            body = st.text_area("ご相談・ご質問内容")
            submitted = st.form_submit_button("入試広報部へ送信")
            if submitted:
                if body:
                    st.success("✅ 送信が完了しました。担当者より折り返しご連絡いたします。")
                else:
                    st.warning("内容を入力してください。")

st.markdown("---")

# よく検索される質問クイックチップ（Enterpriseスタイル）
st.markdown("<div class='quick-chip-title'>🔥 よく検索される質問 TOP 4（クリックで即時回答）:</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

quick_queries = [
    ("推薦基準（内申点）", "推薦入試の出願基準（内申点）"),
    ("学費・納入金内訳", "入学時納入金の内訳"),
    ("から揚げ丼（学食）", "学食・カフェテリア"),
    ("部活動一覧", "部活動一覧")
]

for col, (label, target_title) in zip([c1, c2, c3, c4], quick_queries):
    if col.button(f"💡 {label}", use_container_width=True, key=f"quick_{label}"):
        # ターゲットのQ&Aを取得して即時表示
        found_item = None
        for cat_data in KNOWLEDGE_BASE.values():
            if target_title in cat_data["items"]:
                found_item = cat_data["items"][target_title]
                break
        if found_item:
            st.session_state.messages.append({"role": "user", "content": target_title})
            
            res_content = found_item["answer"] + "\n\n---\n**💡 関連するおすすめ質問:**\n"
            for rel in found_item["related"]:
                res_content += f"・`{rel}`\n"
                
            st.session_state.messages.append({"role": "assistant", "content": res_content, "feedback": None})
            st.rerun()

st.markdown("---")

# インタラクティブ・アコーディオンカテゴリー
st.markdown("### 📂 カテゴリーから絞り込む")
for cat_name, cat_data in KNOWLEDGE_BASE.items():
    with st.expander(f"{cat_data['icon']} {cat_name} — {cat_data['description']}"):
        for item_title, item_info in cat_data["items"].items():
            if st.button(f"👉 {item_title}", key=f"btn_{cat_name}_{item_title}"):
                st.session_state.messages.append({"role": "user", "content": item_title})
                
                ans_text = item_info["answer"] + "\n\n---\n**💡 関連する質問:**\n"
                for rel in item_info["related"]:
                    ans_text += f"・`{rel}`\n"
                    
                st.session_state.messages.append({"role": "assistant", "content": ans_text, "feedback": None})
                st.rerun()

st.markdown("---")

# 自然言語AIチャット入力
if user_input := st.chat_input("何でも自由にご質問ください（例：特進コースの推薦基準や加点は？）"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AIマッチングエンジンで検索
    matches = find_best_answers(user_input, top_n=3)
    
    if matches and matches[0]["score"] >= 2.0:
        best = matches[0]
        response_text = f"ご質問「**{user_input}**」に関する回答です：\n\n" + best["answer"]
        
        # 関連質問の提案
        if best["related"]:
            response_text += "\n\n---\n**💡 関連するよくある質問:**\n"
            for rel in best["related"]:
                response_text += f"・`{rel}`\n"
    elif matches:
        # 候補を表示
        response_text = f"「**{user_input}**」についての質問ですね！以下の関連項目が該当する可能性があります：\n\n"
        for m in matches:
            response_text += f"### 📌 {m['title']}\n{m['answer']}\n\n---\n"
    else:
        # 未解決エスカレーション誘導
        response_text = f"申し訳ありません。「**{user_input}**」に関する直接的な回答が見つかりませんでした。\n\n上のカテゴリー一覧から探していただくか、下の**「入試広報部へ直接ご相談」**フォームよりお気軽にお問い合わせください。"
        st.session_state.show_escalation = True

    st.session_state.messages.append({"role": "assistant", "content": response_text, "feedback": None})
    st.rerun()
