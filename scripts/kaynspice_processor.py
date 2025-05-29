#!/usr/bin/env python3
"""
Script to fetch YouTube video descriptions for KaynSpice recipes
and store them in a JSON data structure.
"""

import os
import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print("Warning: .env file not found. Using default values or command line arguments.")

# Import the video text extraction module
try:
    from video_text_extractor import extract_text_from_youtube
    VIDEO_OCR_AVAILABLE = True
except ImportError:
    VIDEO_OCR_AVAILABLE = False
    print("Warning: video_text_extractor module not found. OCR functionality will be disabled.")

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    if "youtu.be" in youtube_url:
        # Handle youtu.be URLs
        return youtube_url.split("/")[-1].split("?")[0]
    elif "youtube.com" in youtube_url:
        # Handle youtube.com URLs
        parsed_url = urlparse(youtube_url)
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query)["v"][0]
        elif "embed" in parsed_url.path:
            return parsed_url.path.split("/")[-1].split("?")[0]
    
    # If we can't extract the ID, return the original URL
    return youtube_url

def get_video_description(video_id):
    """Fetch the video description by scraping the YouTube page."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the description in the page
        # First try the meta description
        description_meta = soup.find('meta', {'name': 'description'})
        if description_meta and 'content' in description_meta.attrs:
            return description_meta['content']
        
        # Alternative method - look for specific elements that might contain the description
        # These selectors might need adjustment as YouTube's structure changes
        selectors = [
            'span#description-text',
            'div#description-text',
            'div#description',
            'div.description',
            '[itemprop="description"]'
        ]
        
        for selector in selectors:
            description_element = soup.select_one(selector)
            if description_element:
                return description_element.text.strip()
        
        print(f"No description found for video ID: {video_id}")
        return ""
    except Exception as e:
        print(f"Error fetching video description for {video_id}: {e}")
        return ""

def process_recipes_csv(csv_path, extract_video_text=False, frame_rate=None):
    """Process the recipes CSV file and fetch YouTube descriptions."""
    recipes_data = []
    
    # Get frame rate from environment variable if not provided
    if frame_rate is None:
        frame_rate = float(os.getenv('OCR_FRAME_RATE', 0.5))
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        
        for row in reader:
            if len(row) >= 2:
                recipe_name = row[0]
                youtube_url = row[1]
                
                print(f"Processing: {recipe_name}")
                
                # Extract video ID from URL
                video_id = extract_video_id(youtube_url)
                
                # Get video description
                description = get_video_description(video_id)
                
                # Create recipe data structure
                recipe_data = {
                    "recipe_name": recipe_name,
                    "youtube_link": youtube_url,
                    "youtube_description": description
                }
                
                # Extract text from video frames if requested
                if extract_video_text and VIDEO_OCR_AVAILABLE:
                    print(f"Extracting text from video frames for: {recipe_name}")
                    try:
                        video_text_data = extract_text_from_youtube(youtube_url, frame_rate=frame_rate)
                        recipe_data["video_text"] = video_text_data["extracted_text"]
                    except Exception as e:
                        print(f"Error extracting text from video: {e}")
                        recipe_data["video_text"] = []
                
                recipes_data.append(recipe_data)
    
    return recipes_data

def main():
    parser = argparse.ArgumentParser(description='Fetch YouTube video descriptions for KaynSpice recipes.')
    parser.add_argument('--csv', default=os.getenv('CSV_PATH', "_data/kaynspice_recipes.csv"), 
                        help='Path to the CSV file containing recipes')
    parser.add_argument('--output', default=os.getenv('OUTPUT_PATH', "_data/kaynspice_descriptions.json"), 
                        help='Path to save the output JSON file')
    parser.add_argument('--extract-video-text', action='store_true', 
                        help='Extract text from video frames using OCR')
    parser.add_argument('--frame-rate', type=float, 
                        default=float(os.getenv('OCR_FRAME_RATE', 0.5)), 
                        help='Number of frames to extract per second for OCR')
    args = parser.parse_args()
    
    # Check if OCR is requested but not available
    if args.extract_video_text and not VIDEO_OCR_AVAILABLE:
        print("Error: Video text extraction requested but the required module is not available.")
        print("Please install the necessary dependencies:")
        print("pip install opencv-python pytesseract yt-dlp python-dotenv beautifulsoup4")
        return
    
    # Process recipes
    recipes_data = process_recipes_csv(args.csv, args.extract_video_text, args.frame_rate)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    
    # Save to JSON file
    with open(args.output, 'w') as f:
        json.dump(recipes_data, f, indent=2)
    
    print(f"Processed {len(recipes_data)} recipes. Data saved to {args.output}")

if __name__ == "__main__":
    main()
