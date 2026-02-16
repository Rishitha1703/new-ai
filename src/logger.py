"""
Logger: Centralized logging system
"""

import os
import logging
from datetime import datetime

class AgentLogger:
    """Centralized logging for Concert AI Agent"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        log_config = self.config.get('logging', {})
        
        self.enabled = log_config.get('enabled', True)
        self.log_level = log_config.get('level', 'INFO')
        self.log_file = log_config.get('file', 'logs/concert-agent.log')
        self.console_output = log_config.get('console', True)
        
        if self.enabled:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging configuration"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        self.logger = logging.getLogger('ConcertAgent')
        self.logger.setLevel(getattr(logging, self.log_level))
        self.logger.handlers = []
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(getattr(logging, self.log_level))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        if self.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, self.log_level))
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        if self.enabled:
            self.logger.info(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        if self.enabled:
            self.logger.debug(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        if self.enabled:
            self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        if self.enabled:
            self.logger.error(message, extra=kwargs)
    
    def log_playbook_generation(self, intent: str, source: str, playbook_path: str, validation_status: bool):
        """Log playbook generation event"""
        self.info(
            f"Playbook generated: {playbook_path}",
            extra={'intent': intent, 'source': source, 'validated': validation_status}
        )
    
    def get_recent_logs(self, lines: int = 50) -> list:
        """Get recent log entries"""
        if not self.enabled or not os.path.exists(self.log_file):
            return []
        
        try:
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except Exception:
            return []