# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd

# 페이지 제목 설정
st.title("타율의 미학: KBO 리그 타율 분석")

# ---

# baseball32.csv 파일 불러오기
try:
    # 헤더가 첫 번째 줄에 있습니다.
    df = pd.read_csv("baseball32.csv", header=0, encoding="euc-kr")

    # 필요한 열이 있는지 확인
    required_columns = ['Name', 'AVG', 'HR', 'OPS', 'WAR']
    if not all(col in df.columns for col in required_columns):
        st.error(f"데이터 파일에 {required_columns} 중 하나 이상 열이 없습니다. 파일을 확인해주세요.")
    else:
        # 데이터 정제 및 시각화 준비
        # NaN(결측값) 행 제거
        df.dropna(subset=required_columns, inplace=True)
        
        # 숫자형 데이터로 변환
        for col in ['AVG', 'HR', 'OPS', 'WAR']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 변환 후 발생한 NaN 값 다시 제거
        df.dropna(subset=required_columns, inplace=True)

        # 데이터프레임 미리보기
        st.subheader("데이터 미리보기")
        st.dataframe(df[['Name', 'AVG', 'HR', 'OPS', 'WAR']])

        # ---

        # 1. 선수별 타율(AVG) 선 그래프
        st.subheader("선수별 타율(AVG) 선 그래프")
        st.line_chart(df, x='Name', y='AVG', use_container_width=True)

        # 2. 홈런(HR) 순위 막대 그래프
        st.subheader("홈런(HR) 순위 (상위 10명)")
        # 홈런 순으로 정렬하여 상위 10개만 선택
        df_top_hr = df.sort_values(by='HR', ascending=False).head(10)
        st.bar_chart(df_top_hr, x='Name', y='HR', use_container_width=True)

        # 3. OPS와 WAR 관계 산점도
        st.subheader("OPS와 WAR 관계 (선수의 공격력 vs. 종합 가치)")
        # OPS와 WAR를 기준으로 산점도 생성
        st.scatter_chart(df, x='OPS', y='WAR', use_container_width=True)
        
except FileNotFoundError:
    st.error("baseball32.csv 파일을 찾을 수 없습니다. 파일이 'app.py'와 같은 폴더에 있는지 확인해주세요.")
    st.warning("스트림릿 앱을 배포하려면 baseball32.csv 파일도 GitHub 리포지토리에 함께 업로드해야 합니다.")
except Exception as e:
    st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
