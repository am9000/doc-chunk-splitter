"""
File handlers for different file types.
Each handler splits files into chunks based on line count.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class FileHandler(ABC):
    """Abstract base class for file handlers."""
    
    @abstractmethod
    def can_handle(self, file_path: Path) -> bool:
        """Check if this handler can process the given file."""
        pass
    
    @abstractmethod
    def process(self, file_path: Path, chunk_size: int) -> List[str]:
        """
        Process the file and return chunks.
        
        Args:
            file_path: Path to the file to process
            chunk_size: Number of lines per chunk
            
        Returns:
            List of text chunks
        """
        pass


class MarkdownHandler(FileHandler):
    """Handler for Markdown files (.md extension)."""
    
    def can_handle(self, file_path: Path) -> bool:
        """Check if file has .md extension."""
        return file_path.suffix.lower() == '.md'
    
    def process(self, file_path: Path, chunk_size: int) -> List[str]:
        """
        Split markdown file into chunks based on line count.
        
        Args:
            file_path: Path to the markdown file
            chunk_size: Number of lines per chunk
            
        Returns:
            List of markdown text chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            chunks = []
            for i in range(0, len(lines), chunk_size):
                chunk = ''.join(lines[i:i + chunk_size])
                chunks.append(chunk)
            
            return chunks
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []


class JsonHandler(FileHandler):
    """Handler for JSON files (.json extension)."""
    
    def can_handle(self, file_path: Path) -> bool:
        """Check if file has .json extension."""
        return file_path.suffix.lower() == '.json'
    
    def process(self, file_path: Path, chunk_size: int) -> List[str]:
        """
        Split JSON file into chunks based on line count.
        
        Args:
            file_path: Path to the JSON file
            chunk_size: Number of lines per chunk
            
        Returns:
            List of JSON text chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            chunks = []
            for i in range(0, len(lines), chunk_size):
                chunk = ''.join(lines[i:i + chunk_size])
                chunks.append(chunk)
            
            return chunks
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []


class HandlerRegistry:
    """Registry for managing file handlers."""
    
    def __init__(self):
        self.handlers: List[FileHandler] = []
    
    def register(self, handler: FileHandler):
        """Register a new handler."""
        self.handlers.append(handler)
    
    def get_handler(self, file_path: Path) -> FileHandler | None:
        """Get the appropriate handler for a file."""
        for handler in self.handlers:
            if handler.can_handle(file_path):
                return handler
        return None
