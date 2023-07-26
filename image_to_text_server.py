import base64
from io import BytesIO
from PIL import Image
import torch
from transformers import BlipForConditionalGeneration, BlipProcessor

from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base", torch_dtype=torch.float32).to("cpu")  # type: ignore

def resize_image(image, scale_factor=2, min_width=350, min_height=350):
    width, height = image.size
    new_width, new_height = width, height
    
    if width > min_width * scale_factor:
        new_width = width // scale_factor
    if height > min_height * scale_factor:
        new_height = height // scale_factor
    
    new_size = (new_width, new_height)
    image.thumbnail(new_size)
    
    return image


def caption_image(raw_image, num_beams=3):
    inputs = processor(raw_image.convert('RGB'), return_tensors="pt").to("cpu", torch.float32)  # type: ignore
    if num_beams is None:
        out = model.generate(**inputs, max_new_tokens=100)
    else:
        out = model.generate(**inputs, max_new_tokens=100, num_beams=num_beams)
    return processor.decode(out[0], skip_special_tokens=True)

@app.route("/caption_image", methods=["POST"])
def api_caption_image():
    data = request.files['image']
    image = Image.open(data.stream)
    
    resized_image = resize_image(image)
    detailed_caption = caption_image(resized_image, num_beams=10)  # Increase num_beams value for more detailed description
    print(detailed_caption)
    
    return jsonify({"caption": detailed_caption})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2000)
