```python
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    # UTF-8 BOM이 포함되어 있을 수 있으므로 utf-8-sig 사용
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 날짜 또는 평균기온이 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


# 데이터 불러오기
try:
    df = load_data()

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly = (
        df.groupby("연도", as_index=False)["평균기온"]
        .mean()
        .rename(columns={"평균기온": "연평균기온"})
    )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


# -----------------------------
# 화면
# -----------------------------

st.title("🌡️ 서울의 100년 기온 변화")
st.subheader("연평균 기온은 지난 100여 년 동안 어떻게 변했을까?")

st.markdown(
    """
    서울의 일별 기상 데이터를 이용해 **연평균 기온**을 계산했습니다.
    
    그래프의 흐름을 보면 서울의 연평균 기온이 장기적으로
    어떻게 변화해 왔는지 한눈에 확인할 수 있습니다.
    """
)

# 전체 기간 표시
min_year = int(yearly["연도"].min())
max_year = int(yearly["연도"].max())

st.info(
    f"📅 데이터 기간: **{min_year}년 ~ {max_year}년**  "
    f"| 총 {len(yearly)}개 연도의 연평균 기온"
)

# 그래프용 데이터
chart_data = yearly.set_index("연도")[["연평균기온"]]

st.line_chart(
    chart_data,
    y="연평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)",
    height=500
)

# 요약 정보
col1, col2, col3 = st.columns(3)

with col1:
    first_year = yearly.iloc[0]
    st.metric(
        f"{int(first_year['연도'])}년",
        f"{first_year['연평균기온']:.1f} ℃"
    )

with col2:
    last_year = yearly.iloc[-1]
    st.metric(
        f"{int(last_year['연도'])}년",
        f"{last_year['연평균기온']:.1f} ℃"
    )

with col3:
    difference = last_year["연평균기온"] - first_year["연평균기온"]
    st.metric(
        "처음과 마지막 차이",
        f"{difference:+.1f} ℃"
    )

st.divider()

st.caption(
    "자료: 제공된 서울 기상 관측 데이터(seoul.csv) | "
    "연평균 기온은 해당 연도의 일별 평균기온을 평균하여 계산"
)

# 원하면 연도별 데이터 확인
with st.expander("📊 연도별 평균기온 데이터 보기"):
    display_data = yearly.copy()
    display_data["연평균기온"] = display_data["연평균기온"].round(2)
    display_data = display_data.rename(
        columns={
            "연도": "연도",
            "연평균기온": "연평균 기온 (℃)"
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
```
