# Content App

A collection of Streamlit applications for content analysis and summarization using Google's Gemini AI.

## Prerequisites

- Python 3.13+
- A Google Gemini API key

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Streamlit Apps

**All 3 apps on one page (recommended)** — one URL, sidebar menu to switch apps:

```bash
streamlit run streamlit_app.py
```

Then use the **sidebar** to open: **YT Short-Cut**, **Content Distiller**, or **YT Global Short-Cut**. The app opens at `http://localhost:8501`.

---

**Run a single app** (optional):

```bash
streamlit run youtube_summarizer.py      # YT Short-Cut
streamlit run websites_interpreter.py   # Content Distiller
streamlit run youtube_cultural_translator.py   # YT Global Short-Cut
```

## Features

- **YouTube Summarizer**: Extract transcripts and generate fun, high-energy summaries with emojis
- **Content Distiller**: Transform web articles into multiple content formats
- **Cultural Translator**: Translate and interpret content from any language with cultural context

All apps will automatically open in your default web browser at `http://localhost:8501`.
