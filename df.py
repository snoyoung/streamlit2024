import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def show() :
  # 한글 폰트 설정
  plt.rcParams['font.family'] = 'NanumGothic'
  plt.rcParams['axes.unicode_minus'] = False

  # 초기 데이터프레임 로드 또는 session state에서 가져오기
  if 'df' not in st.session_state:
      st.session_state.df = pd.read_excel('./성적계산.xlsx')
  
  st.header('성적계산', divider='rainbow')
  # 버튼 영역
  btCol1, btCol2, btCol3, btCol4, btCol5 = st.columns(5)
  with btCol1 :
    bt1 = st.button('성적계산')
  with btCol2 :
    bt2 = st.button('순위계산')
  with btCol3 :
    bt3 = st.button('학점계산')
  with btCol4 :
    bt4 = st.button('파일저장')
  with btCol5 :
    bt5 = st.button('성적현황')

  # 데이터전처리
  # None 값을 0으로 처리
  st.session_state.df.fillna({'출석': 0, '중간': 0, '기말': 0, '과제': 0}, inplace=True)
  # 학번을 쉼표 없이 문자열로 변환
  st.session_state.df['학번'] = st.session_state.df['학번']\
                            .astype(str)\
                            .str.replace(',', '')

  if bt1 :
    st.session_state.df['합계'] = st.session_state.df['출석'] + \
                                  st.session_state.df['중간'] + \
                                  st.session_state.df['기말'] + \
                                  st.session_state.df['과제']
    st.success('성적계산 완료')
  elif bt2 :
    # NaN 값을 가장 낮은 순위로 처리
    st.session_state.df['순위'] = st.session_state.df['합계']\
                                  .rank(method='min', \
                                      ascending=False, \
                                      na_option='bottom')\
                                  .astype(int)

    
    st.success('순위계산완료')  
  elif bt3 :
    # 총 학생 수
    total_students = len(st.session_state.df)

    # 학점 계산 기준 비율
    bins = [0, 0.2, 0.5, 0.8, 1.0]
    labels = ['A', 'B', 'C', 'D']

    # 학점 계산
    st.session_state.df['학점'] = pd.cut( \
                                  st.session_state.df['순위'] / total_students, \
                                  bins=bins, \
                                  labels=labels, 
                                  right=False)

    # 'F' 카테고리를 추가하고 값 설정
    st.session_state.df['학점'] = st.session_state.df['학점'].astype(str)
    st.session_state.df.loc[st.session_state.df['합계'] == 0, '학점'] = 'F'
    st.session_state.df.loc[st.session_state.df['과제'] == 0, '학점'] = 'F'
    st.success('학점계산 완료')
  elif bt4:  
      # 엑셀 파일로 저장
      output = io.BytesIO()
      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
          st.session_state.df.to_excel(writer, index=False, sheet_name='Sheet1')
      output.seek(0)
      
      # 다운로드 버튼 생성
      st.download_button(
          label="엑셀 파일 다운로드",
          data=output,
          file_name="성적계산_결과.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      )
      st.success('파일 저장 준비 완료. 다운로드 버튼을 클릭하세요.')

  elif bt5: 
    # 그래프 생성
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 성적 분포 히스토그램
    ax1.hist(st.session_state.df['합계'], bins=20, edgecolor='black')
    ax1.set_title('성적 분포')
    ax1.set_xlabel('점수')
    ax1.set_ylabel('학생 수')
    
    # 학점 분포 파이 차트
    if '학점' in st.session_state.df.columns:
        grade_counts = st.session_state.df['학점'].value_counts()
        ax2.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title('학점 분포')
    
    st.pyplot(fig)

  st.dataframe(st.session_state.df)


