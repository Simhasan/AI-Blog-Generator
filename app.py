import streamlit as st
import requests
import pyperclip
import markdown
import io
from datetime import datetime
import uuid
import re

# API keys (assumed to be stored in Streamlit secrets)
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
UNSPLASH_ACCESS_KEY = st.secrets["UNSPLASH_ACCESS_KEY"]
COHERE_API_URL = "https://api.cohere.ai/v1/generate"

# Page configuration (MUST BE FIRST)
st.set_page_config(page_title="AI Blog Generator", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px;
        font-weight: bold;
        transition: background-color 0.3s;
        min-width: 40px;
        text-align: center;
        margin: 0 1px; /* Minimal spacing */
    }
    
    .stTextInput>div>input {
        border-radius: 8px;
        border: 2px solid #d1d5db;
        padding: 10px;
    }
    .stSelectbox>div>div {
        border-radius: 8px;
        border: 2px solid #d1d5db;
    }
    
    .title {
        color: yellow;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #fad7a0;
        font-size: 1.2em;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        color: #fad7a0;
        font-size: 1.8em;
        font-weight: bold;
        margin-top: 0px;
        margin-bottom: 10px;
    }
    .expander {
        background-color: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        opacity: 1 !important; /* Ensure visibility */
    }
    .stExpander summary {
        font-weight: bold;
        color: #1f2937;
        opacity: 1 !important; /* Ensure summary is visible */
    }
    .stExpander {
        opacity: 1 !important; /* Ensure expander content is visible */
    }
    .stImage {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stats {
        padding: 10px;
        margin-bottom: 20px;
        font-size: 1em;
        color: #1f2937;
    }
    .icon-button {
        font-size: 1.2em;
        padding: 8px;
    }
    .button-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
        gap: 2px; /* Minimal gap in flex container */
    }
    </style>
""", unsafe_allow_html=True)

# Function to generate blog content
def generate_blog(topic, tone):
    prompt = f"""
    Write a comprehensive blog post about {topic} in a {tone} tone. The blog should be engaging and well-structured with:
    - A catchy title
    - An introduction (100-150 words)
    - 3-5 sections with descriptive subheadings (150-200 words each)
    - A conclusion with a strong call to action (100-150 words)
    - Include 2-3 relevant keywords related to {topic} naturally throughout the text
    - Format the output in Markdown
    - Aim for 600-800 words total
    """
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 0.7,
        "k": 0,
        "p": 0.75,
        "stop_sequences": [],
        "return_likelihoods": "NONE"
    }
    response = requests.post(COHERE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['generations'][0]['text']
    else:
        raise Exception(f"API request failed: {response.text}")

# Function to fetch images from Unsplash
@st.cache_data
def get_images(topic, count=3):
    url = f"https://api.unsplash.com/search/photos?query={topic}&per_page={count}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return [photo['urls']['regular'] for photo in response.json()['results']]
    return []

# Function to calculate word count and reading time
def calculate_stats(text):
    words = len(text.split())
    reading_time = round(words / 200)
    return words, reading_time

# Sidebar for navigation and history
with st.sidebar:
    st.header("Blog History")
    if "blogs" not in st.session_state:
        st.session_state.blogs = []
    for blog in st.session_state.blogs:
        with st.expander(f"{blog['topic']} ({blog['timestamp']})", expanded=True):  # Expand by default
            st.markdown(blog['content'][:200] + "...")
            if st.button("View Full", key=f"view_{blog['id']}"):
                st.session_state.selected_blog = blog['content']

# Main content
st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">AI Blog Post Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Create engaging, SEO-friendly blog posts in minutes!</div>', unsafe_allow_html=True)

# Input form
with st.form("blog_form"):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Create Your Blog</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("Blog Topic", placeholder="e.g., Sustainable Gardening Tips", help="Enter a specific topic for your blog post")
    with col2:
        tone = st.selectbox("Tone of Writing", ["Professional", "Friendly", "Persuasive", "Witty"], help="Choose the tone that matches your audience")
    submitted = st.form_submit_button("Generate Blog")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle form submission
if submitted and topic:
    with st.spinner("Crafting your blog post..."):
        try:
            blog_content = generate_blog(topic, tone)
            images = get_images(topic)
            word_count, reading_time = calculate_stats(blog_content)

            # Display generated blog
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Your Generated Blog Post</div>', unsafe_allow_html=True)
            
            # Export buttons with icons on the right
            st.markdown('<div class="button-container">', unsafe_allow_html=True)
            col1, col2, col3, _ = st.columns([1, 1, 1, 8])  # Spacer column for right alignment
            with col1:
                if st.button("📋", key="copy_button", help="Copy to Clipboard"):
                    pyperclip.copy(blog_content)
                    st.success("Copied to clipboard!")
            with col2:
                txt_file = io.BytesIO(blog_content.encode())
                st.download_button(
                    label="📄",
                    data=txt_file,
                    file_name=f"blog_{topic[:20]}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    help="Download as .txt"
                )
            with col3:
                md_file = io.BytesIO(blog_content.encode())
                st.download_button(
                    label="📝",
                    data=md_file,
                    file_name=f"blog_{topic[:20]}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                    help="Download as .md"
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # Display stats without background
            st.markdown(f'<div class="stats">**Word Count:** {word_count} | **Estimated Reading Time:** {reading_time} minutes</div>', unsafe_allow_html=True)
            st.markdown(blog_content, unsafe_allow_html=True)

            # Display images
            if images:
                st.markdown('<div class="section-title">Related Images</div>', unsafe_allow_html=True)
                cols = st.columns(3)
                for i, img in enumerate(images):
                    with cols[i % 3]:
                        st.image(img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Save blog to session state
            st.session_state.blogs.append({
                "id": str(uuid.uuid4()),
                "topic": topic,
                "tone": tone,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content": blog_content
            })
        except Exception as e:
            st.error(f"Error generating blog: {str(e)}")

# Display selected blog from history
if "selected_blog" in st.session_state:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Selected Blog Post</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.selected_blog, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Embed code
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Embed This Tool</div>', unsafe_allow_html=True)
st.code(f'<iframe src="{st.get_option("browser.serverAddress")}" width="100%" height="600px"></iframe>', language="html")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
