import streamlit as st
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable in your .env file")

client = OpenAI(api_key=openai_api_key)

def generate_summary(prompt, text_model='gpt-3.5-turbo'):
    response = client.chat.completions.create(
        model=text_model,
        temperature=0,
        messages=[
            {"role": "system", "content": "You only help in studying. You help summarizing and making points with the given question or topic."},
            {"role": "user", "content": prompt}
        ]
    )
    summary = response.choices[0].message.content

    return summary

# Function to generate audio from text using gTTS
def generate_audio(text, filename='summary_audio.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

# Streamlit app
st.title('Study Helper')

text_input = st.text_area('Enter your text here:')

# Generate button
if st.button('Generate'):
    with st.spinner('Generating...'):
        # Generate summary text
        summary_text = generate_summary(text_input)
        
        # Display summary text
        st.write("Summary Text:")
        st.write(summary_text)

        # Generate audio from summary text
        audio_filename = generate_audio(summary_text)

        # Display audio
        st.audio(open(audio_filename, 'rb').read(), format='audio/mp3', start_time=0)

