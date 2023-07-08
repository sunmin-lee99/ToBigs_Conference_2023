# python -m venv nlp_confer   
# source nlp_confer/Scripts/activate
# pip install transformers requests pillow matplotlib torch torchvision torchaudio
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import matplotlib.pyplot as plt
import matplotlib.image as img

model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

img_path = './img/single_concept3.jpg'
img_test = img.imread(img_path)
plt.imshow(img_test)
plt.show()

raw_image = Image.open(img_path).convert('RGB')
# conditional image captioning
text = "a drawing of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

