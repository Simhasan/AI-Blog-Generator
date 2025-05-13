AI Blog Post Generator
A Streamlit web application that generates blog posts using Cohere's API and fetches related images from Unsplash. Users can input a blog topic, select a tone, and generate a structured blog post with export options.
Features

Generate blog posts with customizable topics and tones (Professional, Friendly, Persuasive, Witty)
Structured output including a catchy title, introduction, 3-5 sections with subheadings, and a conclusion with a call to action
Fetch related images from Unsplash API
Export options: copy to clipboard, download as .txt or .md
Display word count and estimated reading time
Save generated blogs in session state
Embed code for integrating the tool into customer websites

Prerequisites

Python 3.8+
Cohere API key (sign up at cohere.com)
Unsplash API key (register at unsplash.com/developers)

Project Structure
.
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── .streamlit/
    └── secrets.toml        # API key storage

Setup

Clone the Repository:
git clone <repository-url>
cd ai-blog-generator


Install Dependencies:
pip install -r requirements.txt


Configure API Keys:

Create a .streamlit/secrets.toml file in the project root:COHERE_API_KEY = "your-cohere-api-key"
UNSPLASH_ACCESS_KEY = "your-unsplash-access-key"


Replace placeholders with your actual API keys.



Running Locally

Ensure you're in the project directory:cd C:\path\to\ai-blog-generator


Run the Streamlit app:streamlit run app.py


Open the provided local URL (e.g., http://localhost:8501) in your browser.

Deploying to Streamlit Cloud

Push your code to a GitHub repository.
Sign up/log in to Streamlit Cloud.
Create a new app and link your GitHub repository.
Add the following secrets in Streamlit Cloud's app settings:
COHERE_API_KEY: Your Cohere API key
UNSPLASH_ACCESS_KEY: Your Unsplash API key


Deploy the app and access it via the provided URL.

Usage

Enter a blog topic in the text input field (e.g., "Benefits of Remote Work").
Select a tone from the dropdown (Professional, Friendly, Persuasive, Witty).
Click Generate Blog to create the blog post.
View the generated content, related images, word count, and reading time.
Use export options to copy the content or download it as .txt or .md.
Copy the embed code to integrate the tool into customer websites.
View saved blogs in the Saved Blogs section.

Notes

Cohere API: The app uses Cohere's text generation API with the generate endpoint. Ensure your API key has sufficient credits (Cohere offers a free tier with limits).
Unsplash API: The app fetches images in demo mode (50 requests/hour). Apply for production mode for higher limits.
Session State: Blogs are saved in the session state and persist during the current session.
Error Handling: API errors are displayed in the Streamlit UI for easy debugging.
Token Optimization: The app limits Cohere API requests to 2000 tokens to stay within free tier limits.

Troubleshooting

Streamlit not recognized: Install Streamlit (pip install streamlit) and ensure the Python Scripts directory is in your PATH.
API errors: Verify API keys in secrets.toml and check your Cohere/Unsplash account for quota or permission issues.
Rate limits: If Cohere's free tier limits are exceeded, consider upgrading to a paid plan or optimizing token usage.

Future Enhancements

* Add user authentication for persistent blog storage
* Integrate AI-generated images (e.g., via Stable Diffusion)
* Include SEO optimization suggestions
* Support multiple blog templates for varied layouts


