"""
Service for extracting and handling plots from Gemini responses.
"""

from typing import List
from ..models.plot import PlotData
from ..models.constants import AppConfig
from logger_config import get_logger

logger = get_logger(__name__)


class PlotService:
    """Handles extraction and validation of plots from AI responses."""
    
    @staticmethod
    def extract_plots_from_response(response) -> List[PlotData]:
        """
        Extract plot images from a Gemini API response.
        
        When Gemini executes code that generates plots, the response
        contains parts with image data that need to be extracted.
        
        Args:
            response: Gemini API response object
            
        Returns:
            List of PlotData objects containing plot images
        """
        plots = []
        
        try:
            # Check if response has candidates
            if not hasattr(response, 'candidates') or not response.candidates:
                logger.debug("No candidates in response")
                return plots
            
            # Get the first candidate's content
            candidate = response.candidates[0]
            if not hasattr(candidate, 'content') or not candidate.content:
                logger.debug("No content in candidate")
                return plots
            
            # Iterate through all parts in the response
            for part in candidate.content.parts:
                # Check for inline_data (images)
                if hasattr(part, 'inline_data') and part.inline_data:
                    mime_type = part.inline_data.mime_type
                    
                    # Only process image types
                    if mime_type in AppConfig.PLOT_MIME_TYPES:
                        plot = PlotData(
                            image_data=part.inline_data.data,
                            mime_type=mime_type
                        )
                        
                        if plot.is_valid():
                            plots.append(plot)
                            logger.info(f"Extracted plot image: {mime_type}")
                        else:
                            logger.warning(f"Invalid plot data: {mime_type}")
            
            if plots:
                logger.info(f"Successfully extracted {len(plots)} plot(s) from response")
            else:
                logger.debug("No plots found in response")
                
        except Exception as e:
            logger.error(f"Error extracting plots from response: {e}", exc_info=True)
        
        return plots
    
    @staticmethod
    def has_executable_code(response) -> bool:
        """
        Check if response contains executable code.
        
        This indicates that Gemini generated code to create visualizations.
        
        Args:
            response: Gemini API response object
            
        Returns:
            True if response contains executable code
        """
        try:
            if not hasattr(response, 'candidates') or not response.candidates:
                return False
            
            candidate = response.candidates[0]
            if not hasattr(candidate, 'content') or not candidate.content:
                return False
            
            for part in candidate.content.parts:
                if hasattr(part, 'executable_code') and part.executable_code:
                    logger.debug("Response contains executable code")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking for executable code: {e}")
            return False
