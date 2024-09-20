import openai
import streamlit as st
import tiktoken
import datetime

def generate_blog_promotion_content_zeroshot(lecture_name, target_audience, api_key):
  
  openai.api_key = api_key
  
  prompt = f"""
  목표:
  - {target_audience}도 쉽게 이해할 수 있는 {lecture_name}의 홍보 문구를 작성해 주세요.
  - 내용을 명확하고 매력적으로 작성하여 사람들이 수강하고 싶도록 만들어 주세요.

  맥락:
  - {target_audience}을 대상으로 하여 {lecture_name}에 관심이 있는 분들에게 적합한 내용으로 구성해 주세요.
  - {target_audience}가 부담 없이 참여할 수 있도록 강의 내용을 쉽게 설명해 주세요.

  지시사항:
  - {lecture_name}의 주요 개념을 {target_audience}이 이해할 수 있도록 간결하고 명확하게 설명해 주세요.
  - {lecture_name}이 실제 생활에서 어떻게 도움이 되는지 구체적으로 설명하여 {target_audience}이 배우고 싶어 하도록 유도해 주세요.
  - 강의 개요, 커리큘럼, 강사 소개, 수강 혜택, 신청 방법을 명확하게 작성해 주세요.
  - 최신 정보와 관련성을 유지하기 위해 인터넷에서 검색한 내용을 참고해 주세요.
  - 홍보 문구 마지막에 주요 핵심 키워드를 #키워드 형태로 포함해 주세요.
  - 전체적으로 친근한 어조를 유지하며, 이모티콘을 충분히 사용해 주세요.

  제약사항:
  - 친근하고 부드러운 톤을 유지해 주세요.
  - 마지막에는 즉시 수강을 결심하도록 유도하는 콜투액션을 포함해 주세요.

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
  - Please write a promotional message for {lecture_name} that {target_audience} can easily understand.
  - Please make the content clear and appealing so that people feel motivated to enroll.

  Context:
  - Please create content tailored for {target_audience}, making it relevant for those interested in {lecture_name}.
  - Please explain the contents of the lecture easily so that {target_audience} can participate without hesitation.

  Instructions:
  - Please explain the key concepts of {lecture_name} clearly so that {target_audience} can understand.
  - Please explain specifically how {lecture_name} helps in real life and encourage {target_audience} to want to learn.
  - Please write clearly a brief introduction, curriculum, instructor introduction, course benefits, and how to apply. 
  - Please refer to information from the internet to maintain up-to-date relevance.
  - Please add key hashtags at the end of the content in the format #Keyword.
  - Please keep a friendly tone overall, and use a lot of emojis.
  - Please write the output in Korean and ensure that it is naturally translated.

  Restrictions:
  - Please keep a friendly and soft tone.
  - At the end, please include a call-to-action that encourages immediate enrollment.

  Expected Output:
  - Format: Blog promotional content
  - Length: 700-1000 characters
  - Tone & Manner: Informative, persuasive, and friendly
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
          
          tab1, tab2 = st.tabs(["**KOR**", "**ENG**"])

          with tab1:
            start = datetime.now()
            zeroshot_result = generate_blog_promotion_content_zeroshot(lecture_name, target_audience, api_key)
            content = zeroshot_result[0]
            bill = zeroshot_result[1]
        
            result_container = st.container(border=True)
            result_container.text(f"분석 소요 시간은 {datetime.now() - start} 입니다.")
            result_container.write(f"예상되는 부과 비용은 ${bill} 입니다.")
            st.write(content)
            
          with tab2:
            start = datetime.now()
            zeroshot_eng_result = generate_blog_promotion_content_zeroshot_eng(lecture_name, target_audience, api_key)
            content = zeroshot_eng_result[0]
            bill = zeroshot_eng_result[1]
        
            result_container = st.container(border=True)
            result_container.text(f"분석 소요 시간은 {datetime.now() - start} 입니다.")
            result_container.write(f"예상되는 부과 비용은 ${bill} 입니다.")
            st.write(content)
          
          st.success(":tada: 홍보 콘텐츠가 생성되었습니다!")
      else:
        st.error(":warning: 강의명과 대상을 입력해주세요!")


if __name__ == "__main__":
    main()

