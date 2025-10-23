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
# Supports text, images, and up to 1 million tokens
model = genai.GenerativeModel('gemini-2.5-flash')

# Also provide a flash lite model for faster responses
text_model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Export model name for use with new genai.Client() API
MODEL_NAME = 'gemini-2.5-flash'
