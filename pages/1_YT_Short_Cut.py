import streamlit as st
import os
import re
import requests
from google import genai
from dotenv import load_dotenv

# --- Config & API Key ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY")

if not GEMINI_API_KEY:
    st.error("Missing API Key. Please add GEMINI_API_KEY to your .env file.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.5-flash"

def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_youtube_transcript(video_id):
    try:
        response = requests.get(
            "https://api.supadata.ai/v1/youtube/transcript",
            headers={"x-api-key": SUPADATA_API_KEY},
            params={"videoId": video_id, "text": "true"},
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("content", "")
        if isinstance(content, list):
            return " ".join(seg.get("text", "") for seg in content)
        return content
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_with_gemini(transcript):
    prompt = f"""
    You are a fun, high-energy YouTube content summarizer.
    I will provide a transcript of a video. Your job is to:
    1. Give it a catchy 'New Title'.
    2. Write a 'Too Long; Didn't Watch' (TL;DW) section.
    3. List the 10 Golden Nuggets' (key takeaways) using emojis.
    4. A blog on the subject of the video.
    5. End with a 'Final Vibe' rating.

    Transcript:
    {transcript}
    """
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

# --- Streamlit UI (no set_page_config; set in main app) ---
st.title("📺 YT Short-Cut")
st.markdown("### Simple, reliable video summaries.")

if not SUPADATA_API_KEY:
    st.error("Missing SUPADATA_API_KEY. Please add it to your .env file or Streamlit secrets.")
    st.stop()

yt_url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Distill Video", type="primary"):
    if yt_url:
        video_id = extract_video_id(yt_url)
        if video_id:
            with st.spinner("🎧 Reading the video transcript..."):
                transcript_text = get_youtube_transcript(video_id)
                if not transcript_text.startswith("Error:"):
                    with st.spinner("🧠 Summarizing with Gemini..."):
                        summary = summarize_with_gemini(transcript_text)
                        st.divider()
                        st.markdown(summary)
                        with st.expander("Show Full Transcript"):
                            st.write(transcript_text)
                else:
                    st.error(f"Could not fetch transcript. {transcript_text}")
        else:
            st.error("Invalid YouTube URL.")
    else:
        st.warning("Please paste a link first!")
