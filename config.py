"""
Configuration module for the Image-CSV Chatbot application.
Handles environment variables and API initialization.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.genai import types

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

# System instruction for code execution (defined here to avoid circular import)
SYSTEM_INSTRUCTION = """You are an expert data analyst AI with Python code execution capabilities.

CORE CAPABILITIES:
- Analyze datasets thoroughly and provide clear, actionable insights
- Execute Python code to perform calculations and generate visualizations
- Use matplotlib/seaborn to create plots when requested

IMPORTANT: When users ask for plots, charts, or visualizations, you MUST write and execute Python code to generate the actual image. Do NOT just describe what the plot would look like."""

# Initialize the Gemini model for vision and text
# Supports text, images, up to 1 million tokens, and code execution
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    tools='code_execution',  # Enable code execution for plot generation
    system_instruction=SYSTEM_INSTRUCTION
)

# Also provide a flash lite model for faster responses
text_model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Export model name for use with new genai.Client() API
MODEL_NAME = 'gemini-2.5-flash'

# Export generation config for file upload API (with code execution)
# Note: genai.Client() uses different format than genai.GenerativeModel()
GENERATION_CONFIG_WITH_CODE_EXECUTION = {
    'tools': [types.Tool(code_execution={})],  # Enable code execution
    'system_instruction': SYSTEM_INSTRUCTION
}
