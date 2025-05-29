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
    <li><a href="{{ '/categories/' | append: category | downcase | relative_url }}">{{ category }}</a></li>
  {% endfor %}
</ul>
