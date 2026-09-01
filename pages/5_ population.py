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

# 2. 데이터 불러오기
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

    # 남성, 여성 각각의 총합 열 생성
    df_latest["남_총인구"] = df_latest[male_cols].sum(axis=1)
    df_latest["여_총인구"] = df_latest[female_cols].sum(axis=1)

    # 행 단위(axis=1)로 남여 인구를 더해 '총인구' 열 생성
    df_latest["총인구"] = df_latest["남_총인구"] + df_latest["여_총인구"]

    return df_latest, latest_year


# 데이터 로딩 실행
df, year = load_data()

st.success(f"🗓️ 가장 최신 데이터인 **{year}년 기준** 읍·면·동 인구 데이터입니다.")
st.divider()

# 디자인 테마 색상 (메인 코랄/복숭아, 서브 감청색)
warm_color = "#E07A5F"
sub_color = "#3D405B"

# --------------------------------------------------
# 1) 총인구 요약 통계량 (describe)
# --------------------------------------------------
st.subheader("1️⃣ 총인구 요약 통계량 (describe)")
st.write(
    "동네별 총인구의 평균, 중앙값(50%), 최소/최댓값 등 데이터의 대표 수치를 확인합니다."
)

desc_df = df["총인구"].describe().to_frame()
desc_df.columns = ["총인구 (명)"]
st.dataframe(desc_df, use_container_width=True)

st.divider()

# --------------------------------------------------
# 2) 총인구 히스토그램 (Histogram)
# --------------------------------------------------
st.subheader("2️⃣ 총인구 히스토그램")
st.write(
    "인구 구간별로 몇 개의 동네가 속해 있는지 막대의 높이로 나타낸 그래프입니다."
)

fig_hist = px.histogram(
    df,
    x="총인구",
    nbins=50,
    title="읍·면·동 총인구 분포 (히스토그램)",
    labels={"총인구": "총인구 (명)"},
    color_discrete_sequence=[warm_color],
)

fig_hist.update_layout(
    xaxis_title="총인구 (명)",
    yaxis_title="동네 수 (개)",
    hovermode="x unified",
    template="plotly_white",
)
st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# --------------------------------------------------
# 3) 총인구 상자그림 (Box Plot)
# --------------------------------------------------
st.subheader("3️⃣ 총인구 상자그림")
st.write(
    "데이터의 사분위수(25%, 50%, 75%)와 인구가 유독 많은 동네(이상치 점)를 쉽게 찾아냅니다."
)

fig_box = px.box(
    df,
    y="총인구",
    title="읍·면·동 총인구 상자그림 (Box Plot)",
    labels={"총인구": "총인구 (명)"},
    color_discrete_sequence=[warm_color],
    points="outliers",
)

fig_box.update_layout(yaxis_title="총인구 (명)", template="plotly_white")
st.plotly_chart(fig_box, use_container_width=True)

st.divider()

# --------------------------------------------------
# 4) 시도별 총인구 합계 막대그래프 (추가)
# --------------------------------------------------
st.subheader("4️⃣ 시도별 총인구 비교 (막대그래프)")
st.info(
    "💡 **왜 이 그래프가 필요할까요?**\n\n"
    "동네 단위의 퍼짐을 넘어 **지역 단위(시·도)**로 데이터를 묶었을 때 "
    "수도권과 지방 사이에 얼마나 거대한 인구 격차가 존재하는지 한눈에 파악하기 위해서입니다."
)

# 시도별 인구 합계 구하기 및 내림차순 정렬
df_sido = (
    df.groupby("시도")["총인구"].sum().reset_index().sort_values(by="총인구", ascending=False)
)

fig_bar = px.bar(
    df_sido,
    x="시도",
    y="총인구",
    title="시도별 총인구 합계 (인구순 정렬)",
    labels={"총인구": "총인구 (명)", "시도": "시·도"},
    color_discrete_sequence=[sub_color],
)

fig_bar.update_layout(
    xaxis_title="시·도",
    yaxis_title="총인구 (명)",
    hovermode="x unified",
    template="plotly_white",
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# --------------------------------------------------
# 5) 동네별 남·여 인구 산점도 (추가)
# --------------------------------------------------
st.subheader("5️⃣ 동네별 남·여 인구 분포 (산점도)")
st.info(
    "💡 **왜 이 그래프가 필요할까요?**\n\n"
    "단순히 '총인구' 표만 봐서는 알 수 없었던 **남녀 성비의 균형과 편차**를 확인하기 위해서입니다. "
    "대각선 기준선에서 멀어진 점일수록 남성 또는 여성 인구가 한쪽으로 치우친 동네임을 의미합니다."
)

fig_scatter = px.scatter(
    df,
    x="남_총인구",
    y="여_총인구",
    hover_name="동",
    hover_data=["시도", "시군구"],
    title="읍·면·동별 남성 인구 vs 여성 인구",
    labels={"남_총인구": "남성 인구 (명)", "여_총인구": "여성 인구 (명)"},
    color_discrete_sequence=[warm_color],
    opacity=0.6,  # 점들이 겹쳐 보여도 밀도를 알 수 있게 투명도 설정
)

# 완벽한 성비 균형(1:1)을 나타내는 대각선 가이드라인 추가
max_val = max(df["남_총인구"].max(), df["여_총인구"].max())
fig_scatter.add_shape(
    type="line",
    x0=0,
    y0=0,
    x1=max_val,
    y1=max_val,
    line=dict(color="Gray", dash="dash"),
)

fig_scatter.update_layout(
    xaxis_title="남성 인구 (명)",
    yaxis_title="여성 인구 (명)",
    template="plotly_white",
)
st.plotly_chart(fig_scatter, use_container_width=True)
