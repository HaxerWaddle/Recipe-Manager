function adjustRecipeListingHeight() {
    document.querySelectorAll(".recipe_listing").forEach(listing => {
        const recipeText = listing.querySelector(".Recipe");
        if (recipeText) {
            const textHeight = recipeText.scrollHeight; // Get actual height of the text
            listing.style.height = `calc(${textHeight}px + 5vh)`; // Add some extra space
        }
    });
}

// Run on page load and resize
window.addEventListener("load", adjustRecipeListingHeight);
window.addEventListener("resize", adjustRecipeListingHeight);