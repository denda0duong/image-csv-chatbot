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

CRITICAL REQUIREMENT FOR DATA QUERIES:
When analyzing CSV data and answering questions about specific values (max, min, top, bottom, counts, averages, filtering, etc.), you MUST:
1. Write and execute Python code using pandas to retrieve the accurate answer
2. VERIFY the result by re-running or using an alternative method to confirm correctness
3. Do NOT estimate or guess - execute code to verify
4. For sorting queries (top N, bottom N), always use df.nsmallest() or df.nlargest() for reliability

IMPORTANT - CODE VISIBILITY:
- For DATA QUERIES: Execute code silently, do NOT show the code in your response. Only present the final answer in natural language.
- For VISUALIZATIONS: Execute code to generate plots, do NOT show the matplotlib code. Only display the resulting image.
- Focus on insights and results, not implementation details.

VERIFICATION IS MANDATORY:
Always verify your answers before presenting them. Never give multiple attempts or corrections - get it right the first time through proper code execution and verification."""

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
