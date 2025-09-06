# 필요한 라이브러리 불러오기
import streamlit as st
import pandas as pd

# 페이지 제목 설정
st.title("타율의 미학: KBO 리그 타율 분석")

# ---

# GitHub URL에서 baseball32.csv 파일 불러오기
url = 'https://github.com/hjoonu32/happy-memories/blob/main/baseball32.csv' + '?raw=true'
try:
    df = pd.read_csv(url, encoding="utf-8")
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# ---

# 데이터 분석 시작
# 필요한 열 목록 정의
base_required_columns = ['Name', 'AVG', 'HR', 'OPS', 'WAR']

# 'Team' 열이 있는지 확인
has_team_column = 'Team' in df.columns

# 필수 열이 모두 있는지 확인
if not all(col in df.columns for col in base_required_columns):
    st.error(f"데이터 파일에 {base_required_columns} 중 하나 이상 열이 없습니다. 파일을 확인해주세요.")
else:
    # 데이터 정제 및 시각화 준비
    # NaN(결측값) 행 제거
    df.dropna(subset=base_required_columns, inplace=True)
    
    # 숫자형 데이터로 변환
    for col in ['AVG', 'HR', 'OPS', 'WAR']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 변환 후 발생한 NaN 값 다시 제거
    df.dropna(subset=base_required_columns, inplace=True)

    # ---
    # 팀 선택 기능 추가 (사이드바)
    # 'Team' 열이 있을 때만 팀 필터링 기능 활성화
    if has_team_column:
        st.sidebar.header("데이터 필터링")
        teams = ['전체'] + sorted(df['Team'].unique().tolist())
        selected_team = st.sidebar.selectbox("팀을 선택해주세요:", teams)
        
        # 선택된 팀에 따라 데이터프레임 필터링
        if selected_team == '전체':
            df_filtered = df
        else:
            df_filtered = df[df['Team'] == selected_team]
    else:
        df_filtered = df
        selected_team = '전체'
        st.warning("데이터 파일에 'Team' 열이 없어 팀별 필터링 기능이 비활성화됩니다.")

    # 데이터프레임 미리보기
    st.subheader("데이터 미리보기")
    if df_filtered.empty:
        st.warning("선택한 팀의 데이터가 존재하지 않습니다.")
    else:
        # 'Team' 열이 있을 때와 없을 때 데이터프레임 표시 방식 변경
        if has_team_column:
            st.dataframe(df_filtered[['Name', 'Team', 'AVG', 'HR', 'OPS', 'WAR']])
        else:
            st.dataframe(df_filtered[['Name', 'AVG', 'HR', 'OPS', 'WAR']])

        # ---
        # 선수 정보 분석 기능
        st.sidebar.header("선수 정보 분석")
        player_names = df_filtered['Name'].unique().tolist()
        if player_names:
            selected_player = st.sidebar.selectbox("선수를 선택해주세요:", player_names)
            player_data = df_filtered[df_filtered['Name'] == selected_player]

            if not player_data.empty:
                st.subheader(f"{selected_player} 선수 정보")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(label="타율 (AVG)", value=f"{player_data['AVG'].iloc[0]:.3f}")
                with col2:
                    st.metric(label="홈런 (HR)", value=f"{int(player_data['HR'].iloc[0])}개")
                with col3:
                    st.metric(label="OPS", value=f"{player_data['OPS'].iloc[0]:.3f}")
                with col4:
                    st.metric(label="WAR", value=f"{player_data['WAR'].iloc[0]:.2f}")
        
        st.markdown("---")

        # 1. 선수별 타율(AVG) 선 그래프
        st.subheader(f"{selected_team} 팀 선수별 타율(AVG) 분포")
        st.line_chart(df_filtered, x='Name', y='AVG', use_container_width=True)

        # 2. 홈런(HR) 순위 막대 그래프
        st.subheader(f"{selected_team} 팀 홈런(HR) 순위 (상위 10명)")
        # 홈런 순으로 정렬하여 상위 10개만 선택
        df_top_hr = df_filtered.sort_values(by='HR', ascending=False).head(10)
        st.bar_chart(df_top_hr, x='Name', y='HR', use_container_width=True)

        # 3. OPS와 WAR 관계 산점도
        st.subheader(f"{selected_team} 팀 OPS와 WAR 관계 (공격력 vs. 종합 가치)")
        # OPS와 WAR를 기준으로 산점도 생성
        st.scatter_chart(df_filtered, x='OPS', y='WAR', use_container_width=True)
