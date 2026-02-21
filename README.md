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

### 1. YouTube Summarizer (YT Short-Cut)
Summarize YouTube videos with catchy titles, TL;DR sections, and key takeaways.

```bash
streamlit run youtube_summarizer.py
```

### 2. Website Content Distiller
Distill website content into executive summaries, LinkedIn posts, ELI5 explanations, and blog posts.

```bash
streamlit run websites_interpreter.py
```

### 3. YouTube Cultural Translator (YT Global Short-Cut)
Translate and interpret YouTube videos from any language, perfect for anime, songs, and global content.

```bash
streamlit run youtube_cultural_translator.py
```

## Features

- **YouTube Summarizer**: Extract transcripts and generate fun, high-energy summaries with emojis
- **Content Distiller**: Transform web articles into multiple content formats
- **Cultural Translator**: Translate and interpret content from any language with cultural context

All apps will automatically open in your default web browser at `http://localhost:8501`.
