import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai  # New SDK import
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("API Key not found. Please check your .env file.")
    st.stop()

# Initialize the new Client
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.5-flash"

def scrape_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
            
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs])
        return text if text.strip() else "No readable paragraph content found."
    except Exception as e:
        return f"Error scraping: {e}"

def distill_content(text):
    prompt = f"""
    You are an expert content strategist. Distill the following text into exactly these three formats:
    
    1. **Executive Summary**: A single, high-impact sentence.
    2. **LinkedIn Post**: Three punchy, professional bullet points.
    3. **ELI5**: A simple, easy-to-understand paragraph for a non-technical person.
    4. **Blog**: A witty but informative blog for everyone.

    Use clear headings for each section.

    Text to distill:
    {text}
    """
    
    # New SDK method: client.models.generate_content
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

# --- Streamlit Web UI ---
st.set_page_config(page_title="Content Distiller", page_icon="🪄", layout="wide")

st.title("🪄 Micro-Niche Content Distiller")
st.caption("Updated to the latest Google Gen AI SDK.")

url_input = st.text_input("Paste a URL (Blog, Research Paper, Article):", placeholder="https://example.com/article")

if st.button("Generate Insights", type="primary"):
    if url_input:
        with st.spinner("Reading and distilling content..."):
            raw_text = scrape_text(url_input)
            
            if not raw_text.startswith("Error"):
                result = distill_content(raw_text)
                
                st.divider()
                st.markdown(result)
                
                with st.expander("View Scraped Text"):
                    st.write(raw_text)
            else:
                st.error(f"Couldn't fetch the article. {raw_text}")
    else:
        st.warning("Please enter a URL first.")