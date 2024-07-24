import streamlit as st
import random
import time

def show() :
    # 상태 초기화
    if 'stFlag' not in st.session_state:
        st.session_state.stFlag = False

    if 'n' not in st.session_state:
        st.session_state['n'] = None

    st.header('업다운 게임', divider='rainbow')

    def start_game():
        st.session_state['n'] = random.randint(1, 100)
        st.session_state.stFlag = True 

    if st.session_state.stFlag:
        st.subheader('게임중...')
        usern = st.text_input('1에서 100까지 숫자를 입력하세요.',\
                            '', \
                            placeholder='정수입력')
        if usern.isdigit():
            un = int(usern)
            if st.session_state.n > un:
                st.image('./img/up.png')
            elif st.session_state.n < un:
                st.image('./img/down.png')
            else:
                st.image('./img/good.png')
                st.session_state.stFlag = False
                st.session_state.n = None
                st.success("정답입니다! 5초후에 초기화됩니다.")
                time.sleep(5)
                st.experimental_rerun()
            
    else:
        if st.button('게임시작', on_click=start_game):
            st.session_state.stFlag = True
        st.image('./img/what.png')

    # 디버깅을 위해 콘솔에 난수 출력
    if st.session_state['n'] is not None:
        print(f'Random number: {st.session_state["n"]}')
        print(f'session_state.stFlag: {st.session_state.stFlag}')
