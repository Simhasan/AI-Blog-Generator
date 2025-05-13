import streamlit as st
import requests
import pyperclip
import markdown
import io
from datetime import datetime
import uuid
import re

# Initialize Cohere API client
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
UNSPLASH_ACCESS_KEY = st.secrets["UNSPLASH_ACCESS_KEY"]
COHERE_API_URL = "https://api.cohere.ai/v1/generate"

# Blog generation function using Cohere API
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

# Image search function using Unsplash
def get_images(topic, count=3):
    url = f"https://api.unsplash.com/search/photos?query={topic}&per_page={count}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return [photo['urls']['regular'] for photo in response.json()['results']]
    return []

# Word count and reading time
def calculate_stats(text):
    words = len(text.split())
    reading_time = round(words / 200)  # Average reading speed: 200 words/min
    return words, reading_time

# Main Streamlit app
st.set_page_config(page_title="Blog Generator", layout="wide")

st.title("AI Blog Post Generator")
st.markdown("Create engaging blog posts with AI in just a few clicks!")

# Input section
with st.form("blog_form"):
    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Blog Topic", placeholder="Enter your blog topic...")
    with col2:
        tone = st.selectbox("Tone of Writing", ["Professional", "Friendly", "Persuasive", "Witty"])
    submitted = st.form_submit_button("Generate Blog")

# Output section
if submitted and topic:
    with st.spinner("Generating your blog post..."):
        try:
            # Generate blog content
            blog_content = generate_blog(topic, tone)
            
            # Get related images
            images = get_images(topic)
            
            # Calculate stats
            word_count, reading_time = calculate_stats(blog_content)
            
            # Display blog
            st.markdown("## Generated Blog Post")
            st.markdown(f"**Word Count:** {word_count} | **Estimated Reading Time:** {reading_time} minutes")
            
            # Display blog content
            st.markdown(blog_content)
            
            # Display images
            if images:
                st.markdown("### Related Images")
                cols = st.columns(3)
                for i, img in enumerate(images):
                    with cols[i % 3]:
                        st.image(img, use_column_width=True)
            
            # Export options
            st.markdown("### Export Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Copy to Clipboard"):
                    pyperclip.copy(blog_content)
                    st.success("Copied to clipboard!")
            
            with col2:
                txt_file = io.BytesIO(blog_content.encode())
                st.download_button(
                    label="Download as .txt",
                    data=txt_file,
                    file_name=f"blog_{topic[:20]}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            with col3:
                md_file = io.BytesIO(blog_content.encode())
                st.download_button(
                    label="Download as .md",
                    data=md_file,
                    file_name=f"blog_{topic[:20]}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
        except Exception as e:
            st.error(f"Error generating blog: {str(e)}")

# Embed code for customer websites
st.markdown("### Embed This Tool")
st.code(f'<iframe src="{st.get_option("browser.serverAddress")}" width="100%" height="600px"></iframe>', language="html")

# Additional feature: Save blog to session
if "blogs" not in st.session_state:
    st.session_state.blogs = []
if submitted and topic:
    st.session_state.blogs.append({
        "id": str(uuid.uuid4()),
        "topic": topic,
        "tone": tone,
        "content": blog_content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Display saved blogs
if st.session_state.blogs:
    st.markdown("### Saved Blogs")
    for blog in st.session_state.blogs:
        with st.expander(f"{blog['topic']} ({blog['timestamp']})"):
            st.markdown(blog['content'])