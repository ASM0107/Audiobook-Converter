import streamlit as st
from pypdf import PdfReader
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="PDF to Audiobook Converter", page_icon="🎧", layout="centered")

st.title("🎧 PDF to Audiobook Converter")
st.markdown("Convert your PDF documents into MP3 audiobooks easily. Upload your file below to get started!")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.info("PDF uploaded successfully! Extracting text...")
    
    try:
        # Read the PDF
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        
        # Adding a progress bar for text extraction
        progress_bar = st.progress(0)
        num_pages = len(pdf_reader.pages)
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
            progress_bar.progress((page_num + 1) / num_pages)
        
        if text.strip() == "":
            st.error("No text could be extracted from this PDF. It might consist only of scanned images.")
        else:
            st.success("Text extracted successfully! Generating audio...")
            
            with st.spinner('Converting text to speech... This may take a few minutes for larger documents.'):
                # Generate Audio
                tts = gTTS(text=text, lang='en')
                
                # Save to a temporary file
                temp_dir = tempfile.gettempdir()
                temp_file_path = os.path.join(temp_dir, "audiobook.mp3")
                
                tts.save(temp_file_path)
                
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
