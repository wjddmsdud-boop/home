import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(
    page_title="전국 고령화 단계구분도", page_icon="🗺️", layout="wide"
)

st.title("🗺️ 2026년 전국 시군구별 고령화율 단계구분도")
st.write(
    "전국 읍·면·동 인구 데이터를 **시군구(5자리 코드)** 단위로 합산하여 **65세 이상 고령 인구 비율(%)**을 지도 위에 시각화합니다."
)

# 2. 데이터 및 GeoJSON 경로 지정
POPULATION_URL = "https://raw.githubusercontent.com/wjddmsdud-boop/dataset/main/population_yearly.csv.gz"
GEOJSON_URL = "https://raw.githubusercontent.com/wjddmsdud-boop/dataset/refs/heads/main/sigungu_kr.geojson"


# 3. 데이터 로딩 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    # --------------------------------------------------
    # A. GeoJSON 경계 파일 로드 (requests)
    # --------------------------------------------------
    geo_res = requests.get(GEOJSON_URL)
    geojson_data = geo_res.json()

    # --------------------------------------------------
    # B. 인구 데이터 로드 및 2026년 데이터 추출
    # --------------------------------------------------
    df = pd.read_csv(POPULATION_URL)

    # 코드를 5자리 문자열로 다루기 위해 처리 (앞자리 0 유지를 위한 zfill 적용)
    df["코드"] = df["코드"].astype(str).str.zfill(8)

    # 2026년 최신 데이터만 필터링
    df_2026 = df[df["연도"] == 2026].copy()

    # 동 코드의 앞 5자리를 잘라 '시군구코드' 생성
    df_2026["시군구코드"] = df_2026["코드"].str[:5]

    # --------------------------------------------------
    # C. 전체 인구 및 65세 이상 인구 열 집계
    # --------------------------------------------------
    # '계_'로 시작하되 '남_', '여_'는 제외한 전체 나이 열 찾기
    all_total_cols = [
        col
        for col in df_2026.columns
        if col.startswith("계_")
        and not col.startswith("남_")
        and not col.startswith("여_")
    ]

    # '계_65세'부터 나이 열만 추출
    # 열 이름에서 숫자만 가져와 65 이상인 열을 필터링합니다.
    senior_cols = []
    for col in all_total_cols:
        age_str = col.replace("계_", "").replace("세 이상", "").replace("세", "")
        if age_str.isdigit() and int(age_str) >= 65:
            senior_cols.append(col)

    # 동 단위로 총인구 및 고령인구 합산
    df_2026["동_총인구"] = df_2026[all_total_cols].sum(axis=1)
    df_2026["동_고령인구"] = df_2026[senior_cols].sum(axis=1)

    # --------------------------------------------------
    # D. 시군구(5자리 코드) 단위 그룹화 및 고령화율(%) 계산
    # --------------------------------------------------
    df_sigungu = (
        df_2026.groupby("시군구코드")[["동_총인구", "동_고령인구"]]
        .sum()
        .reset_index()
    )

    # 고령화율 (%) = (65세 이상 인구 / 전체 인구) * 100
    df_sigungu["고령화율"] = (
        df_sigungu["동_고령인구"] / df_sigungu["동_총인구"]
    ) * 100
    df_sigungu["고령화율"] = df_sigungu["고령화율"].round(2)

    return geojson_data, df_sigungu


# 데이터 준비
geojson_data, df_sigungu = load_data()

st.success("✅ 인구 데이터 및 지리 경계 데이터(GeoJSON) 처리가 완료되었습니다.")
st.divider()

# --------------------------------------------------
# 4. Plotly 단계구분도(Choropleth Map) 작성
# --------------------------------------------------
st.subheader("📌 시군구별 고령화율(%) 지도 관찰")
st.info(
    "💡 지도 위의 시군구 영역에 마우스를 올리면 해당 지역의 **시군구 명칭**과 **고령화 비율(%)**을 확인할 수 있습니다."
)

# Plotly Choropleth 지도 생성
fig = px.choropleth(
    df_sigungu,
    geojson=geojson_data,
    locations="시군구코드",  # 인구 데이터의 5자리 코드
    featureidkey="properties.코드",  # GeoJSON의 5자리 코드 속성
    color="고령화율",  # 색상으로 표현할 값
    color_continuous_scale="Reds",  # 고령화율이 높을수록 진한 빨간색
    range_color=(df_sigungu["고령화율"].min(), df_sigungu["고령화율"].max()),
    labels={"고령화율": "고령화율 (%)", "시군구코드": "지역코드"},
    hover_data={"시군구코드": False, "고령화율": ":.2f%"},  # hover 툴팁 설정
)

# GeoJSON 내부 속성의 '시군구', '시도' 이름을 Hover 툴팁 표시에 추가 연결
# (GeoJSON 매핑 특성에 맞춰 hovertemplate 커스텀)
fig.update_traces(
    hovertemplate="<b>%{properties.시도} %{properties.시군구}</b><br>고령화율: %{z:.2f}%<extra></extra>"
)

# 지도 배경 타일 제거 및 경계선만 깔끔하게 스타일링
fig.update_geos(
    fitbounds="locations",  # 대한민국 영역으로 지도 자동 맞춤
    visible=False,  # 외부 타일 및 기본 지형선 비활성화
)

fig.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    height=650,
    template="plotly_white",
)

# 스트림릿에 지도 출력
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 5. 요약 통계 및 하단 표 제공
# --------------------------------------------------
st.divider()
st.subheader("📊 시군구별 고령화율 데이터 수치 확인")

# 고령화율 높은 순으로 정렬하여 표 출력
df_table = df_sigungu.sort_values(by="고령화율", ascending=False).reset_index(
    drop=True
)
df_table.columns = ["시군구 코드", "총인구(명)", "고령인구(명)", "고령화율(%)"]

st.dataframe(df_table, use_container_width=True)
