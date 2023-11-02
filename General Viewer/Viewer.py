import gradio as gr
import os
from PIL import Image

def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(os.path.join(folder, filename))
            if img is not None:
                images[filename] = img
    return images

def image_viewer(folder, image_name):
    images = load_images_from_folder(folder)
    return images[image_name] if image_name in images else "No images found in the directory"

iface = gr.Interface(fn=image_viewer, inputs=["text", "text"], outputs="image")
iface.launch()
