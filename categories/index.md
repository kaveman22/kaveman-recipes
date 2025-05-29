---
layout: default
title: Recipe Categories
permalink: /categories/
---

# Recipe Categories

Browse recipes by category:

{% assign categories = site.recipes | map: "category" | uniq | sort %}
<ul class="category-list">
  {% for category in categories %}
    {% assign category_slug = category | downcase | replace: ' ', '-' %}
    <li><a href="{{ '/categories/' | append: category_slug | relative_url }}">{{ category }}</a></li>
  {% endfor %}
</ul>
