# PDF Extractor

A Python script that extracts structured content from PDF files, including text blocks and tables, and outputs the data in JSON format.

## Features

- **Text Block Extraction**: Extracts text content with automatic section detection
- **Table Extraction**: Uses Camelot for robust table detection and extraction
- **Multi-Library Approach**: Combines PyMuPDF and Camelot for comprehensive content extraction
- **JSON Output**: Structured output format for easy data processing

## Installation

### Prerequisites

- Python 3.7 or higher
- Required system dependencies for Camelot (see below)

### Install Python Dependencies

```bash
pip install PyMuPDF pdfplumber camelot-py[cv] pandas
```

### System Dependencies

#### Windows
```bash
# Install Ghostscript
# Download from: https://www.ghostscript.com/download/gsdnld.html

# Install via conda (recommended)
conda install -c conda-forge camelot-py
```

#### macOS
```bash
brew install ghostscript
pip install camelot-py[cv]
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ghostscript
sudo apt-get install python3-tk
pip install camelot-py[cv]
```

### Alternative Installation (if Camelot fails)

If you encounter issues with Camelot installation:

```bash
# Install without cv dependencies
pip install PyMuPDF pdfplumber
pip install camelot-py

# Or use tabula as alternative
pip install tabula-py
```

## Usage

### Command Line

#### Basic Usage
```bash
python pdf_extractor.py input.pdf
```

#### Specify Output File
```bash
python pdf_extractor.py input.pdf output.json
```

#### Examples
```bash
# Process a financial document
python pdf_extractor.py "360ONE-MF-May 2025.pdf" fund_data.json

# Use default output filename
python pdf_extractor.py document.pdf
```

### Python Script Usage

```python
from pdf_extractor import parse_pdf

# Extract content from PDF
result = parse_pdf("document.pdf", "output.json")
print("Extraction completed!")
```

## Output Format

The script generates JSON with the following structure:

```json
{
  "pages": [
    {
      "page_number": 1,
      "content": [
        {
          "type": "paragraph",
          "section": "SECTION NAME",
          "sub_section": null,
          "text": "Extracted text content..."
        },
        {
          "type": "table",
          "section": null,
          "description": null,
          "table_data": [
            ["Column 1", "Column 2", "Column 3"],
            ["Row 1 Data", "Row 1 Data", "Row 1 Data"],
            ["Row 2 Data", "Row 2 Data", "Row 2 Data"]
          ]
        }
      ]
    }
  ]
}
```

## How It Works

### Text Extraction Process

1. **PyMuPDF Processing**: Uses `fitz` to extract text blocks from each page
2. **Section Detection**: Identifies uppercase text as potential section headers
3. **Content Classification**: Categorizes content as sections or regular text

### Table Extraction Process

1. **Camelot Processing**: Uses lattice-based table detection
2. **Data Conversion**: Converts pandas DataFrames to nested lists
3. **Page Mapping**: Associates tables with their respective pages

### Section Detection Logic

- Text blocks that are ALL UPPERCASE and contain fewer than 8 words are classified as sections
- Other text blocks are treated as regular paragraph content
- Tables are extracted separately and merged with text content by page

## Troubleshooting

### Common Issues

1. **Camelot Installation Error**
   ```
   ERROR: Failed building wheel for camelot-py
   ```
   **Solution**: Install system dependencies first (Ghostscript, Tkinter)
   ```bash
   # Windows: Download and install Ghostscript manually
   # macOS: brew install ghostscript
   # Linux: sudo apt-get install ghostscript python3-tk
   ```

2. **No Tables Detected**
   ```
   Table extraction error: No tables found
   ```
   **Solutions**:
   - Try different Camelot flavors: `flavor="stream"` instead of `flavor="lattice"`
   - Check if PDF contains actual table structures (not just formatted text)
   - Use pdfplumber as fallback for simple tables

3. **Empty or Garbled Text**
   ```
   Text appears corrupted or missing
   ```
   **Solutions**:
   - Ensure PDF is text-based, not scanned images
   - For scanned PDFs, use OCR preprocessing
   - Check if PDF has copy restrictions

4. **Memory Issues with Large Files**
   ```
   MemoryError or process hangs
   ```
   **Solutions**:
   - Process pages in batches
   - Use page ranges: `pages="1-10"`
   - Increase system memory or use a more powerful machine

### Performance Tips

- **Large PDFs**: Process specific page ranges using `pages="1-5"` parameter
- **Complex Tables**: Lattice flavor works better for bordered tables
- **Simple Tables**: Stream flavor works better for tables without clear borders
- **Memory Usage**: Close the PDF document object when done to free memory

## Limitations

- **Scanned PDFs**: Does not include OCR capabilities
- **Complex Layouts**: Multi-column layouts may not preserve reading order
- **Image Content**: Cannot extract text from images or charts
- **Table Detection**: May miss tables without clear borders or structure
- **Section Logic**: Simple uppercase detection may misclassify some content

## Dependencies

### Required Libraries
- `PyMuPDF (fitz)`: PDF text extraction
- `camelot-py[cv]`: Advanced table extraction
- `pandas`: Data manipulation for tables
- `pdfplumber`: Alternative PDF processing (imported but not actively used)

### System Requirements
- **Ghostscript**: Required for Camelot table extraction
- **Tkinter**: Required for Camelot on some systems
- **OpenCV**: Automatically installed with camelot-py[cv]

## File Structure

```
pdf_extractor.py          # Main extraction script
output.json              # Default output file (generated)
README.md               # This documentation
```

## Error Handling

The script includes basic error handling for:
- Missing input files
- Table extraction failures
- JSON writing errors
- Command line argument validation

Errors are printed to console but don't stop execution of other extraction processes.

## Contributing

To improve this script:
1. Add OCR support for scanned PDFs
2. Implement better section detection algorithms
3. Add support for chart/image extraction
4. Include configuration options for different PDF types
5. Add batch processing capabilities

## License

This script is provided as-is for educational and development purposes.
