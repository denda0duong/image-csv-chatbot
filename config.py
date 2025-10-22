"""
Configuration module for the Image-CSV Chatbot application.
Handles environment variables and API initialization.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. "
        "Please create a .env file with your API key."
    )

# Configure the Google Generative AI with the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model for vision and text
# Using gemini-2.5-pro for multimodal capabilities (text + images)
model = genai.GenerativeModel('gemini-2.5-pro')

# Also provide a text-only model for CSV/text queries
text_model = genai.GenerativeModel('gemini-2.5-flash')
