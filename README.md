# doc-chunk-splitter

A Python application that splits document files into smaller chunks based on line count. The application processes files recursively from an input directory and saves the chunks to an output directory.

## Features

- **Multiple File Handlers**: Support for Markdown (.md) and JSON (.json) files
- **Configurable Chunk Size**: Split files based on a configurable number of lines
- **Recursive Processing**: Processes all files in subdirectories
- **Exclusion Lists**: Configure folders and files to skip during processing
- **Structured Output**: Chunks are saved with descriptive names that reflect the source file path

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The application uses a `.env` file for configuration. Edit the `.env` file to customize settings:

```env
# Input and output directories
INPUT_PATH=input-docs
OUTPUT_PATH=output-chunks

# Number of lines per chunk
CHUNK_SIZE=100

# Exclusion lists (comma-separated)
EXCLUDE_FOLDERS=.git,.vscode,__pycache__
EXCLUDE_FILES=.gitignore,.DS_Store
```

### Configuration Options

- `INPUT_PATH`: Directory containing the documents to process
- `OUTPUT_PATH`: Directory where chunks will be saved
- `CHUNK_SIZE`: Number of lines per chunk (default: 100)
- `EXCLUDE_FOLDERS`: Comma-separated list of folder names to exclude
- `EXCLUDE_FILES`: Comma-separated list of file names to exclude

## Usage

Run the application:

```bash
python main.py
```

The application will:
1. Read all files recursively from the input directory
2. Process each file with the appropriate handler (Markdown or JSON)
3. Split files into chunks based on the configured line count
4. Save chunks to the output directory with descriptive names

## Output File Naming

Chunks are saved with the following naming pattern:
```
<source_file_path_with_dashes>-<file_name>-<chunk_number>.<extension>
```

**Example:**
- Source file: `input-docs/auth/sessions.md`
- Output chunks:
  - `auth-sessions-1.md`
  - `auth-sessions-2.md`
  - `auth-sessions-3.md`

## Supported File Types

- **Markdown** (`.md`): Handled by `MarkdownHandler`
- **JSON** (`.json`): Handled by `JsonHandler`
- Files with other extensions are skipped

## Project Structure

```
doc-chunk-splitter/
├── main.py              # Main application entry point
├── config.py            # Configuration management
├── handlers.py          # File handlers for different types
├── requirements.txt     # Python dependencies
├── .env                 # Configuration file
├── input-docs/          # Input directory (configurable)
└── output-chunks/       # Output directory (configurable)
```

## Adding New File Handlers

To add support for new file types:

1. Create a new handler class in `handlers.py` that extends `FileHandler`
2. Implement the `can_handle()` and `process()` methods
3. Register the handler in `main.py` in the `DocChunkSplitter.__init__()` method

Example:
```python
class XmlHandler(FileHandler):
    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == '.xml'
    
    def process(self, file_path: Path, chunk_size: int) -> List[str]:
        # Implementation here
        pass
```