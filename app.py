
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

# =========================
# Prompt
# =========================
SYSTEM_PROMPT = """
너는 동물 전투력 분석가다.

사용자가 두 동물을 주면 반드시 아래 기준으로 비교해서 승자를 결정한다:

- 힘 (physical strength)
- 속도
- 공격력
- 방어력
- 생존 능력
- 실제 야생에서의 전투력

반드시 하나의 승자를 선택해야 한다.
그리고 마지막 줄에는 반드시 "승자: XXX" 형식으로 작성한다.
"""

# =========================
# Page Setting
# =========================
def init_page():
    st.set_page_config(page_title="동물의 왕", page_icon="🦁")
    st.header("🦁 동물의 왕 AI")
    st.sidebar.title("Options")

# =========================
# Model 선택 (수업 스타일 응용)
# =========================
def select_model(temperature=0):
    models = ("gpt-5.5", "gpt-5.4-mini")
    model = st.sidebar.radio("Choose model:", models)

    return ChatOpenAI(
        temperature=temperature,
        model=model
    )

# =========================
# Chain 생성
# =========================
def init_chain():
    llm = select_model()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "동물 A: {animal1}\n동물 B: {animal2}")
    ])

    return prompt | llm | StrOutputParser()

# =========================
# Main Logic
# =========================
def main():
    init_page()
    chain = init_chain()

    col1, col2 = st.columns(2)

    with col1:
        animal1 = st.text_input("동물 A", placeholder="호랑이")

    with col2:
        animal2 = st.text_input("동물 B", placeholder="사자")

    if st.button("🔥 누가 더 강한가?"):
        if not animal1 or not animal2:
            st.warning("두 동물을 모두 입력하세요!")
        else:
            with st.spinner("AI가 전투력 분석 중..."):
                result = chain.invoke({
                    "animal1": animal1,
                    "animal2": animal2
                })

            st.subheader("🏆 결과")
            st.write(result)

            if "승자:" in result:
                winner = result.split("승자:")[-1].strip()
                st.success(f"최종 승자 👉 {winner}")

if __name__ == "__main__":
    main()
