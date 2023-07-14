# pip3 install streamlit
# streamlit run app.py
import replicate
# !pip install replicate
import openai # pip install openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from transformers import BlipProcessor, BlipForConditionalGeneration
import re
uploaded_file = st.file_uploader("Upload Image")

model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

raw_image = Image.open(uploaded_file).convert('RGB')
# conditional image captioning
text = "a drawing of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
#print(processor.decode(out[0], skip_special_tokens=True))

st.image(raw_image)
st.write(processor.decode(out[0], skip_special_tokens=True))


openai.api_key = "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"  # api key error 발생하면 연락주세요

prompt = processor.decode(out[0], skip_special_tokens=True)   # prompt 입력 받는 부분 
model="gpt-3.5-turbo"
temperature= 0.2          

# promt를 바탕으로 영어 동화 생성
messages_story_eng =[{"role": "user",
                        "content": "%sUse this sentence to create a child story with a twist of up to 1000 characters."%prompt}]

completion_story_eng = openai.ChatCompletion.create(
    model= model,
    messages= messages_story_eng,
    temperature=temperature
    )
print("*"*20)
print(1)
print(completion_story_eng.choices[0].message.content)   # 이 부분 return 으로 바꾸기
#st.write(completion_story_eng.choices[0].message.content)
#st.divider()
# 위에서 생성한 영어 동화를 한국어로 번역(동화체)
messages_story_kor =[{"role": "user",
                        "content": "%s 이 동화 내용을 한국어로 번역하고 동화체로 만들어줘."%completion_story_eng.choices[0].message.content}]

completion_story_kor = openai.ChatCompletion.create(
    model= model,
    messages= messages_story_kor,
    temperature=temperature
    )
print("*"*20)
print(2)
print(completion_story_kor.choices[0].message.content)  # 이 부분 return 으로 바꾸기
#for i in completion_story_kor.choices[0].message.content.split('\n'):
#    st.write(i)
#    st.divider()
"""st.write(completion_story_kor.choices[0].message.content)
st.divider()"""
# 위에서 생성한 영어 동화를 바탕으로 장면을 생성하기 좋은 프롬프트로 변경 
messages_story_prompt =[{"role": "user",
                        "content": "%s  Generate appropriate prompts for each scene, such as 'banana on the dish', \
                        so that a picture can be created based on this story."%completion_story_eng.choices[0].message.content}]

completion_story_prompt = openai.ChatCompletion.create(
    model= model,

    
    messages= messages_story_prompt,
    temperature=temperature
    )

print("*"*20)
print(3)
print(completion_story_prompt.choices[0].message.content)  # 이 부분 return 으로 
prompt_list=[]
for i in completion_story_prompt.choices[0].message.content.split('\n'):
    new_str = re.sub(r"[0-9]", "", i)
    #st.write(i[2:])
    prompt_list.append(i[2:])
    #st.divider()

print("끝")


class StyleAPI:
    def __init__(self, api_token, model_name):
        self.api_token = api_token
        self.model_name = model_name
        self.client = replicate.Client(api_token=self.api_token)

    def run_style_api(self, prompt_list):
        outputs = []
        style = "kid crayon drawing"

        for prompt in prompt_list:
            processed_prompt = prompt.replace("Max", "A puppy")
            input_data = {
                "prompt": processed_prompt,
                "style_adapter": style,
                "num_samples": 1,
                "sample_steps": 50
            }
            output = self.client.run(
                self.model_name,
                input=input_data
            )

            outputs.append(output)

        return outputs


api_token = "r8_P5WSPEac15Wg9yirNapsltFxBO0qTwt2QcLd5"
model_name = "cjwbw/styledrop:d0174762791a4fbe47e051c8348304ca31ab8058007e91d9a70eaf66e95c77a9"

style_api = StyleAPI(api_token, model_name)


api_outputs = style_api.run_style_api(prompt_list)

for i, output in enumerate(api_outputs):
    print(f"Output for prompt {i+1}:")

    image_url = output[0]
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    #image.show()
    st.image(image)
    st.write(prompt_list[i])
    print("\n")