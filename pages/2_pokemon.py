import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="PokéMBTI - 내 성격과 어울리는 포켓몬은?",
    page_icon="🐾",
    layout="centered"
)

# 2. MBTI별 포켓몬 데이터베이스 (이모지 및 테마 컬러 적용)
POKEMON_DATA = {
    "ISTJ": {
        "name": "거북왕 (Blastoise)",
        "emoji": "🐢",
        "bg_color": "#E3F2FD",
        "border_color": "#1E88E5",
        "type": "💧 물",
        "desc": "신중하고 책임감이 강하며 규칙을 잘 지키는 든든한 리더입니다.",
        "quote": "묵묵하지만 언제나 완벽하게 임무를 완수해요!"
    },
    "ISFJ": {
        "name": "토게피 (Togepi)",
        "emoji": "🥚",
        "bg_color": "#FFF8E1",
        "border_color": "#FFB300",
        "type": "✨ 페어리",
        "desc": "다정하고 헌신적이며 주변 사람들에게 행복과 안정을 선사합니다.",
        "quote": "당신의 따뜻함이 주위를 밝게 만들어줘요!"
    },
    "INFJ": {
        "name": "뮤 (Mew)",
        "emoji": "🔮",
        "bg_color": "#F3E5F5",
        "border_color": "#AB47BC",
        "type": "👁️ 에스퍼",
        "desc": "신비롭고 통찰력이 뛰어납니다. 깊은 생각과 강한 신념을 가졌어요.",
        "quote": "보이지 않는 마음의 소리를 귀담아듣습니다."
    },
    "INTJ": {
        "name": "뮤츠 (Mewtwo)",
        "emoji": "🧬",
        "bg_color": "#EDE7F6",
        "border_color": "#7E57C2",
        "type": "👁️ 에스퍼",
        "desc": "철저한 전략가이자 독창적인 고독한 천재 스타일입니다.",
        "quote": "모든 행동에는 치밀한 계획과 이유가 있죠."
    },
    "ISTP": {
        "name": "루카리오 (Lucario)",
        "emoji": "🐺",
        "bg_color": "#ECEFF1",
        "border_color": "#607D8B",
        "type": "⚙️ 강철 / 🥊 격투",
        "desc": "냉철한 상황 판단력과 도구를 다루는 능력이 뛰어난 실전파입니다.",
        "quote": "말보다는 행동으로 빠르게 증명합니다."
    },
    "ISFP": {
        "name": "이브이 (Eevee)",
        "emoji": "🦊",
        "bg_color": "#EFEBE9",
        "border_color": "#8D6E63",
        "type": "⭐ 노말",
        "desc": "자유롭고 호기심 많으며 다양한 가능성을 지닌 감성파입니다.",
        "quote": "무엇이든 될 수 있는 당신만의 매력이 있어요!"
    },
    "INFP": {
        "name": "랄토스 (Ralts)",
        "emoji": "🌱",
        "bg_color": "#E8F5E9",
        "border_color": "#66BB6A",
        "type": "👁️ 에스퍼 / ✨ 페어리",
        "desc": "섬세하고 상상력이 풍부하며 맑고 순수한 마음을 간직하고 있습니다.",
        "quote": "타인의 감정에 감동하고 이상을 꿈꿉니다."
    },
    "INTP": {
        "name": "고라파덕 (Psyduck)",
        "emoji": "🦆",
        "bg_color": "#E0F7FA",
        "border_color": "#26C6DA",
        "type": "💧 물",
        "desc": "엉뚱해 보이지만 머릿속에서는 끝없는 고민과 생각이 소용돌이칩니다.",
        "quote": "깊은 질문을 던지며 세상의 원리를 탐구해요."
    },
    "ESTP": {
        "name": "피카츄 (Pikachu)",
        "emoji": "⚡",
        "bg_color": "#FFFDE7",
        "border_color": "#FDD835",
        "type": "⚡ 전기",
        "desc": "에너지가 넘치고 순발력이 뛰어납니다. 스릴과 모험을 즐겨요!",
        "quote": "망설일 시간에 일단 도전하고 보는 거야!"
    },
    "ESFP": {
        "name": "푸린 (Jigglypuff)",
        "emoji": "🎤",
        "bg_color": "#FCE4EC",
        "border_color": "#EC407A",
        "type": "⭐ 노말 / ✨ 페어리",
        "desc": "주목받는 것을 좋아하고 밝은 에너지로 분위기 메이커 역할을 합니다.",
        "quote": "모두의 시선을 사로잡는 나는야 스타!"
    },
    "ENFP": {
        "name": "팽도리 (Piplup)",
        "emoji": "🐧",
        "bg_color": "#E1F5FE",
        "border_color": "#29B6F6",
        "type": "💧 물",
        "desc": "자존감이 높고 호기심이 왕성하며 늘 새로운 열정으로 가득합니다.",
        "quote": "오늘 하루는 어떤 신나는 일이 펼쳐질까?"
    },
    "ENTP": {
        "name": "팬텀 (Gengar)",
        "type": "👻 고스트 / ☠️ 독",
        "emoji": "😈",
        "bg_color": "#F3E5F5",
        "border_color": "#8E24AA",
        "desc": "위트가 넘치고 창의적입니다. 유쾌한 장난과 재치 있는 대화를 좋아합니다.",
        "quote": "뻔한 건 재미없잖아? 새로운 방식을 찾아보자!"
    },
    "ESTJ": {
        "name": "윈디 (Arcanine)",
        "emoji": "🦁",
        "bg_color": "#FBE9E7",
        "border_color": "#FF7043",
        "type": "🔥 불꽃",
        "desc": "체계적이고 리더십이 뛰어나며 명예와 신의를 중요하게 생각합니다.",
        "quote": "위엄 있고 당당하게 그룹을 이끌어 나갑니다."
    },
    "ESFJ": {
        "name": "해피너스 (Blissey)",
        "emoji": "💖",
        "bg_color": "#FFEBEE",
        "border_color": "#EF5350",
        "type": "⭐ 노말",
        "desc": "친절하고 사교적이며 타인을 살뜰하게 보살피는 친화력의 소유자입니다.",
        "quote": "모두가 행복하고 정다운 세상을 원해요!"
    },
    "ENFJ": {
        "name": "가디안 (Gardevoir)",
        "emoji": "🧚‍♀️",
        "bg_color": "#E8F5E9",
        "border_color": "#4CAF50",
        "type": "👁️ 에스퍼 / ✨ 페어리",
        "desc": "카리스마와 공감 능력을 동시에 겸비한 진정한 조력자입니다.",
        "quote": "당신을 보호하고 함께 성장하도록 도울게요."
    },
    "ENTJ": {
        "name": "리자몽 (Charizard)",
        "emoji": "🐉",
        "bg_color": "#FFF3E0",
        "border_color": "#FF9800",
        "type": "🔥 불꽃 / 🕊️ 비행",
        "desc": "당당한 야망과 강한 추진력으로 목표를 향해 거침없이 돌진합니다.",
        "quote": "승리는 준비된 자의 것입니다. 날 따라오세요!"
    }
}

# 3. 타이틀 영역
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎀 PokéMBTI 🎀</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555555;'>당신의 MBTI와 꼭 닮은 포켓몬을 만나보세요!</h3>", unsafe_allow_html=True)
st.write("---")

# 4. MBTI 선택 박스
mbti_list = list(POKEMON_DATA.keys())
selected_mbti = st.selectbox("✨ 당신의 MBTI 유형을 선택해 주세요:", mbti_list)

# 5. 결과 표시 영역 (HTML/CSS 맞춤 카드 디자인)
if selected_mbti:
    poke = POKEMON_DATA[selected_mbti]
    st.write("")
    
    st.subheader(f"✨ [{selected_mbti}] 유형에 딱 맞는 포켓몬은?")
    
    # 이미지 대신 끊기지 않는 가벼운 대형 이모지 카드 생성
    st.markdown(f"""
    <div style="
        background-color: {poke['bg_color']};
        border: 3px solid {poke['border_color']};
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    ">
        <div style="font-size: 90px; line-height: 1.2; margin-bottom: 10px;">
            {poke['emoji']}
        </div>
        <h2 style="color: #333333; margin-bottom: 5px;">{poke['name']}</h2>
        <p style="color: #666666; font-weight: bold; margin-bottom: 15px;">{poke['type']}</p>
        <hr style="border: 0.5px solid {poke['border_color']}; opacity: 0.3; margin: 15px 0;">
        <p style="font-size: 1.1em; color: #444444; margin-bottom: 15px;">{poke['desc']}</p>
        <div style="
            background-color: rgba(255, 255, 255, 0.7);
            padding: 12px;
            border-radius: 10px;
            font-style: italic;
            color: #333333;
            font-weight: 500;
        ">
            💬 "{poke['quote']}"
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("✨ Streamlit Cloud Ready | 100% Reliable & Fast")
