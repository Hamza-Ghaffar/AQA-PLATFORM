"""
Logger utility for consistent logging across tests.
Provides structured logging with automatic context capture.
"""

import logging
from typing import Optional

class TestLogger:
    """
    Wrapper around Python's logging module for test automation.
    Provides consistent formatting and context capture.
    """
    
    def __init__(self, name: str):
        """
        Initialize logger for a test module.
        
        Args:
            name: Logger name (typically __name__)
        """
        self.logger = logging.getLogger(name)
    
    def info(self, message: str, **kwargs):
        """Log info level message"""
        self.logger.info(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug level message"""
        self.logger.debug(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error level message"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical level message"""
        self.logger.critical(message, **kwargs)
    
    def step(self, action: str, description: str = ""):
        """
        Log test step with consistent formatting.
        
        Args:
            action: The action being performed (e.g., "NAVIGATE", "LOGIN", "VERIFY")
            description: Detailed description of what's happening
        """
        self.logger.info(f"[STEP] {action}: {description}")
    
    def result(self, status: str, message: str):
        """
        Log test result.
        
        Args:
            status: "PASS", "FAIL", "SKIP"
            message: Result details
        """
        self.logger.info(f"[{status}] {message}")
