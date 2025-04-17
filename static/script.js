document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('search-btn');
    const destinationInput = document.getElementById('destination');
    const preferencesInput = document.getElementById('preferences');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const recommendationsDiv = document.getElementById('recommendations');
    const errorDiv = document.getElementById('error');

    searchBtn.addEventListener('click', getRecommendations);

    function getRecommendations() {
        const destination = destinationInput.value.trim();

        if (!destination) {
            alert('Please enter a destination');
            return;
        }
        
        loadingDiv.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        errorDiv.classList.add('hidden');

        const preferences = preferencesInput.value.trim();
        fetch('/get_recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                destination: destination,
                preferences: preferences
            })
        })
            .then(response => {
                console.log("HTTP Response:", response);
                return response.json();
            })
            .then(data => {
                loadingDiv.classList.add('hidden');

                if (data.error) {
                    errorDiv.classList.remove('hidden');
                    errorDiv.querySelector('p').textContent = data.error;
                    console.error("Error:", data.error);
                } else {
                    recommendationsDiv.innerHTML = data.recommendations;
                    resultsDiv.classList.remove('hidden');
                }
            })
            .catch(error => {
                loadingDiv.classList.add('hidden');
                errorDiv.classList.remove('hidden');
                errorDiv.querySelector('p').textContent = 'An unexpected error occurred. Please try again.';
                console.error('Fetch Error:', error);
            });
    }
});
