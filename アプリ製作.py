import streamlit as st
import re
import streamlit.components.v1 as components
import random#ランダム


TWEMOJI_BASE_URL = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/svg"

QUIZ_DATA = [
    {"image_url": "1f600", "answer": "にこやかな笑顔", "keywords": ["にこやか"]},
    {"image_url": "1f604", "answer": "目もにこやかな笑顔", "keywords": ["目もにこやか", "めもにこやか", "にこやか"]},
    {"image_url": "1f603", "answer": "大きい目の笑顔", "keywords": ["大きい目", "おおきいめ", "大きい", "おおきい"]},
    {"image_url": "1f601", "answer": "輝く笑顔", "keywords": ["輝く", "かがやく"]},
    {"image_url": "1f606", "answer": "大笑いの顔", "keywords": ["大笑い", "おおわらい","わらい","笑い"]},
    {"image_url": "1f605", "answer": "汗をかいた笑顔", "keywords": ["汗", "あせ"]},
    {"image_url": "1f923", "answer": "笑い転げる顔", "keywords": ["笑い転げる", "わらいころげる", "転げる", "ころげる"]},
    {"image_url": "1f602", "answer": "目もにこやかな笑顔", "keywords": ["目もにこやか", "めもにこやか", "にこやか", "嬉し泣き", "うれしなき"]},
    {"image_url": "1f642", "answer": "控え目な笑顔", "keywords": ["控え目", "控えめ", "ひかえめ"]},
    {"image_url": "1f643", "answer": "逆さまの顔", "keywords": ["逆さま", "さかさま", "逆さ", "さかさ"]},
    {"image_url": "1f609", "answer": "ウィンクの顔", "keywords": ["ウィンク", "ウインク"]},
    {"image_url": "1fae0", "answer": "溶ける顔", "keywords": ["溶ける", "とける"]},
    {"image_url": "1f60a", "answer": "微笑む目の笑顔", "keywords": ["微笑む", "ほほえむ", "微笑み", "ほほえみ"]},
    {"image_url": "1f607", "answer": "天使の輪がついた笑顔", "keywords": ["天使", "てんし"]},
    {"image_url": "1f637", "answer": "マスク顔", "keywords": ["マスク"]},
    {"image_url": "1f914", "answer": "試行中の顔", "keywords": ["試行", "思考", "しこう"]},
    {"image_url": "1f917", "answer": "ハグの顔", "keywords": ["ハグ"]},
    {"image_url": "1f92b", "answer": "静かにの顔", "keywords": ["静か", "しずか"]},
    {"image_url": "1f913", "answer": "オタク顔", "keywords": ["オタク"]},
    {"image_url": "1f60e", "answer": "サングラスの笑顔", "keywords": ["サングラス"]},
    {"image_url": "1f60c", "answer": "ほっとした顔", "keywords": ["ほっと"]},
    {"image_url": "1f614", "answer": "物思いの顔", "keywords": ["物思い", "ものおもい"]},
    {"image_url": "1f62a", "answer": "眠い顔", "keywords": ["眠い", "ねむい"]},
    {"image_url": "1f924", "answer": "よだれ顔", "keywords": ["よだれ"]},
    {"image_url": "1f634", "answer": "寝てる顔", "keywords": ["寝てる", "ねてる", "寝ている", "ねている"]},
    {"image_url": "1f615", "answer": "混乱した顔", "keywords": ["混乱", "こんらん"]},
    {"image_url": "1f979", "answer": "涙をこらえている顔", "keywords": ["こらえて", "涙", "なみだ"]},
    {"image_url": "1f622", "answer": "泣き顔", "keywords": ["泣き", "なき"]},
    {"image_url": "1f62d", "answer": "大声で泣いている顔", "keywords": ["大声", "おおごえ"]},
    {"image_url": "1f631", "answer": "恐怖で叫ぶ顔", "keywords": ["恐怖", "きょうふ", "叫ぶ", "さけぶ"]},
]

#ひらがなカタカナ混ざってもOKにするためにつかえそうなもの
def hira_to_kata(text: str) -> str:
    """ひらがなをカタカナに変換する"""
    return "".join(
        chr(ord(c) + 0x60) if "ぁ" <= c <= "ゖ" else c
        for c in text
    )

def normalize(text: str) -> str:
    """空白（半角・全角）を除去し、カタカナに統一する"""
    no_space = re.sub(r"\s+", "", text)
    return hira_to_kata(no_space)

def check_answer(user_input: str, keywords: list[str]) -> bool:
    """ユーザー入力に正解キーワードのいずれかが含まれるか判定する"""
    norm_user = normalize(user_input)
    if not norm_user:
        return False
    return any(normalize(kw) in norm_user for kw in keywords)

def reset_quiz_state() -> None:
    """回答入力欄の履歴と採点フラグをリセットする"""
    for key in list(st.session_state.keys()):
        if isinstance(key, str) and key.startswith("answer_"):
            del st.session_state[key]
    st.session_state.submitted = False

#画面上部への移動
def scroll_to_quiz_top() -> None:
    """再描画時にクイズ上部（id='quiz-top'）へ滑らかにスクロールする"""
    if not st.session_state.get("scroll_top", False):
        return
    components.html(
        f"""
        <!-- {random.random()} -->
        <script>
            // 画面の描画が終わるのを0.15秒待ってから移動開始
            setTimeout(function() {{
                const target = window.parent.document.getElementById("quiz-top");
                if (target) {{
                    target.scrollIntoView({{ behavior: "smooth", block: "start" }});
                }}
            }}, 150);
        </script>
        """,
        height=0,
    )
    st.session_state.scroll_top = False

#題名
st.set_page_config(page_title="顔文字名称あてクイズ", page_icon="🤔")
st.title("顔文字の名称を当てるクイズ")

scroll_to_quiz_top()

#問題数選択
available_counts = [n for n in (10, 20, 30) if n <= len(QUIZ_DATA)]
num_questions = st.radio(#問題数選択の流れ
    "出題する問題数を選んでください",
    available_counts,#問題数選択肢選択
    horizontal=True,
)

#初回表示または問題数が変更された場合に問題リストを再作成
if "quiz_list" not in st.session_state or st.session_state.get("num_questions") != num_questions:
    st.session_state.quiz_list = random.sample(QUIZ_DATA, num_questions)
    st.session_state.num_questions = num_questions
    reset_quiz_state()
quiz_list = st.session_state.quiz_list
submitted = st.session_state.get("submitted", False)

#スクロール移動先の目印（ページ内で1箇所のみ配置）
st.markdown('<div id="quiz-top"></div>', unsafe_allow_html=True)

#採点済みの場合は上部に総合得点を表示
if submitted:
    score = sum(
        1 for i, quiz in enumerate(quiz_list)
        if check_answer(st.session_state.get(f"answer_{i}", ""), quiz["keywords"])
    )
    st.success(f"## 得点：{score} / {len(quiz_list)}")

st.divider()

# 各問題の表示と回答入力
for i, quiz in enumerate(quiz_list):
    st.subheader(f"問題 {i + 1}")
    #顔文字
    twemoji_url = f"{TWEMOJI_BASE_URL}/{quiz['image_url']}.svg"
    st.markdown(f'<img src="{twemoji_url}" width="150">', unsafe_allow_html=True)

    user_ans = st.text_input(
        "この顔文字の名称は？（キーワード入力でもOK）",
        key=f"answer_{i}",
    )

    if submitted:#下でここがtrueになったら正誤判定実施
        if check_answer(user_ans, quiz["keywords"]):
            st.success(f"正解！（正式名称：{quiz['answer']}）")
        else:
            st.error(f"不正解（正解：{quiz['answer']}）")
    st.divider()

#採点ボタン
if st.button("まとめて答え合わせ", type="primary"):
    st.session_state.submitted = True
    st.session_state.scroll_top = True
    st.rerun()

st.markdown("---")

# リトライボタン
col1, col2 = st.columns(2)

with col1:
    if st.button("🔁 同じ問題をもう一度"):
        reset_quiz_state()
        st.session_state.scroll_top = True
        st.rerun()

with col2:
    if st.button("🎲 新しい問題を出題"):
        st.session_state.pop("quiz_list", None)#消す
        reset_quiz_state()
        st.session_state.scroll_top = True
        st.rerun()

# 出典表記
st.caption(
    "画像提供：Twemoji © Twitter, Inc.（CC BY 4.0）｜"
    "名称・解説参考：Let's Emoji（https://lets-emoji.com/）"
)    
    
    