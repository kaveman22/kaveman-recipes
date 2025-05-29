#!/usr/bin/env python3
"""
Script to convert KaynSpice recipes from CSV to markdown files.
This script reads the kaynspice_recipes.csv file and creates individual
markdown files for each recipe in the _recipes/jamaican directory.
"""

import csv
import os
import re
import datetime

def slugify(text):
    """Convert text to slug format (lowercase, hyphens instead of spaces)."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text

def create_recipe_md(recipe_name, youtube_url):
    """Create a markdown file for a recipe."""
    # Create slug from recipe name
    slug = slugify(recipe_name)
    
    # Set file path
    file_path = f"_recipes/jamaican/{slug}.md"
    
    # Extract YouTube ID from URL
    youtube_id = youtube_url.split('/')[-1]
    
    # Create front matter and template content
    content = f"""---
layout: recipe
title: {recipe_name}
category: Jamaican
date: {datetime.date.today().isoformat()}
source: KaynSpice
source_url: {youtube_url}
ingredients:
  - name: Ingredient 1
    amount: Amount (to be filled)
  - name: Ingredient 2
    amount: Amount (to be filled)
tags: [jamaican]
prep_time: 30 minutes (estimate)
cook_time: 30 minutes (estimate)
total_time: 60 minutes (estimate)
servings: 4
---

# {recipe_name}

## Ingredients

*Note: This recipe was converted from KaynSpice's YouTube channel. Please watch the video for detailed ingredients and instructions.*

- Ingredient 1
- Ingredient 2
- Ingredient 3

## Directions

### Step 1: Preparation
- Watch the full recipe video at [KaynSpice YouTube Channel]({youtube_url})
- Follow along with the video for detailed instructions

---

*This recipe template was automatically generated from KaynSpice's YouTube channel. Please update with actual ingredients and instructions after watching the video.*

*Video link: [{youtube_url}]({youtube_url})*
"""
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    return file_path

def main():
    """Main function to convert CSV to markdown files."""
    csv_path = "_data/kaynspice_recipes.csv"
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return
    
    # Read CSV and create markdown files
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        
        for row in reader:
            if len(row) >= 2:
                recipe_name = row[0]
                youtube_url = row[1]
                
                file_path = create_recipe_md(recipe_name, youtube_url)
                print(f"Created {file_path}")

if __name__ == "__main__":
    main()
