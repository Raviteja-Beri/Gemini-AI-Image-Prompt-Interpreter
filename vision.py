from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(user_input, image=None):
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')

        if user_input and image:
            response = model.generate_content([user_input, image])
        elif image:
            response = model.generate_content([image])
        else:
            response = model.generate_content(user_input)

        if response.candidates and response.candidates[0].content.parts:
            return "".join(
                [part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')]
            )
        else:
            return "No valid response returned"
    except Exception as e:
        return f"Gemini API error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Gemini AI Image Demo")
st.header("Gemini AI Multi Application")

user_input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

if st.button("Tell me about the image"):
    result = get_gemini_response(user_input, image)
    st.subheader("The Response is")
    st.write(result)
