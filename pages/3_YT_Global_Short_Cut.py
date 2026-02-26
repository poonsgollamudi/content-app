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
    You are a high-energy content interpreter and cultural expert.
    If the following transcript is not in English, first translate the core meaning into English.

    If this is a song or anime clip, provide deep interpretation of the themes and lyrics.

    Your output must follow this structure:
    1. 📺 **Catchy New Title**: (A creative English title)
    2. 📝 **TL;DW**: (A conversational summary of what happens/is said)
    3. 💎 **10 Golden Nuggets**: (10 punchy takeaways or lyrical meanings with emojis)
    4. 📈 **Final Vibe Rating**: (X/10 rating)

    Transcript:
    {transcript}
    """
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

# --- Streamlit UI ---
st.title("📺 YT Global Short-Cut")
st.markdown("### Anime, Songs, and Global Content Distiller.")

if not SUPADATA_API_KEY:
    st.error("Missing SUPADATA_API_KEY. Please add it to your .env file or Streamlit secrets.")
    st.stop()

yt_url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Distill Video", type="primary"):
    if yt_url:
        video_id = extract_video_id(yt_url)
        if video_id:
            with st.spinner("🎧 Reading the video transcript (Any Language)..."):
                transcript_text = get_youtube_transcript(video_id)
                if not transcript_text.startswith("Error:"):
                    with st.spinner("🧠 Translating and Summarizing..."):
                        summary = summarize_with_gemini(transcript_text)
                        st.divider()
                        st.markdown(summary)
                        with st.expander("Show Original Transcript"):
                            st.write(transcript_text)
                else:
                    st.error("Could not fetch transcript. This video might not have captions enabled.")
        else:
            st.error("Invalid YouTube URL.")
    else:
        st.warning("Please paste a link first!")
