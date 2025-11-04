"""
Main application for doc-chunk-splitter.
Processes files recursively from input directory and saves chunks to output directory.
"""

from pathlib import Path
from typing import List
from config import Config
from handlers import HandlerRegistry, MarkdownHandler, JsonHandler


class DocChunkSplitter:
    """Main application class for splitting documents into chunks."""
    
    def __init__(self, config: Config):
        self.config = config
        self.handler_registry = HandlerRegistry()
        
        # Register handlers
        self.handler_registry.register(MarkdownHandler())
        self.handler_registry.register(JsonHandler())
    
    def get_output_filename(self, file_path: Path, chunk_number: int) -> str:
        """
        Generate output filename according to the pattern:
        <source_file_path_recursive_with_dashes>-<file_name>-<chunk_number>.<extension>
        
        Args:
            file_path: Path to the source file (relative to input path)
            chunk_number: Chunk number (1-indexed)
            
        Returns:
            Generated filename
        """
        # Get relative path from input directory
        try:
            relative_path = file_path.relative_to(self.config.input_path)
        except ValueError:
            # If file is not relative to input path, use the file path as is
            relative_path = file_path
        
        # Get parent directory path and replace slashes with dashes
        parent_parts = relative_path.parent.parts
        parent_str = '-'.join(parent_parts) if parent_parts else ''
        
        # Get filename without extension
        file_stem = file_path.stem
        
        # Get extension
        extension = file_path.suffix
        
        # Build output filename
        if parent_str:
            output_name = f"{parent_str}-{file_stem}-{chunk_number}{extension}"
        else:
            output_name = f"{file_stem}-{chunk_number}{extension}"
        
        return output_name
    
    def save_chunks(self, file_path: Path, chunks: List[str]):
        """
        Save chunks to output directory.
        
        Args:
            file_path: Path to the source file
            chunks: List of text chunks to save
        """
        # Create output directory if it doesn't exist
        self.config.output_path.mkdir(parents=True, exist_ok=True)
        
        # Save each chunk
        for i, chunk in enumerate(chunks, start=1):
            output_filename = self.get_output_filename(file_path, i)
            output_path = self.config.output_path / output_filename
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(chunk)
                print(f"  Saved chunk {i}/{len(chunks)}: {output_filename}")
            except Exception as e:
                print(f"  Error saving chunk {i}: {e}")
    
    def process_file(self, file_path: Path):
        """
        Process a single file.
        
        Args:
            file_path: Path to the file to process
        """
        # Check if file is excluded
        if self.config.is_excluded(file_path):
            print(f"Skipping excluded file: {file_path}")
            return
        
        # Get appropriate handler
        handler = self.handler_registry.get_handler(file_path)
        
        if handler is None:
            print(f"Skipping unmatched file: {file_path}")
            return
        
        print(f"Processing: {file_path}")
        
        # Process file and get chunks
        chunks = handler.process(file_path, self.config.chunk_size)
        
        if chunks:
            # Save chunks to output directory
            self.save_chunks(file_path, chunks)
            print(f"  Created {len(chunks)} chunk(s)")
        else:
            print(f"  No chunks created")
    
    def process_directory(self, directory: Path):
        """
        Process all files in a directory recursively.
        
        Args:
            directory: Path to the directory to process
        """
        # Check if directory is excluded
        if self.config.is_excluded(directory):
            print(f"Skipping excluded directory: {directory}")
            return
        
        try:
            # Iterate through all items in directory
            for item in sorted(directory.iterdir()):
                if item.is_file():
                    self.process_file(item)
                elif item.is_dir():
                    self.process_directory(item)
        except PermissionError as e:
            print(f"Permission denied: {directory} - {e}")
        except Exception as e:
            print(f"Error processing directory {directory}: {e}")
    
    def run(self):
        """Run the application."""
        print("=" * 60)
        print("Doc Chunk Splitter")
        print("=" * 60)
        print(f"Input path: {self.config.input_path}")
        print(f"Output path: {self.config.output_path}")
        print(f"Chunk size: {self.config.chunk_size} lines")
        print(f"Excluded folders: {self.config.exclude_folders}")
        print(f"Excluded files: {self.config.exclude_files}")
        print("=" * 60)
        
        # Validate configuration
        if not self.config.validate():
            print("\nConfiguration validation failed. Exiting.")
            return
        
        # Process input directory
        print("\nProcessing files...\n")
        self.process_directory(self.config.input_path)
        
        print("\n" + "=" * 60)
        print("Processing complete!")
        print("=" * 60)


def main():
    """Entry point for the application."""
    config = Config()
    app = DocChunkSplitter(config)
    app.run()


if __name__ == '__main__':
    main()
