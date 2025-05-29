#!/usr/bin/env python3
"""
Script to convert a text file with recipe names and YouTube URLs into a well-formatted CSV file.
The text file is expected to have recipe names followed by YouTube URLs.
"""

import re
import csv
import sys

def convert_to_csv(input_file, output_file):
    """
    Convert the input text file to a CSV file with recipe names and YouTube URLs.
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to the output CSV file
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Clean up the content
    # Replace multiple consecutive newlines with just two newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Extract all YouTube URLs from the file to count them
    all_urls = re.findall(r'(https?://youtu\.be/[a-zA-Z0-9_-]+)', content)
    unique_urls = set(all_urls)
    print(f"Total YouTube URLs found: {len(all_urls)}")
    print(f"Unique YouTube URLs found: {len(unique_urls)}")
    
    # Find duplicate URLs
    url_counts = {}
    for url in all_urls:
        url_counts[url] = url_counts.get(url, 0) + 1
    
    duplicates = {url: count for url, count in url_counts.items() if count > 1}
    if duplicates:
        print(f"Found {len(duplicates)} duplicate URLs:")
        for url, count in duplicates.items():
            print(f"  {url}: appears {count} times")
    
    # Find all recipe-URL pairs
    recipes = []
    seen_urls = set()
    
    # Pattern 1: Recipe name followed by URL on next line
    pattern1 = r'([^\n]+)\n+(https?://youtu\.be/[a-zA-Z0-9_-]+)'
    matches1 = re.findall(pattern1, content)
    
    # Pattern 2: Recipe name and URL on same line
    pattern2 = r'([^\n]+)\s+(https?://youtu\.be/[a-zA-Z0-9_-]+)'
    matches2 = re.findall(pattern2, content)
    
    # Process all matches
    all_matches = matches1 + matches2
    for recipe_name, url in all_matches:
        recipe_name = recipe_name.strip()
        url = url.strip()
        
        # Skip empty recipe names or incomplete URLs
        if not recipe_name or url == "https://youtu.be/":
            continue
            
        # Skip duplicate URLs
        if url in seen_urls:
            continue
            
        # Handle special characters in recipe names for CSV
        if '"' in recipe_name:
            recipe_name = recipe_name.replace('"', '""')
            recipe_name = f'"{recipe_name}"'
        
        # Remove any extra quotes from recipe names
        recipe_name = recipe_name.replace("''", "")
        
        recipes.append([recipe_name, url])
        seen_urls.add(url)
    
    # Check for URLs that were found but not matched with a recipe
    unmatched_urls = unique_urls - seen_urls
    if unmatched_urls:
        print(f"Found {len(unmatched_urls)} URLs without matching recipe names:")
        for url in unmatched_urls:
            print(f"  {url}")
    
    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Recipe Name', 'YouTube URL'])
        writer.writerows(recipes)
    
    print(f"Successfully converted {len(recipes)} recipes to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_csv.py input_file.txt output_file.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_to_csv(input_file, output_file)
