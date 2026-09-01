import pandas as pd
import plotly.express as px
import streamlit as st

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(
    page_title="데이터 퍼짐 시각화 앱", page_icon="📊", layout="centered"
)

st.title("📊 동네별 총인구 데이터의 '퍼짐' 관찰하기")
st.write(
    "우리나라 읍·면·동 인구 데이터의 분포(퍼짐 정도)를 한눈에 파악해 봅시다!"
)

# 2. 데이터 불러오기 (선생님의 GitHub dataset 저장소 Raw 주소 사용)
DATA_URL = "https://raw.githubusercontent.com/wjddmsdud-boop/dataset/main/population_yearly.csv.gz"


@st.cache_data
def load_data():
    # pandas는 .csv.gz 압축 파일을 자동으로 풀어서 읽어옵니다.
    df = pd.read_csv(DATA_URL)

    # 데이터에서 가장 최근 연도 추출
    latest_year = df["연도"].max()
    df_latest = df[df["연도"] == latest_year].copy()

    # '남_'과 '여_'로 시작하는 나이별 인구 열 선택하기
    male_cols = [col for col in df_latest.columns if col.startswith("남_")]
    female_cols = [col for col in df_latest.columns if col.startswith("여_")]

    # 남성 및 여성 인구를 행 단위(axis=1)로 더해 '총인구' 열 생성
    df_latest["총인구"] = df_latest[male_cols + female_cols].sum(axis=1)

    return df_latest, latest_year


# 데이터 로딩 실행
df, year = load_data()

st.success(f"🗓️ 가장 최신 데이터인 **{year}년 기준** 읍·면·동 인구 데이터입니다.")
st.divider()

# 따뜻한 톤의 색상 지정 (코랄/복숭아 테마)
warm_color = "#E07A5F"

# --------------------------------------------------
# 1) 총인구 요약 통계량 (describe)
# --------------------------------------------------
st.subheader("1️⃣ 총인구 요약 통계량 (describe)")
st.write(
    "동네별 총인구의 평균, 중앙값(50%), 최소/최댓값 등 데이터의 대표 수치를 확인합니다."
)

# describe() 결과를 보기 쉽게 데이터프레임 형태로 변환
desc_df = df["총인구"].describe().to_frame()
desc_df.columns = ["총인구 (명)"]

# 스트림릿 표 형태로 출력
st.dataframe(desc_df, use_container_width=True)

st.divider()

# --------------------------------------------------
# 2) 총인구 히스토그램 (Histogram)
# --------------------------------------------------
st.subheader("2️⃣ 총인구 히스토그램")
st.write(
    "인구 구간별로 몇 개의 동네가 속해 있는지 막대의 높이로 나타낸 그래프입니다."
)

# Plotly 대화형 히스토그램 생성
fig_hist = px.histogram(
    df,
    x="총인구",
    nbins=50,
    title="읍·면·동 총인구 분포 (히스토그램)",
    labels={"총인구": "총인구 (명)"},
    color_discrete_sequence=[warm_color],
)

# 그래프 스타일 변경
fig_hist.update_layout(
    xaxis_title="총인구 (명)",
    yaxis_title="동네 수 (개)",
    hovermode="x unified",
    template="plotly_white",
)

# 스트림릿에 Plotly 그래프 표시
st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# --------------------------------------------------
# 3) 총인구 상자그림 (Box Plot)
# --------------------------------------------------
st.subheader("3️⃣ 총인구 상자그림")
st.write(
    "데이터의 사분위수(25%, 50%, 75%)와 인구가 유독 많은 동네(이상치 점)를 쉽게 찾아냅니다."
)

# Plotly 대화형 상자그림 생성
fig_box = px.box(
    df,
    y="총인구",
    title="읍·면·동 총인구 상자그림 (Box Plot)",
    labels={"총인구": "총인구 (명)"},
    color_discrete_sequence=[warm_color],
    points="outliers",  # 이상치 점을 명확히 표시
)

# 그래프 스타일 변경
fig_box.update_layout(yaxis_title="총인구 (명)", template="plotly_white")

# 스트림릿에 Plotly 그래프 표시
st.plotly_chart(fig_box, use_container_width=True)
