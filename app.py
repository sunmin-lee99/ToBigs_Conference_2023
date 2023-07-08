# pip3 install streamlit
# streamlit run app.py
import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

uploaded_file = st.file_uploader("Upload Image")

model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

raw_image = Image.open(uploaded_file).convert('RGB')
# conditional image captioning
text = "a drawing of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
#print(processor.decode(out[0], skip_special_tokens=True))

st.image(raw_image, caption=processor.decode(out[0], skip_special_tokens=True))
