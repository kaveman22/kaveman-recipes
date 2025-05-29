# Recipe Creation Workflow

This document outlines the process for adding new recipes to the collection from the KaynSpice YouTube channel.

## Workflow Steps

### 1. Recipe Selection
- Identify the next recipe from `_data/kaynspice_recipes.csv`
- Watch the corresponding YouTube video to gather recipe details
- Note down ingredients, quantities, and instructions

### 2. File Creation
- Create a new markdown file in the appropriate category folder
- Use kebab-case for the filename (e.g., `sticky-mango-jerk-chicken-wings.md`)
- Place file in `_recipes/[category]/` directory
- **Important**: Category folder names should be kebab-case (hyphenated) for multi-word categories (e.g., `middle-eastern`)

### 3. Front Matter Structure
```yaml
---
layout: recipe
title: [Recipe Name]
category: [Category]  # Use proper capitalization, spaces are fine here
date: [Current Date]
source: KaynSpice
source_url: [YouTube URL]  # Must be the full YouTube URL for video embedding
ingredients:
  - name: [Ingredient Name]
    amount: [Amount]
    alternatives:
      - [Alternative 1]
      - [Alternative 2]
tags: [tag1, tag2, tag3]
prep_time: [Time]
cook_time: [Time]
total_time: [Time]
servings: [Number]
---
```

### 4. Content Structure
```markdown
# [Recipe Name]

## Ingredients

### [Section Name] (if applicable)
- List ingredients with amounts

## Directions

### Step 1: [Step Name]
- Detailed instructions
- Additional notes

### Step 2: [Step Name]
- Detailed instructions
- Additional notes
```

### 5. YouTube Video Embedding
- Ensure the `source_url` in the front matter contains the full YouTube URL
- The template will automatically extract the YouTube video ID and create an embedded player
- The video will appear at the top of the recipe page, below the title
- Format should be: `https://youtu.be/VIDEO_ID` or `https://www.youtube.com/watch?v=VIDEO_ID`

### 6. Category Management
- If recipe belongs to a new category:
  1. Create category folder in `_recipes/` using kebab-case (e.g., `middle-eastern`)
  2. Create category page in `/categories/` with the same kebab-case name
  3. Set the permalink in the category page to match the kebab-case format:
     ```yaml
     permalink: /categories/middle-eastern/
     ```
  4. Update CSS for any category-specific styling

### 7. URL Handling
- **Critical**: For multi-word categories, always use kebab-case (hyphens) in:
  - Directory names
  - File names
  - Permalinks
  - URL references
- Example: "Middle Eastern" category should be referenced as `middle-eastern` in URLs and file paths

### 8. Git Workflow
```bash
# Stage the new files
git add _recipes/[category]/[recipe-name].md

# If new category was created
git add categories/[category-slug].md

# Commit changes
git commit -m "Add [recipe name] recipe"

# Push to repository
git push
```

## Example Recipe Addition

Here's an example of adding the "Sticky Mango Jerk Chicken Wings" recipe:

1. Create file: `_recipes/jamaican/sticky-mango-jerk-chicken-wings.md`
2. Add front matter with recipe details including YouTube URL
3. Structure content with ingredients and steps
4. Add to git and push changes

For a multi-word category like "Middle Eastern":
1. Create directory: `_recipes/middle-eastern/`
2. Create file: `_recipes/middle-eastern/spicy-roasted-garlic-chicken-shawarma.md`
3. Create category page: `categories/middle-eastern.md` with permalink `/categories/middle-eastern/`

## Tips

- Always watch the video completely before starting
- Note any special techniques or tips mentioned
- Include any alternative ingredients mentioned
- Add relevant tags for searchability
- Test the recipe page locally before pushing
- Make sure images (if any) are optimized
- Keep formatting consistent across recipes
- **Always use kebab-case for URLs and file paths**
- Ensure YouTube URLs are correctly formatted for proper video embedding

## Quality Checklist

- [ ] Front matter complete and valid
- [ ] YouTube URL correctly formatted in source_url
- [ ] All ingredients listed with amounts
- [ ] Clear, step-by-step instructions
- [ ] Proper categorization
- [ ] Relevant tags added
- [ ] Source URL correct
- [ ] Category slug properly formatted (kebab-case)
- [ ] Local build successful
- [ ] Preview looks correct
- [ ] Video embeds and plays correctly
- [ ] Changes committed and pushed

## Automation Tools

The `scripts/` directory contains helpful tools:

- `convert_kaynspice_to_md.py`: Converts CSV entries to markdown templates
- Additional scripts can be added to automate parts of this workflow

## Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Markdown Guide](https://www.markdownguide.org/)
- [KaynSpice YouTube Channel](https://www.youtube.com/@KaynSpice)
- [YouTube Embed Parameters](https://developers.google.com/youtube/player_parameters)
