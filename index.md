---
layout: default
title: Home
---

# My Recipe Collection

Welcome to my recipe collection! Here you'll find a variety of recipes with detailed instructions and ingredient alternatives.

## Browse by Category

{% assign categories = site.recipes | map: "category" | uniq | sort %}
<ul class="category-list">
  {% for category in categories %}
    {% assign category_slug = category | downcase | replace: ' ', '-' %}
    <li><a href="{{ '/categories/' | append: category_slug | relative_url }}">{{ category }}</a></li>
  {% endfor %}
</ul>

## Recent Recipes

<div class="recipe-grid">
  {% assign recipes = site.recipes | sort: "date" | reverse %}
  {% for recipe in recipes limit:6 %}
    <div class="recipe-card">
      <h3><a href="{{ recipe.url | relative_url }}">{{ recipe.title }}</a></h3>
      <div class="recipe-meta">
        <span class="category">{{ recipe.category }}</span>
        <span class="time">{{ recipe.total_time }}</span>
      </div>
      <div class="tags">
        {% for tag in recipe.tags %}
          <span class="tag">{{ tag }}</span>
        {% endfor %}
      </div>
    </div>
  {% endfor %}
</div>

## Search Recipes

Looking for something specific? Try our [search page](/search/) to find recipes by ingredient, category, or keyword.
