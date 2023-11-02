import os
import gradio as gr
from PIL import PngImagePlugin

def process_images(dir_path):
    # First, rename all the PNG files in the directory
    png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
    for i, filename in enumerate(sorted(png_files), start=1):
        new_filename = f'{i:03}.png'
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))

    # Then, extract the prompts from the renamed files
    for i in range(1, len(png_files)+1):
        # Open the image file
        img = PngImagePlugin.PngImageFile(os.path.join(dir_path, f'{i:03}.png'))

        # Extract the text from the image file
        with open(os.path.join(dir_path, f'{i:03}.png'), mode='rb') as file:
            text = file.read().decode(errors='ignore')

        # Find the start and end of the positive prompts
        start = text.find('parameters')
        end = text.find('Negative prompt:')
        prompts = text[start+10:end].strip()

        # Remove the specific string from the prompts
        prompts = prompts.replace(' <hypernet:SHSID:0.6>', '')

        # Write the prompts to a new .txt file
        with open(os.path.join(dir_path, f'{i:03}.txt'), 'w') as f:
            f.write(prompts)

    return "Processing complete!"

# Define Gradio interface
iface = gr.Interface(fn=process_images, inputs="text", outputs="text")
iface.launch()
