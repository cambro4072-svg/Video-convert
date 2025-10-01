import streamlit as st
import subprocess
import os
import tempfile

st.title("🎥 MP4 Video Converter")
st.write("Convert MP4 to AMV, AVI, MP3, MKV, MOV, and more using FFmpeg.")

# Upload file
uploaded_file = st.file_uploader("Choose an MP4 file", type=["mp4"])

# Format selector
formats = ["amv", "avi", "mp3", "mkv", "mov", "flv", "wmv"]
output_format = st.selectbox("Select output format", formats)

if uploaded_file is not None:
    st.video(uploaded_file)

    if st.button("Convert"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
            temp_input.write(uploaded_file.read())
            temp_input.flush()
            base = os.path.splitext(temp_input.name)[0]
            output_file = f"{base}_converted.{output_format}"

            # Run ffmpeg
            ffmpeg_cmd = ["ffmpeg", "-i", temp_input.name, "-y", output_file]
            process = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if process.returncode == 0:
                with open(output_file, "rb") as f:
                    st.success("✅ Conversion complete!")
                    st.download_button(
                        label="Download converted file",
                        data=f,
                        file_name=f"converted.{output_format}",
                        mime="application/octet-stream"
                    )
            else:
                st.error("❌ Conversion failed. Check FFmpeg installation.")