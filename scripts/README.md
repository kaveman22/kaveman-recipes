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

1. **Get a YouTube API Key**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create an API key
   - Replace `YOUR_API_KEY_HERE` in the script with your actual API key

2. **Install Required Packages**:
   ```bash
   pip install requests
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

1. **Install Required Packages**:
   ```bash
   pip install opencv-python pytesseract yt-dlp
   ```

2. **Install Tesseract OCR**:
   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

3. **Usage as Standalone**:
   ```bash
   # Extract text from a YouTube video
   python scripts/video_text_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"
   
   # Save output to a file
   python scripts/video_text_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --output results.json
   
   # Adjust frame rate (frames per second to extract)
   python scripts/video_text_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" --frame-rate 1
   ```

## Workflow Example

Here's a complete workflow example for processing KaynSpice recipes:

```bash
# 1. Convert a text list to CSV (if needed)
./scripts/convert_to_csv.py recipe_list.txt _data/kaynspice_recipes.csv

# 2. Fetch YouTube descriptions and extract text from videos
python scripts/kaynspice_processor.py --extract-video-text

# 3. Convert recipes to markdown files
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

### YouTube API Issues
- If you get API errors, check your API key and quota limits
- YouTube API has daily quotas that may limit the number of videos you can process

### Permission Issues
- If you get permission errors, ensure scripts are executable: `chmod +x script_name.py`
- For file access issues, check that paths are correct and you have write permissions
