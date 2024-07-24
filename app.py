import streamlit as st
import dice
import updown
import df

st.sidebar.title("메뉴선택")
page = st.sidebar.radio("", ["주사위던지기", "업다운게임", "데이터분석"])

if page == "주사위던지기":
  st.title("주사위던지기")
  dice.show()

elif page == "업다운게임":
  st.title("업다운게임")
  updown.show()

elif page == "데이터분석":
  st.title("데이터분석")
  df.show()

  