import streamlit as st
import requests
from streamlit_lottie import st_lottie
from modules import download_youtube_video, save_uploaded_video, transcribe_video, match_candidate

# Load Lottie animation JSON from URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def inject_css():
    st.markdown(
        """
        <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        /* General app style */
        .stApp {
            background-color: #f4f6f8;
            color: #222;
            font-family: 'Roboto', sans-serif;
            padding: 40px 60px;
        }

        /* Headers */
        h1, h2 {
            color: #4B8BBE;
            font-weight: 700;
            margin-bottom: 0.4em;
        }

        /* Section card */
        .section-card {
            background-color: white;
            padding: 30px 40px;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgb(0 0 0 / 0.08);
            margin-bottom: 50px;
        }

        /* Inputs */
        .stTextInput>div>div>input, .stTextArea>div>textarea {
            background-color: #f9fbfc;
            color: #333;
            border: 1.8px solid #ccc;
            border-radius: 12px;
            padding: 14px;
            font-size: 17px;
            transition: border-color 0.3s ease;
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>textarea:focus {
            border-color: #4B8BBE;
            outline: none;
            box-shadow: 0 0 10px #4B8BBE;
        }

        /* File uploader */
        .stFileUploader > div > div {
            border: 2px dashed #ccc;
            border-radius: 12px;
            padding: 50px;
            background-color: #fafafa;
            color: #777;
            transition: border-color 0.3s ease;
        }
        .stFileUploader > div > div:hover {
            border-color: #4B8BBE;
            color: #333;
        }

        /* Buttons */
        button[data-baseweb="button"] {
            background-color: #4B8BBE !important;
            color: white !important;
            font-weight: 700;
            border-radius: 12px !important;
            padding: 14px 40px !important;
            font-size: 18px;
            box-shadow: 0 6px 16px rgb(75 139 190 / 0.5);
            transition: background-color 0.3s ease;
            margin-top: 20px;
        }
        button[data-baseweb="button"]:hover:not(:disabled) {
            background-color: #357ABD !important;
            cursor: pointer;
            box-shadow: 0 8px 22px rgb(53 122 189 / 0.7);
        }
        button[data-baseweb="button"]:disabled {
            background-color: #bbb !important;
            color: #eee !important;
            cursor: not-allowed;
            box-shadow: none;
        }

        /* Info and status messages */
        .stInfo, .stSuccess, .stWarning, .stError {
            font-weight: 600;
            font-size: 16px;
            margin: 18px 0;
        }

        /* Centered and spaced main title */
        .main-title {
            text-align: center;
            margin-bottom: 50px;
            font-size: 42px;
            letter-spacing: 1.2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
def main():
    st.set_page_config(page_title="🎯 Smart Interview Analyzer", layout="wide", initial_sidebar_state="collapsed")

    inject_css()

    # Lottie animation
    lottie_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_j1adxtyb.json")
    if lottie_animation:
        st_lottie(lottie_animation, height=180, key="header_anim")

    st.markdown('<h1 class="main-title">🎯 Smart Interview Analyzer</h1>', unsafe_allow_html=True)

    # Section 1: Upload or Download Video
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.header("Step 1: Upload or Download Interview Video")

        col1, col2 = st.columns([1, 2])
        with col1:
            upload_option = st.radio(
                "Input method:",
                ("Upload Video", "YouTube URL"),
                index=0,
                label_visibility="visible",
            )
        with col2:
            video_path = None
            if upload_option == "Upload Video":
                uploaded_file = st.file_uploader(
                    "Upload interview video (mp4 or mov)",
                    type=["mp4", "mov"],
                    key="video_uploader",
                )
                if uploaded_file:
                    video_path = save_uploaded_video(uploaded_file)
                    st.success("✅ Video uploaded successfully!")
                    st.session_state["video_path"] = video_path
            else:
                yt_url = st.text_input("Enter YouTube video URL", key="yt_url_input")
                if yt_url and ("video_downloaded" not in st.session_state or st.session_state["video_downloaded"] != yt_url):
                    with st.spinner("Downloading YouTube video..."):
                        video_path = download_youtube_video(yt_url)
                    if video_path:
                        st.success("✅ YouTube video downloaded!")
                        st.session_state["video_downloaded"] = yt_url
                        st.session_state["video_path"] = video_path
                    else:
                        st.error("❌ Could not download the video. Check the URL.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Auto transcription (hidden)
    if "video_path" in st.session_state and "transcript" not in st.session_state:
        with st.spinner("Transcribing video... this might take a minute"):
            transcript = transcribe_video(st.session_state["video_path"])
            st.session_state["transcript"] = transcript
        st.success("✅ Transcription complete!")

    # Section 2: Job requirements
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.header("Step 2: Enter Job Requirements")

        job_requirements = st.text_area(
            "Describe job requirements or qualifications",
            placeholder="e.g. strong communication, teamwork, problem-solving skills...",
            height=150,
            key="job_req_area",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Section 3: Match candidate
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.header("Step 3: Analyze Candidate Match")

        can_analyze = ("transcript" in st.session_state) and job_requirements.strip() != ""
        if not can_analyze:
            if "transcript" not in st.session_state:
                st.info("Please upload/download and transcribe a video first.")
            if job_requirements.strip() == "":
                st.info("Please enter the job requirements.")

        if st.button("🔎 Get Match Score", disabled=not can_analyze):
            with st.spinner("Analyzing candidate..."):
                score = match_candidate(st.session_state["transcript"], job_requirements)
            st.success("✅ Analysis complete!")
            st.markdown(f"### Match Score:\n{score}")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
