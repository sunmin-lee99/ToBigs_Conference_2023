import openai # pip install openai

openai.api_key = "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"  # api key error 발생하면 연락주세요

prompt = 'a drawing of a boy kicking a soccer ball on a field'   # prompt 입력 받는 부분 
model="gpt-3.5-turbo"
temperature= 0.2          

# promt를 바탕으로 영어 동화 생성
messages_story_eng =[{"role": "user",
                        "content": "%s Use this sentence to create a short children's story with a twist."%prompt}]

completion_story_eng = openai.ChatCompletion.create(
    model= model,
    messages= messages_story_eng,
    temperature=temperature
    )
print(completion_story_eng.choices[0].message.content)   # 이 부분 return 으로 바꾸기

# 위에서 생성한 영어 동화를 한국어로 번역(동화체)
messages_story_kor =[{"role": "user",
                        "content": "%s 이 동화 내용을 한국어로 번역하고 동화체로 만들어줘."%completion_story_eng.choices[0].message.content}]

completion_story_kor = openai.ChatCompletion.create(
    model= model,
    messages= messages_story_kor,
    temperature=temperature
    )
print(completion_story_kor.choices[0].message.content)  # 이 부분 return 으로 바꾸기

# 위에서 생성한 영어 동화를 바탕으로 장면을 생성하기 좋은 프롬프트로 변경 
messages_story_prompt =[{"role": "user",
                        "content": "%s  Generate appropriate prompts for each scene, such as 'banana on the dish', \
                        so that a picture can be created based on this story."%completion_story_eng.choices[0].message.content}]

completion_story_prompt = openai.ChatCompletion.create(
    model= model,
    messages= messages_story_prompt,
    temperature=temperature
    )
print(completion_story_prompt.choices[0].message.content)  # 이 부분 return 으로 바꾸기