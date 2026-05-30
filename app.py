# pyrefly: ignore [missing-import]
import streamlit as st
import fitz  # PyMuPDF
import edge_tts
import asyncio
import tempfile
import os
import re

st.set_page_config(page_title="PDF to Audiobook Converter", page_icon="🎧", layout="centered")

VOICE_OPTIONS = {
    "US English (Female)": "en-US-AriaNeural",
    "US English (Male)": "en-US-GuyNeural",
    "UK English (Female)": "en-GB-SoniaNeural",
    "UK English (Male)": "en-GB-RyanNeural",
    "Indian English (Female)": "en-IN-NeerjaNeural",
    "Indian English (Male)": "en-IN-PrabhatNeural",
    "Australian English (Female)": "en-AU-NatashaNeural",
    "Australian English (Male)": "en-AU-WilliamNeural"
}

st.title("🎧 PDF to Audiobook Converter")
st.markdown("Convert your PDF documents into MP3 audiobooks easily. Upload your file below to get started!")

# Add voice selection
selected_voice_label = st.selectbox("🗣️ Select Voice / Accent", list(VOICE_OPTIONS.keys()))
selected_voice_id = VOICE_OPTIONS[selected_voice_label]

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.info("PDF uploaded successfully! Extracting text...")
    
    try:
        # Read the PDF
        # We need to read the uploaded file bytes for PyMuPDF
        pdf_bytes = uploaded_file.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        
        # Adding a progress bar for text extraction
        progress_bar = st.progress(0)
        num_pages = len(pdf_document)
        
        for page_num in range(num_pages):
            page = pdf_document.load_page(page_num)
            extracted_text = page.get_text()
            if extracted_text:
                text += extracted_text + "\n"
            progress_bar.progress((page_num + 1) / num_pages)
        
        # Clean the text: remove newlines and multiple spaces which cause spelling issues
        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text).strip()

        if text == "":
            st.error("No text could be extracted from this PDF. It might consist only of scanned images.")
        else:
            st.success("Text extracted successfully! Generating audio...")
            
            with st.spinner('Converting text to speech... This may take a few minutes for larger documents.'):
                # Save to a temporary file
                temp_dir = tempfile.gettempdir()
                temp_file_path = os.path.join(temp_dir, "audiobook.mp3")
                
                # Generate Audio using edge-tts
                async def generate_audio():
                    communicate = edge_tts.Communicate(text, selected_voice_id)
                    await communicate.save(temp_file_path)
                
                asyncio.run(generate_audio())
                
            st.success("Audiobook generated successfully!")
            
            # Display audio player
            st.audio(temp_file_path, format="audio/mp3")
            
            # Provide download button
            with open(temp_file_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download Audiobook (MP3)",
                    data=file,
                    file_name=f"{uploaded_file.name.replace('.pdf', '')}_audiobook.mp3",
                    mime="audio/mp3"
                )
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
