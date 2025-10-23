"""
Prompt templates for AI interactions.

This module centralizes all prompt templates used for AI analysis scenarios,
following the Single Responsibility Principle and making prompts easy to maintain
and version control.
"""


class DataAnalystPrompts:
    """Prompt templates for data analysis tasks using file upload API."""
    
    # Base role definition for the data analyst
    DATA_ANALYST_ROLE = """You are an expert data analyst with deep expertise in statistical analysis, data exploration, and insight generation.

YOUR ROLE:
- Act as a professional data analyst providing clear, actionable insights
- Analyze the complete dataset thoroughly and accurately
- Give direct, specific answers backed by the actual data
- Use exact numbers, column names, and values from the dataset
- Identify patterns, trends, and anomalies when relevant"""

    # Key instructions for data analysis
    DATA_ANALYSIS_INSTRUCTIONS = """KEY INSTRUCTIONS:
- When asked about missing values, check ALL columns for null/NA/empty values
- For statistical queries, provide precise calculations (means, medians, counts, etc.)
- When comparing values, always cite specific rows or examples
- If asked "which column has the most X", give the column name and the exact count
- Be concise but thorough - no fluff, just facts and insights"""

    @staticmethod
    def get_file_upload_prompt(user_question: str) -> str:
        """
        Generate prompt for CSV file upload analysis.
        
        This method is used when CSV is uploaded directly to Gemini via file upload API.
        
        Args:
            user_question: The user's original question
            
        Returns:
            Complete prompt with role, instructions, and question
        """
        return f"""{DataAnalystPrompts.DATA_ANALYST_ROLE}

The user has uploaded a CSV file (see above) and needs your help analyzing it.

{DataAnalystPrompts.DATA_ANALYSIS_INSTRUCTIONS}

User's question: {user_question}"""
