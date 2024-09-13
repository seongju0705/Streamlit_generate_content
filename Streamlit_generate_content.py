import openai
import streamlit as st
import tiktoken
from datetime import datetime

def generate_blog_promotion_content_zeroshot(lecture_name, target_audience, api_key):
  
  openai.api_key = api_key
  
  prompt = f"""
  목표:
  - {target_audience}도 쉽게 이해할 수 있는 {lecture_name}의 홍보 문구를 작성해 주세요.
  - 강의의 특징과 수강 혜택을 명확하게 전달하여 사람들이 수강하고 싶도록 만들어 주세요.

  맥락:
  - {target_audience}을 대상으로 하여 {lecture_name}에 관심이 있는 분들에게 적합한 내용으로 구성해 주세요.
  - {target_audience}가 부담 없이 참여할 수 있도록 강의 내용을 쉽게 설명해 주세요.

  지시사항:
  - {lecture_name}의 주요 개념을 {target_audience}이 이해할 수 있도록 간결하고 명확하게 설명해 주세요.
  - 강의의 개요, 차별화된 특징, 그리고 수강 혜택을 명확하게 포함해 주세요.
  - {lecture_name}이 실제 생활에서 어떻게 도움이 되는지 구체적으로 설명하여 {target_audience}이 배우고 싶어 하도록 유도해 주세요.
  - 최신 정보와 관련성을 유지하기 위해 인터넷에서 검색한 내용을 참고해 주세요.
  - 홍보 문구 마지막에 주요 핵심 키워드를 #키워드 형태로 포함해 주세요.
  - 전체적으로 친근한 어조를 유지하며, 적절히 이모티콘을 사용하여 독자와의 친밀감을 높여 주세요.

  제약사항:
  - 핵심 키워드 중심으로 작성해 주세요. 
  - 문단과 주요 포인트 사이에 적절한 줄 바꿈을 추가해 주세요.

  결과 설정:
  - 형식: 블로그 홍보 문구
  - 길이: 700~1000자
  - 톤 & 매너: 정보 제공적이고 설득력 있으며, 친근한 어조로 작성해 주세요.
  """
  
  response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 블로그 홍보 콘텐츠를 작성하는 마케터입니다."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000
  )
  
  prompt_result = response.choices[0].message.content    
  
  encoder = tiktoken.get_encoding("cl100k_base")
  input_token = len(encoder.encode(prompt))
  output_token = len(encoder.encode(prompt_result))
  expected_sum_bill = (input_token * (0.005/1000)) + (output_token * (0.015/1000))

  return prompt_result, expected_sum_bill
  


def generate_blog_promotion_content_zeroshot_eng(lecture_name, target_audience, api_key):
  
  openai.api_key = api_key
  
  prompt = f"""
  Objective:
  - Write a promotional text for {lecture_name} that is easy for {target_audience} to understand.
  - Clearly highlight the course features and benefits to motivate people to enroll.

  Context:
  - The content should be tailored for {target_audience} who are interested in {lecture_name}.
  - Explain the course content in a simple way so {target_audience} feel comfortable participating.

  Instructions:
  - Clearly and concisely explain the key concepts of {lecture_name} in a way {target_audience} can understand.
  - Include the course overview, key features, and benefits.
  - Show how {lecture_name} can be practically applied to daily life, encouraging {target_audience} to learn.
  - Include relevant, up-to-date information based on internet research.
  - Add key hashtags at the end of the text in the formaLLt #Keyword.
  - Keep a friendly tone and use emojis to increase engagement.

  Restrictions:
  - Avoid technical jargon and use simple language.
  - Maintain appropriate line breaks between paragraphs and key points.
  - **The final response should be in Korean.**

  Result:
  - Format: Blog promotional text
  - Length: 700-1000 characters
  - Tone & Style: Informative, persuasive, and friendly
  """
  
  response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 블로그 홍보 콘텐츠를 작성하는 마케터입니다."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000
  )
  
  prompt_result = response.choices[0].message.content    
  
  encoder = tiktoken.get_encoding("cl100k_base")
  input_token = len(encoder.encode(prompt))
  output_token = len(encoder.encode(prompt_result))
  expected_sum_bill = (input_token * (0.005/1000)) + (output_token * (0.015/1000))

  return prompt_result, expected_sum_bill
  

def main():
  st.set_page_config(page_title="블로그 홍보 콘텐츠 생성기", page_icon=":loudspeaker:", layout="centered")  
  st.sidebar.header(":loudspeaker: 블로그 홍보 콘텐츠 생성하기")
  st.subheader("강의명과 대상을 입력하고, 맞춤형 블로그 홍보 콘텐츠를 생성하세요! :sparkles:")  
  
  api_key = st.sidebar.text_input("Openai API Key를 입력하세요.")
  st.sidebar.divider()
  lecture_name = st.sidebar.text_input(label="강의명을 입력하세요.", placeholder="예: 데이터 분석, Python 기초")
  target_audience = st.sidebar.text_input(label="대상을 입력하세요.", placeholder="예: 비전공자, 직장인")

  if st.sidebar.button(":memo: 홍보 콘텐츠 생성"):
      if lecture_name and target_audience:
        with st.spinner("콘텐츠를 생성 중입니다..."):
          zeroshot_result = generate_blog_promotion_content_zeroshot(lecture_name, target_audience, api_key)
          zeroshot_eng_result = generate_blog_promotion_content_zeroshot_eng(lecture_name, target_audience, api_key)
          st.success(":tada: 홍보 콘텐츠가 생성되었습니다!")
          
          tab1, tab2 = st.tabs(["**KOR**", "**ENG**"])

          with tab1:
            content = zeroshot_result[0]
            bill = zeroshot_result[1]
        
            result_container = st.container(border=True)
            result_container.write(f"예상되는 부과 비용은 ${bill} 입니다.")
            st.write(content)
            
          with tab2:
            content = zeroshot_eng_result[0]
            bill = zeroshot_eng_result[1]
        
            result_container = st.container(border=True)
            result_container.write(f"예상되는 부과 비용은 ${bill} 입니다.")
            st.write(content)
      else:
        st.error(":warning: 강의명과 대상을 입력해주세요!")


if __name__ == "__main__":
    main()

