import streamlit as st
import random

st.set_page_config(page_title="용어 3x3 빙고 게임", page_icon="🧩", layout="centered")

st.title("🧩 용어 3x3 빙고 게임")
st.caption("선생님이 설명을 읽어주면 해당하는 용어 칸을 클릭하세요!")

# ------------------------------------------------------------------------------
# 1. 용어 단어장 정의 (13개)
# ------------------------------------------------------------------------------
VOCAB_LIST = [
    {"term": "Repository\n(레포지토리)", "desc": "코드와 파일들을 모아두는 저장 공간"},
    {"term": "Sign up", "desc": "새로 회원가입하기"},
    {"term": "Username", "desc": "나를 나타내는 고유한 이름 (아이디)"},
    {"term": "Public / Private", "desc": "공개(누구나 볼 수 있음) / 비공개(나만 볼 수 있음)"},
    {"term": "Commit", "desc": "수정한 내용을 \"저장하고 기록\"하는 것"},
    {"term": "README", "desc": "이 저장소가 뭔지 설명하는 안내문"},
    {"term": "Authorize\n(승인)", "desc": "\"이 앱이 내 정보를 사용해도 좋다\"고 허락하는 것"},
    {"term": "Branch\n(브랜치)", "desc": "원본은 그대로 두고 따로 수정해볼 수 있는 \"가지\""},
    {"term": "Main file path", "desc": "실행할 때 가장 먼저 열어야 할 파일의 위치"},
    {"term": "Deploy\n(배포)", "desc": "완정한 코드를 실제로 작동하는 서비스로 세상에 공개하는 것"},
    {"term": "requirements.txt", "desc": "이 프로그램을 실행하는 데 필요한 도구 목록"},
    {"term": "main.py", "desc": "실제 프로그램 코드가 담긴 파일 (.py = 파이썬 파일)"},
    {"term": "import", "desc": "다른 사람이 만든 기능(도구)을 내 코드로 가져와 쓰는 것"},
]

# ------------------------------------------------------------------------------
# 2. 게임 상태 초기화 및 셔플 함수
# ------------------------------------------------------------------------------
def start_new_game():
    selected_vocab = random.sample(VOCAB_LIST, 9)
    st.session_state.board = [selected_vocab[i:i+3] for i in range(0, 9, 3)]
    st.session_state.marked = [[False] * 3 for _ in range(3)]

if "board" not in st.session_state:
    start_new_game()

# ------------------------------------------------------------------------------
# 3. 빙고 줄 수 계산 함수
# ------------------------------------------------------------------------------
def count_bingo():
    m = st.session_state.marked
    lines = 0
    # 가로 줄
    for r in range(3):
        if all(m[r]):
            lines += 1
    # 세로 줄
    for c in range(3):
        if all(m[r][c] for r in range(3)):
            lines += 1
    # 대각선 ↘
    if m[0][0] and m[1][1] and m[2][2]:
        lines += 1
    # 대각선 ↙
    if m[0][2] and m[1][1] and m[2][0]:
        lines += 1
    return lines

# ------------------------------------------------------------------------------
# 4. 상단 점수 및 조작 버튼
# ------------------------------------------------------------------------------
bingo_count = count_bingo()

col_score, col_btn = st.columns([3, 1])
with col_score:
    st.metric("🎯 완성한 빙고 줄 수", f"{bingo_count} 줄")
with col_btn:
    st.write("")
    if st.button("🔄 새 판 만들기", use_container_width=True):
        start_new_game()
        st.rerun()

# 1줄 이상 완성 시 풍선 효과 및 축하 문구 표시
if bingo_count >= 1:
    st.balloons()
    st.success(f"🎉 축하합니다! {bingo_count}빙고를 달성했습니다!")

st.divider()

# ------------------------------------------------------------------------------
# 5. 3x3 빙고판 버튼 출력
# ------------------------------------------------------------------------------
st.subheader("📋 나의 3x3 빙고판")

for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        item = st.session_state.board[r][c]
        term = item["term"]
        is_marked = st.session_state.marked[r][c]
        
        button_label = f"✅\n{term}" if is_marked else f"\n{term}\n"
        
        with cols[c]:
            if st.button(
                button_label,
                key=f"cell_{r}_{c}_{term}",
                use_container_width=True
            ):
                st.session_state.marked[r][c] = not is_marked
                st.rerun()

st.divider()

# ------------------------------------------------------------------------------
# 6. 선생님용 용어 힌트
# ------------------------------------------------------------------------------
with st.expander("💡 [선생님용] 이번 판에 등장한 용어와 쉬운 설명 확인하기"):
    st.write("현재 빙고판에 포함된 9개 용어의 설명입니다:")
    current_board_flat = [item for row in st.session_state.board for item in row]
    for idx, item in enumerate(current_board_flat, 1):
        clean_term = item['term'].replace('\n', ' ')
        st.write(f"**{idx}. {clean_term}**: {item['desc']}")
