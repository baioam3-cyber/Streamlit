
import tiktoken
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL_PRICES = {
    "input": {
        "gpt-5.5": 5 / 1_000_000,
        "gpt-5.4-mini": 0.75 / 1_000_000
    },
    "output": {
        "gpt-5.5": 30 / 1_000_000,
        "gpt-5.4-mini": 4.5 / 1_000_000
    },
}

SYSTEM_PROMPT = """
너는 동물 생물학 전문가이자 전투력 분석가다.

사용자가 두 동물을 주면 반드시 아래 기준으로 비교해서 승자를 결정한다:

- 힘 (physical strength)
- 속도
- 공격력
- 방어력
- 생존 능력
- 실제 야생에서의 전투력

중요:
- 반드시 하나의 승자를 선택해야 한다.
- 애매하다는 답변 금지
- 논리적으로 설명 후 마지막에 반드시 "승자: XXX" 형식으로 결론을 낸다.
"""

def init_page():
    st.set_page_config(page_title="동물의 왕 찾기", page_icon="🦁")
    st.header("동물의 왕 찾기 🦁")
    st.sidebar.title("Options")

def init_page():
    st.set_page_config(page_title="동물의 왕", page_icon="🦁")
    st.title("🦁 동물의 왕 AI")
    st.write("두 동물을 입력하면 누가 더 강한지 판단합니다")

def init_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", "동물 A: {animal1}\n동물 B: {animal2}")
    ])
    return prompt | llm | StrOutputParser()

def main():
    init_page()

    # 모델
    llm = ChatOpenAI(temperature=0)
    chain = init_chain(llm)

    # 입력 UI
    col1, col2 = st.columns(2)

    with col1:
        animal1 = st.text_input("동물 A", placeholder="호랑이")

    with col2:
        animal2 = st.text_input("동물 B", placeholder="사자")

    # 버튼
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

            # 강조 표시
            if "승자:" in result:
                winner = result.split("승자:")[-1].strip()
                st.success(f"최종 승자 👉 {winner}")

if __name__ == "__main__":
    main()
