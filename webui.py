import streamlit as st
import numpy as np
from PIL import Image
import model  # Assuming your modularized code is in a file named model.py

pipe = model.pipe  # Use the pipe object from your modularized code

# Add a logo and some descriptive text to the app
st.set_page_config(page_title='Moroccan Text-to-Image Generator', page_icon='🇲🇦',
                   layout='wide', initial_sidebar_state='collapsed')
st.title('Moroccan carpet Text-to-Image Generator')
st.write('Enter some text related to Moroccan concepts or styles in carpet. '
         'Click "Generate Image" to create a personalized and culturally relevant image based on the text. '
         'Note that the model may not always generate images that match the input text exactly.')

logo_image = Image.open('logo.png')
st.sidebar.image(logo_image)


def main():
    # User input
    input_text = st.text_input('Enter text:')
    generate_button = st.button('Generate Image')

    if generate_button and input_text:
        with st.spinner('Generating image...'):
            num_samples = 1
            num_inference_steps = 30
            guidance_scale = 7.5
            images = pipe([input_text] * num_samples, num_inference_steps=num_inference_steps,
                          guidance_scale=guidance_scale).images

            generated_image = images[0]

            st.image(generated_image, caption=f'Generated image: {input_text}')


if __name__ == '__main__':
    main()
