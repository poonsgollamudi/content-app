import streamlit as st
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from dotenv import load_dotenv

# --- Config & API Key ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Missing API Key. Please add GEMINI_API_KEY to your .env file.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.5-flash"

# --- Helper Functions ---

def extract_video_id(url):
    """Extracts the ID from various YouTube URL formats."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_youtube_transcript(video_id):
    """
    Fetches transcript using the modern v1.x API methods.
    """
    try:
        # Create an instance of the API
        api = YouTubeTranscriptApi()
        
        # In v1.0+, use .list() instead of .list_transcripts()
        transcript_list = api.list(video_id)
        
        # Automatically find the best English transcript (Manual or Generated)
        transcript = transcript_list.find_transcript(['en'])
        
        # Fetch the data
        transcript_data = transcript.fetch()
        
        # Build the text: Newer versions return objects with .text attributes
        # while older ones return dictionaries. This handles both.
        full_text = ""
        for segment in transcript_data:
            if hasattr(segment, 'text'):
                full_text += segment.text + " "
            else:
                full_text += segment.get('text', '') + " "
                
        return full_text.strip()
        
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_with_gemini(transcript):
    """Sends the transcript to Gemini for a fun summary."""
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

# --- Streamlit UI ---
st.set_page_config(page_title="YT Short-Cut", page_icon="📺")

st.title("📺 YT Short-Cut")
st.markdown("### Simple, reliable video summaries.")

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