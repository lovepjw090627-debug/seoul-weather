import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울의 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    df = df.dropna(subset=["날짜", "평균기온"])

    return df


try:
    df = load_data()

    df["연도"] = df["날짜"].dt.year

    yearly = (
        df.groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    yearly = yearly.rename(
        columns={"평균기온": "연평균기온"}
    )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


st.title("🌡️ 서울의 100년 기온 변화")

st.write(
    "서울의 일별 평균기온 데이터를 이용해 연도별 평균기온을 계산했습니다."
)

min_year = int(yearly["연도"].min())
max_year = int(yearly["연도"].max())

st.info(
    f"📅 데이터 기간: {min_year}년 ~ {max_year}년"
)

st.subheader("연평균 기온 변화")

chart_data = yearly.set_index("연도")

st.line_chart(
    chart_data["연평균기온"],
    height=500
)

first_temp = yearly.iloc[0]["연평균기온"]
last_temp = yearly.iloc[-1]["연평균기온"]
difference = last_temp - first_temp

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        f"{min_year}년 평균",
        f"{first_temp:.1f} ℃"
    )

with col2:
    st.metric(
        f"{max_year}년 평균",
        f"{last_temp:.1f} ℃"
    )

with col3:
    st.metric(
        "기온 변화",
        f"{difference:+.1f} ℃"
    )

st.divider()

st.caption(
    "자료: 서울 기상 관측 데이터(seoul.csv) | "
    "연평균 기온은 해당 연도의 일별 평균기온을 평균하여 계산했습니다."
)

with st.expander("📊 연도별 데이터 보기"):
    display_data = yearly.copy()
    display_data["연평균기온"] = display_data["연평균기온"].round(2)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )
```
