"""
Configuration management for doc-chunk-splitter.
Loads settings from .env file.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv


class Config:
    """Application configuration loaded from .env file."""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Input and output paths
        self.input_path = Path(os.getenv('INPUT_PATH', 'input-docs'))
        self.output_path = Path(os.getenv('OUTPUT_PATH', 'output-chunks'))
        
        # Chunk size (number of lines)
        self.chunk_size = int(os.getenv('CHUNK_SIZE', '100'))
        
        # Exclusion lists
        exclude_folders = os.getenv('EXCLUDE_FOLDERS', '')
        self.exclude_folders = [f.strip() for f in exclude_folders.split(',') if f.strip()]
        
        exclude_files = os.getenv('EXCLUDE_FILES', '')
        self.exclude_files = [f.strip() for f in exclude_files.split(',') if f.strip()]
    
    def is_excluded(self, path: Path) -> bool:
        """
        Check if a path should be excluded based on configuration.
        
        Args:
            path: Path to check
            
        Returns:
            True if path should be excluded, False otherwise
        """
        # Check if any parent folder is in exclusion list
        for parent in path.parents:
            if parent.name in self.exclude_folders:
                return True
        
        # Check if the path itself is an excluded folder
        if path.is_dir() and path.name in self.exclude_folders:
            return True
        
        # Check if filename is in exclusion list
        if path.name in self.exclude_files:
            return True
        
        return False
    
    def validate(self) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.input_path.exists():
            print(f"Error: Input path '{self.input_path}' does not exist")
            return False
        
        if not self.input_path.is_dir():
            print(f"Error: Input path '{self.input_path}' is not a directory")
            return False
        
        if self.chunk_size <= 0:
            print(f"Error: Chunk size must be positive, got {self.chunk_size}")
            return False
        
        return True
