"""
Service for detecting user intent in prompts.
"""

import re
from logger_config import get_logger

logger = get_logger(__name__)


class PromptAnalyzer:
    """Analyzes user prompts to determine intent and required features."""
    
    # Keywords that indicate plot/visualization requests
    PLOT_KEYWORDS = [
        'plot', 'chart', 'graph', 'visualize', 'visualization', 'visualise', 'visualisation',
        'bar chart', 'line chart', 'pie chart', 'scatter plot', 'histogram', 'heatmap',
        'box plot', 'boxplot', 'draw', 'show me', 'create a'
    ]
    
    @staticmethod
    def requires_plot(prompt: str) -> bool:
        """
        Determine if the user prompt is requesting a plot/visualization.
        
        Analyzes the prompt for keywords that indicate the user wants
        to see a visual representation of data.
        
        Args:
            prompt: The user's input text
            
        Returns:
            True if prompt appears to request a plot/visualization
        """
        if not prompt:
            return False
        
        # Convert to lowercase for case-insensitive matching
        prompt_lower = prompt.lower()
        
        # Check for plot-related keywords
        for keyword in PromptAnalyzer.PLOT_KEYWORDS:
            if keyword in prompt_lower:
                logger.info(f"Plot request detected - keyword: '{keyword}'")
                return True
        
        # Check for common visualization patterns
        visualization_patterns = [
            r'show.*\b(distribution|trend|comparison|correlation)\b',
            r'compare.*\b(using|with|via)\b',
            r'display.*\b(data|results|analysis)\b.*visually'
        ]
        
        for pattern in visualization_patterns:
            if re.search(pattern, prompt_lower):
                logger.info(f"Plot request detected - pattern match: {pattern}")
                return True
        
        logger.debug("No plot request detected in prompt")
        return False
