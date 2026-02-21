"""
Content App — one entry point for all Streamlit apps.
Run: streamlit run streamlit_app.py
Use the sidebar to switch between apps.
"""
import streamlit as st

st.set_page_config(
    page_title="Content App",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📦 Content App")
st.markdown("### One place for all your content tools.")

st.markdown("""
Choose an app from the **sidebar** (left):

- **📺 YT Short-Cut** — Summarize YouTube videos (titles, TL;DR, nuggets, blog).
- **🪄 Content Distiller** — Turn articles into executive summary, LinkedIn post, ELI5, and blog.
- **📺 YT Global Short-Cut** — Translate and interpret YouTube videos (any language, anime, songs).

Each app uses your `GEMINI_API_KEY` from `.env`.
""")

st.divider()
st.caption("Run with: `streamlit run streamlit_app.py`")
