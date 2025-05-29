// Search functionality for recipe site
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  let searchIndex;
  let recipeData;

  // Fetch the search index
  fetch('/search.json')
    .then(response => response.json())
    .then(data => {
      recipeData = data;
      
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
    })
    .catch(error => {
      console.error('Error loading search index:', error);
    });

  // Handle search input
  searchInput.addEventListener('input', function() {
    if (!searchIndex) return;
    
    const query = this.value;
    if (query.length < 2) {
      document.getElementById('search-results').innerHTML = '';
      return;
    }
    
    const results = searchIndex.search(query);
    displayResults(results);
  });
  
  function displayResults(results) {
    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '';
    
    if (results.length === 0) {
      resultsContainer.innerHTML = '<p>No results found</p>';
      return;
    }
    
    results.forEach(result => {
      const recipe = recipeData.find(r => r.url === result.ref);
      if (!recipe) return;
      
      const resultItem = document.createElement('div');
      resultItem.classList.add('search-result');
      
      // Highlight matching ingredients if possible
      let ingredientMatches = '';
      if (recipe.ingredients && recipe.ingredients.length > 0) {
        const matchedIngredients = recipe.ingredients.slice(0, 3).map(ing => ing.name);
        if (matchedIngredients.length > 0) {
          ingredientMatches = `<p>Ingredients: ${matchedIngredients.join(', ')}${recipe.ingredients.length > 3 ? '...' : ''}</p>`;
        }
      }
      
      resultItem.innerHTML = `
        <h3><a href="${recipe.url}">${recipe.title}</a></h3>
        <p>Category: ${recipe.category}</p>
        ${recipe.tags ? `<p>Tags: ${recipe.tags.join(', ')}</p>` : ''}
        ${ingredientMatches}
      `;
      
      resultsContainer.appendChild(resultItem);
    });
  }
});
