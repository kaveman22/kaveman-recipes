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

### 3. Front Matter Structure
```yaml
---
layout: recipe
title: [Recipe Name]
category: [Category]
date: [Current Date]
source: KaynSpice
source_url: [YouTube URL]
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

### 5. Category Management
- If recipe belongs to a new category:
  1. Create category page in `/categories/`
  2. Add category to navigation if needed
  3. Update CSS for any category-specific styling

### 6. Git Workflow
```bash
# Stage the new files
git add _recipes/[category]/[recipe-name].md

# If new category was created
git add categories/[category].md

# Commit changes
git commit -m "Add [recipe name] recipe"

# Push to repository
git push
```

## Example Recipe Addition

Here's an example of adding the "Sticky Mango Jerk Chicken Wings" recipe:

1. Create file: `_recipes/jamaican/sticky-mango-jerk-chicken-wings.md`
2. Add front matter with recipe details
3. Structure content with ingredients and steps
4. Add to git and push changes

## Tips

- Always watch the video completely before starting
- Note any special techniques or tips mentioned
- Include any alternative ingredients mentioned
- Add relevant tags for searchability
- Test the recipe page locally before pushing
- Make sure images (if any) are optimized
- Keep formatting consistent across recipes

## Quality Checklist

- [ ] Front matter complete and valid
- [ ] All ingredients listed with amounts
- [ ] Clear, step-by-step instructions
- [ ] Proper categorization
- [ ] Relevant tags added
- [ ] Source URL correct
- [ ] Local build successful
- [ ] Preview looks correct
- [ ] Changes committed and pushed

## Automation Tools

The `scripts/` directory contains helpful tools:

- `convert_kaynspice_to_md.py`: Converts CSV entries to markdown templates
- Additional scripts can be added to automate parts of this workflow

## Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Markdown Guide](https://www.markdownguide.org/)
- [KaynSpice YouTube Channel](https://www.youtube.com/@KaynSpice)
