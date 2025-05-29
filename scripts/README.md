# Recipe Scripts

This directory contains utility scripts for managing the recipe collection.

## Available Scripts

### `convert_to_csv.py`

Converts a text file with recipe names and YouTube URLs into a CSV file.

Usage:
```
./convert_to_csv.py input_file.txt output_file.csv
```

### `convert_kaynspice_to_md.py`

Converts KaynSpice recipes from the CSV file to individual markdown files.

Usage:
```
./convert_kaynspice_to_md.py
```

This script reads from `_data/kaynspice_recipes.csv` and creates markdown files in the `_recipes/jamaican/` directory.

### `kaynspice_processor.py`

Fetches YouTube video descriptions for KaynSpice recipes and stores them in a JSON data structure.

#### Setup:

1. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Edit `.env` to customize settings if needed
   ```
   cp scripts/.env.example scripts/.env
   nano scripts/.env
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **Usage**:
   ```bash
   # Basic usage (fetch descriptions only)
   python scripts/kaynspice_processor.py
   
   # Custom paths
   python scripts/kaynspice_processor.py --csv path/to/recipes.csv --output path/to/output.json
   
   # With OCR text extraction (see below)
   python scripts/kaynspice_processor.py --extract-video-text
   ```

### `video_text_extractor.py`

Module for extracting text from YouTube videos using OCR. Can be used standalone or with `kaynspice_processor.py`.

#### Setup for OCR:

1. **Environment Variables**:
   - In your `.env` file, you can configure:
   ```
   OCR_FRAME_RATE=0.5
   OCR_TEMP_DIR=temp_video_processing
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

3. **Install Tesseract OCR**:
   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

4. **Usage as Standalone**:
   ```bash
   # Extract text from a YouTube video
   python scripts/video_text_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
   
   # Save output to a file
   python scripts/video_text_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --output results.json
   
   # Adjust frame rate (frames per second to extract)
   python scripts/video_text_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --frame-rate 1
   ```

## Environment Variables

The scripts use the following environment variables from the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OCR_FRAME_RATE` | Number of frames to extract per second | 0.5 |
| `OCR_TEMP_DIR` | Temporary directory for video processing | temp_video_processing |
| `CSV_PATH` | Path to the CSV file with recipes | _data/kaynspice_recipes.csv |
| `OUTPUT_PATH` | Path to save the output JSON file | _data/kaynspice_descriptions.json |

## Workflow Example

Here's a complete workflow example for processing KaynSpice recipes:

```bash
# 1. Set up environment variables
cp scripts/.env.example scripts/.env

# 2. Install dependencies
pip install -r scripts/requirements.txt

# 3. Convert a text list to CSV (if needed)
./scripts/convert_to_csv.py recipe_list.txt _data/kaynspice_recipes.csv

# 4. Fetch YouTube descriptions and extract text from videos
python scripts/kaynspice_processor.py --extract-video-text

# 5. Convert recipes to markdown files
./scripts/convert_kaynspice_to_md.py
```

## Adding New Scripts

When adding new scripts:

1. Place the script in this directory
2. Make it executable with `chmod +x script_name.py`
3. Add documentation to this README file
4. Follow the existing patterns for input/output handling

## Troubleshooting

### OCR Issues
- If OCR results are poor, try adjusting the frame rate to capture more frames
- Ensure Tesseract is properly installed and in your PATH
- For better results with specific videos, you may need to adjust preprocessing in the script

### YouTube Scraping Issues
- If descriptions aren't being extracted correctly, YouTube may have changed their page structure
- Try updating the selectors in the `get_video_description` function
- YouTube may temporarily block requests if too many are made in a short time

### Environment Variables
- If environment variables aren't being recognized, ensure your `.env` file is in the scripts directory
- Check that you've installed the `python-dotenv` package
- You can override any environment variable using command-line arguments
