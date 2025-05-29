// Enhanced search functionality for recipe site with ingredient filtering
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  const ingredientSelect = document.getElementById('ingredient-select');
  const selectedIngredientsContainer = document.getElementById('selected-ingredients');
  const clearFiltersButton = document.getElementById('clear-filters');
  const resultCountElement = document.getElementById('result-count');
  
  if (!searchInput || !ingredientSelect) return;

  let searchIndex;
  let recipeData;
  let allIngredients = new Set();
  let selectedIngredients = new Set();

  // Initialize Select2 for ingredient dropdown
  if (typeof $ !== 'undefined' && $.fn.select2) {
    $(ingredientSelect).select2({
      placeholder: 'Select ingredients...',
      allowClear: true,
      closeOnSelect: false,
      width: '100%'
    });
  }

  // Fetch the search index
  fetch('/search.json')
    .then(response => response.json())
    .then(data => {
      recipeData = data;
      
      // Extract all unique ingredients
      data.forEach(recipe => {
        if (recipe.ingredients && recipe.ingredients.length > 0) {
          recipe.ingredients.forEach(ing => {
            if (ing.name) {
              allIngredients.add(ing.name.toLowerCase());
            }
            // Also add alternatives
            if (ing.alternatives && ing.alternatives.length > 0) {
              ing.alternatives.forEach(alt => {
                if (alt && typeof alt === 'string') {
                  // Extract the main part before any parentheses or commas
                  const mainPart = alt.split('(')[0].split(',')[0].trim().toLowerCase();
                  if (mainPart) allIngredients.add(mainPart);
                }
              });
            }
          });
        }
      });
      
      // Populate ingredient dropdown
      const sortedIngredients = Array.from(allIngredients).sort();
      sortedIngredients.forEach(ingredient => {
        const option = document.createElement('option');
        option.value = ingredient;
        option.textContent = ingredient.charAt(0).toUpperCase() + ingredient.slice(1); // Capitalize first letter
        ingredientSelect.appendChild(option);
      });
      
      // Build the Lunr.js index
      searchIndex = lunr(function() {
        this.field('title', { boost: 10 });
        this.field('category', { boost: 5 });
        this.field('ingredients');
        this.field('tags', { boost: 5 });
        this.field('content');
        this.ref('url');
        
        // Add each recipe to the index
        data.forEach(recipe => {
          // Create a searchable string of all ingredients and alternatives
          let ingredientText = recipe.ingredients.map(ing => {
            return ing.name + ' ' + (ing.alternatives ? ing.alternatives.join(' ') : '');
          }).join(' ');
          
          // Add the recipe with enhanced ingredient data
          this.add({
            title: recipe.title,
            category: recipe.category,
            ingredients: ingredientText,
            tags: recipe.tags ? recipe.tags.join(' ') : '',
            content: recipe.content,
            url: recipe.url
          });
        });
      });
      
      // Show all recipes initially
      updateResults();
    })
    .catch(error => {
      console.error('Error loading search index:', error);
    });

  // Handle search input
  searchInput.addEventListener('input', function() {
    updateResults();
  });
  
  // Handle ingredient selection
  if (typeof $ !== 'undefined') {
    $(ingredientSelect).on('change', function() {
      selectedIngredients = new Set($(this).val() || []);
      updateSelectedIngredientsDisplay();
      updateResults();
    });
  }
  
  // Clear all filters
  if (clearFiltersButton) {
    clearFiltersButton.addEventListener('click', function() {
      searchInput.value = '';
      selectedIngredients.clear();
      if (typeof $ !== 'undefined') {
        $(ingredientSelect).val(null).trigger('change');
      }
      updateSelectedIngredientsDisplay();
      updateResults();
    });
  }
  
  // Update the display of selected ingredients
  function updateSelectedIngredientsDisplay() {
    if (!selectedIngredientsContainer) return;
    
    selectedIngredientsContainer.innerHTML = '';
    
    selectedIngredients.forEach(ingredient => {
      const tag = document.createElement('span');
      tag.classList.add('ingredient-tag');
      tag.textContent = ingredient.charAt(0).toUpperCase() + ingredient.slice(1);
      
      const removeButton = document.createElement('button');
      removeButton.classList.add('remove-ingredient');
      removeButton.innerHTML = '&times;';
      removeButton.addEventListener('click', function() {
        selectedIngredients.delete(ingredient);
        if (typeof $ !== 'undefined') {
          const currentValues = $(ingredientSelect).val() || [];
          const newValues = currentValues.filter(val => val !== ingredient);
          $(ingredientSelect).val(newValues).trigger('change');
        }
        updateSelectedIngredientsDisplay();
        updateResults();
      });
      
      tag.appendChild(removeButton);
      selectedIngredientsContainer.appendChild(tag);
    });
  }
  
  // Filter recipes by selected ingredients
  function filterRecipesByIngredients(recipes) {
    if (selectedIngredients.size === 0) return recipes;
    
    return recipes.filter(recipe => {
      // Check if recipe contains all selected ingredients
      return Array.from(selectedIngredients).every(selectedIngredient => {
        // Check main ingredients
        const hasIngredient = recipe.ingredients.some(ing => {
          if (!ing.name) return false;
          
          // Check if the main ingredient matches
          if (ing.name.toLowerCase().includes(selectedIngredient)) {
            return true;
          }
          
          // Check alternatives
          if (ing.alternatives && ing.alternatives.length > 0) {
            return ing.alternatives.some(alt => {
              if (!alt || typeof alt !== 'string') return false;
              return alt.toLowerCase().includes(selectedIngredient);
            });
          }
          
          return false;
        });
        
        return hasIngredient;
      });
    });
  }
  
  // Update search results based on current filters
  function updateResults() {
    if (!searchIndex || !recipeData) return;
    
    const query = searchInput.value;
    let results = [];
    
    // If search query exists, use Lunr search
    if (query && query.length >= 2) {
      const searchResults = searchIndex.search(query);
      results = searchResults.map(result => {
        return recipeData.find(r => r.url === result.ref);
      }).filter(Boolean);
    } else {
      // Otherwise, use all recipes
      results = [...recipeData];
    }
    
    // Apply ingredient filters
    results = filterRecipesByIngredients(results);
    
    // Update result count
    if (resultCountElement) {
      resultCountElement.textContent = results.length;
    }
    
    // Display results
    displayResults(results);
  }
  
  function displayResults(results) {
    const resultsContainer = document.getElementById('search-results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = '';
    
    if (results.length === 0) {
      resultsContainer.innerHTML = '<p class="no-results">No recipes found matching your criteria</p>';
      return;
    }
    
    results.forEach(recipe => {
      const resultItem = document.createElement('div');
      resultItem.classList.add('recipe-card');
      
      // Get up to 3 main ingredients to display
      let ingredientsList = '';
      if (recipe.ingredients && recipe.ingredients.length > 0) {
        const mainIngredients = recipe.ingredients.slice(0, 3).map(ing => ing.name);
        ingredientsList = `
          <div class="recipe-ingredients-preview">
            <p>${mainIngredients.join(', ')}${recipe.ingredients.length > 3 ? '...' : ''}</p>
          </div>
        `;
      }
      
      // Create tags HTML
      let tagsHtml = '';
      if (recipe.tags && recipe.tags.length > 0) {
        tagsHtml = `
          <div class="tags">
            ${recipe.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
          </div>
        `;
      }
      
      // Add YouTube thumbnail if available
      let thumbnailHtml = '';
      if (recipe.source_url && recipe.source_url.includes('youtu')) {
        // More robust YouTube ID extraction
        let videoId;
        
        try {
          if (recipe.source_url.includes('youtu.be/')) {
            videoId = recipe.source_url.split('youtu.be/')[1];
            if (videoId && videoId.includes('?')) videoId = videoId.split('?')[0];
          } else if (recipe.source_url.includes('youtube.com/watch')) {
            const urlParts = recipe.source_url.split('v=');
            if (urlParts.length > 1) {
              videoId = urlParts[1];
              if (videoId && videoId.includes('&')) videoId = videoId.split('&')[0];
            }
          } else if (recipe.source_url.includes('youtube.com/embed/')) {
            videoId = recipe.source_url.split('youtube.com/embed/')[1];
            if (videoId && videoId.includes('?')) videoId = videoId.split('?')[0];
          } else {
            // Fallback to the last segment of the URL
            videoId = recipe.source_url.split('/').pop();
          }
          
          // Clean up the video ID
          if (videoId) {
            videoId = videoId.trim();
            
            thumbnailHtml = `
              <div class="recipe-thumbnail">
                <a href="${recipe.url}">
                  <img src="https://img.youtube.com/vi/${videoId}/mqdefault.jpg" alt="${recipe.title}">
                </a>
              </div>
            `;
          }
        } catch (e) {
          console.error('Error extracting YouTube ID:', e);
        }
      }
      
      resultItem.innerHTML = `
        ${thumbnailHtml}
        <h3><a href="${recipe.url}">${recipe.title}</a></h3>
        <div class="recipe-meta">
          <span class="category">${recipe.category}</span>
          ${recipe.total_time ? `<span class="time">${recipe.total_time}</span>` : ''}
        </div>
        ${ingredientsList}
        ${tagsHtml}
      `;
      
      resultsContainer.appendChild(resultItem);
    });
  }
});
