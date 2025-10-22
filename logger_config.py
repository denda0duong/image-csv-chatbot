"""
Logging configuration for the chatbot application.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class LoggerConfig:
    """Centralized logging configuration."""
    
    # Log directory
    LOG_DIR = Path("logs")
    
    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    # Log format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    @staticmethod
    def setup_logging(log_level: int = logging.INFO) -> None:
        """
        Set up logging configuration for the application.
        
        Args:
            log_level: The minimum logging level to capture
        """
        # Create logs directory if it doesn't exist
        LoggerConfig.LOG_DIR.mkdir(exist_ok=True)
        
        # Generate log filename with date
        log_filename = f"chatbot_{datetime.now().strftime('%Y%m%d')}.log"
        log_filepath = LoggerConfig.LOG_DIR / log_filename
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format=LoggerConfig.LOG_FORMAT,
            datefmt=LoggerConfig.DATE_FORMAT,
            handlers=[
                # File handler - logs everything
                logging.FileHandler(log_filepath, encoding='utf-8'),
                # Console handler - only warnings and above
                logging.StreamHandler()
            ]
        )
        
        # Set console handler to WARNING level
        console_handler = logging.getLogger().handlers[1]
        console_handler.setLevel(logging.WARNING)
        
        # Log startup
        logger = logging.getLogger(__name__)
        logger.info("=" * 60)
        logger.info("Chatbot application started")
        logger.info(f"Log file: {log_filepath}")
        logger.info("=" * 60)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger instance for a specific module.
        
        Args:
            name: Name of the module/logger
            
        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.
    
    Args:
        name: Name of the module requesting the logger
        
    Returns:
        Logger instance
    """
    return LoggerConfig.get_logger(name)
