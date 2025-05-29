#!/usr/bin/env python3
"""
Script to fetch YouTube video descriptions for KaynSpice recipes
and store them in a JSON data structure.
"""

import os
import csv
import json
import requests
from urllib.parse import urlparse, parse_qs
import argparse

# Import the video text extraction module
try:
    from video_text_extractor import extract_text_from_youtube
    VIDEO_OCR_AVAILABLE = True
except ImportError:
    VIDEO_OCR_AVAILABLE = False
    print("Warning: video_text_extractor module not found. OCR functionality will be disabled.")

# YouTube API key - you'll need to get one from Google Cloud Console
# https://console.cloud.google.com/apis/credentials
API_KEY = "YOUR_API_KEY_HERE"

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    if "youtu.be" in youtube_url:
        # Handle youtu.be URLs
        return youtube_url.split("/")[-1]
    elif "youtube.com" in youtube_url:
        # Handle youtube.com URLs
        parsed_url = urlparse(youtube_url)
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query)["v"][0]
        elif "embed" in parsed_url.path:
            return parsed_url.path.split("/")[-1]
    
    # If we can't extract the ID, return the original URL
    return youtube_url

def get_video_description(video_id):
    """Fetch the video description from YouTube API."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["snippet"]["description"]
        else:
            print(f"No description found for video ID: {video_id}")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching video description for {video_id}: {e}")
        return ""

def process_recipes_csv(csv_path, extract_video_text=False):
    """Process the recipes CSV file and fetch YouTube descriptions."""
    recipes_data = []
    
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
                        video_text_data = extract_text_from_youtube(youtube_url)
                        recipe_data["video_text"] = video_text_data["extracted_text"]
                    except Exception as e:
                        print(f"Error extracting text from video: {e}")
                        recipe_data["video_text"] = []
                
                recipes_data.append(recipe_data)
    
    return recipes_data

def main():
    parser = argparse.ArgumentParser(description='Fetch YouTube video descriptions for KaynSpice recipes.')
    parser.add_argument('--csv', default="_data/kaynspice_recipes.csv", help='Path to the CSV file containing recipes')
    parser.add_argument('--output', default="_data/kaynspice_descriptions.json", help='Path to save the output JSON file')
    parser.add_argument('--extract-video-text', action='store_true', help='Extract text from video frames using OCR')
    args = parser.parse_args()
    
    # Check if OCR is requested but not available
    if args.extract_video_text and not VIDEO_OCR_AVAILABLE:
        print("Error: Video text extraction requested but the required module is not available.")
        print("Please install the necessary dependencies:")
        print("pip install opencv-python pytesseract yt-dlp")
        return
    
    # Process recipes
    recipes_data = process_recipes_csv(args.csv, args.extract_video_text)
    
    # Save to JSON file
    with open(args.output, 'w') as f:
        json.dump(recipes_data, f, indent=2)
    
    print(f"Processed {len(recipes_data)} recipes. Data saved to {args.output}")

if __name__ == "__main__":
    main()
