# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd

# 페이지 제목 설정
st.title("타율의 미학: KBO 리그 타율 분석")
url='https://github.com/hjoonu32/happy-memories/blob/main/baseball32.csv'+'?raw=true'
df = pd.read_csv(url)
st.dataframe(df)
