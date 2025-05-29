# My Recipe Collection

This is a GitHub Pages repository for my recipe collection. The site features searchable recipes with ingredient alternatives.

## Structure

- `_data/ingredients.csv`: Master CSV file with ingredients and alternatives
- `_recipes/`: Collection of recipe markdown files organized by category
- `_layouts/`: HTML layouts for the site
- `assets/`: CSS, JavaScript, and images
- `search.json`: Search index for the site
- `search.html`: Search page

## Adding a New Recipe

1. Create a new markdown file in the appropriate category folder under `_recipes/`
2. Use the following front matter template:

```yaml
---
layout: recipe
title: Recipe Name
category: Category
date: YYYY-MM-DD
ingredients:
  - name: Ingredient Name
    amount: Amount
    alternatives:
      - Alternative 1
      - Alternative 2
      - Alternative 3
tags: [tag1, tag2, tag3]
prep_time: X minutes
cook_time: X minutes
total_time: X minutes
servings: X
---
```

3. Add the recipe content below the front matter

## Local Development

To run this site locally:

1. Install Jekyll and Bundler:
   ```
   gem install jekyll bundler
   ```

2. Install dependencies:
   ```
   bundle install
   ```

3. Run the development server:
   ```
   bundle exec jekyll serve
   ```

4. Visit `http://localhost:4000` in your browser

## Deployment

This site is automatically deployed to GitHub Pages when changes are pushed to the main branch.
