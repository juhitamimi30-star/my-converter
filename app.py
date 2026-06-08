import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Video Converter", layout="centered")
st.title("Video Processor")

uploaded_file = st.file_uploader("Upload video", type=["mp4", "mkv", "mov"])

if uploaded_file is not None:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.success("File uploaded successfully")
    
    if st.button("Process & Secure"):
        with st.spinner("Processing... please wait"):
            command = [
                'ffmpeg', '-y', 
                '-i', 'input_video.mp4',
                '-vf', 'hflip,eq=brightness=0.05:contrast=1.05', 
                '-c:v', 'libx264', '-crf', '28', '-preset', 'ultrafast', 
                '-c:a', 'copy', 
                'output_video.mp4'
            ]
            
            try:
                subprocess.run(command, check=True)
                
                if os.path.exists("output_video.mp4"):
                    st.success("Processing complete")
                    with open("output_video.mp4", "rb") as file:
                        st.download_button(
                            label="Download Secure Video",
                            data=file,
                            file_name="safe_video.mp4",
                            mime="video/mp4"
                        )
            except subprocess.CalledProcessError:
                st.error("Error: Processing failed")

if os.path.exists("input_video.mp4"):
    os.remove("input_video.mp4")
