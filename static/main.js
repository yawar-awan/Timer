class RecommendationApp {
    constructor() {
        this.currentUserId = null;
        this.currentMovieId = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadSystemStats();
    }

    bindEvents() {
        document.getElementById('loadUserBtn').addEventListener('click', () => this.loadUserProfile());
        document.getElementById('getRecommendationsBtn').addEventListener('click', () => this.getRecommendations());
        document.getElementById('loadMoviesBtn').addEventListener('click', () => this.loadMovies());
        document.getElementById('searchMovies').addEventListener('input', (e) => this.searchMovies(e.target.value));
        document.getElementById('submitRatingBtn').addEventListener('click', () => this.submitRating());
        
        // Modal events
        document.querySelector('.close').addEventListener('click', () => this.closeModal());
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal();
            }
        });
    }

    async loadUserProfile() {
        const userId = document.getElementById('userId').value;
        if (!userId) {
            this.showError('Please enter a user ID');
            return;
        }

        this.currentUserId = parseInt(userId);
        this.showLoading('userProfile');

        try {
            const response = await fetch(`/api/user/${userId}`);
            const data = await response.json();

            if (data.success) {
                this.displayUserProfile(data.profile);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Failed to load user profile');
        }
    }

    displayUserProfile(profile) {
        const profileSection = document.getElementById('userProfile');
        const profileContent = document.getElementById('profileContent');

        let html = `
            <div class="user-info">
                <h3>User ${profile.user_id}</h3>
                <p><strong>Total Movies Rated:</strong> ${profile.total_movies}</p>
                <p><strong>Average Rating:</strong> ${profile.avg_rating}/5</p>
            </div>
        `;

        if (profile.ratings.length > 0) {
            html += '<h4>Rated Movies:</h4>';
            profile.ratings.forEach(rating => {
                html += `
                    <div class="user-rating">
                        <strong>${rating.title}</strong> (${rating.year}) - ${rating.rating}/5 stars
                        <br><small>Genre: ${rating.genre}</small>
                    </div>
                `;
            });
        } else {
            html += '<p>No movies rated yet.</p>';
        }

        profileContent.innerHTML = html;
        profileSection.style.display = 'block';
    }

    async getRecommendations() {
        if (!this.currentUserId) {
            this.showError('Please load a user profile first');
            return;
        }

        const method = document.getElementById('methodSelect').value;
        this.showLoading('recommendations');

        try {
            const response = await fetch(`/api/recommendations/${this.currentUserId}?method=${method}&n=5`);
            const data = await response.json();

            if (data.success) {
                this.displayRecommendations(data.recommendations, method);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Failed to get recommendations');
        }
    }

    displayRecommendations(recommendations, method) {
        const recommendationsSection = document.getElementById('recommendations');
        const recommendationsContent = document.getElementById('recommendationsContent');

        let html = `<p><strong>Method:</strong> ${method.charAt(0).toUpperCase() + method.slice(1)} Filtering</p>`;

        if (recommendations.length === 0) {
            html += '<p>No recommendations available.</p>';
        } else {
            recommendations.forEach((movie, index) => {
                const score = movie.score || movie.similarity || 0;
                html += `
                    <div class="movie-card">
                        <h3>${movie.title}</h3>
                        <div class="movie-info">
                            <span><strong>Year:</strong> ${movie.year}</span>
                            <span><strong>Genre:</strong> ${movie.genre}</span>
                            <span><strong>IMDB Rating:</strong> ${movie.rating}/10</span>
                        </div>
                        <div class="rating-stars">${this.generateStars(movie.rating / 2)}</div>
                        <div class="recommendation-score">Score: ${score}</div>
                        <button class="btn btn-primary" onclick="app.rateMovie(${movie.id}, '${movie.title}')">
                            <i class="fas fa-star"></i> Rate This Movie
                        </button>
                    </div>
                `;
            });
        }

        recommendationsContent.innerHTML = html;
        recommendationsSection.style.display = 'block';
    }

    async loadMovies() {
        this.showLoading('moviesCatalog');

        try {
            const response = await fetch('/api/movies');
            const data = await response.json();

            if (data.success) {
                this.displayMovies(data.movies);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Failed to load movies');
        }
    }

    displayMovies(movies) {
        const moviesCatalog = document.getElementById('moviesCatalog');

        if (movies.length === 0) {
            moviesCatalog.innerHTML = '<p>No movies found.</p>';
            return;
        }

        let html = '';
        movies.forEach(movie => {
            html += `
                <div class="movie-card">
                    <h3>${movie.title}</h3>
                    <div class="movie-info">
                        <span><strong>Year:</strong> ${movie.year}</span>
                        <span><strong>Genre:</strong> ${movie.genre}</span>
                        <span><strong>IMDB Rating:</strong> ${movie.rating}/10</span>
                    </div>
                    <div class="rating-stars">${this.generateStars(movie.rating / 2)}</div>
                    <button class="btn btn-primary" onclick="app.rateMovie(${movie.id}, '${movie.title}')">
                        <i class="fas fa-star"></i> Rate This Movie
                    </button>
                </div>
            `;
        });

        moviesCatalog.innerHTML = html;
    }

    searchMovies(query) {
        const movieCards = document.querySelectorAll('#moviesCatalog .movie-card');
        const searchTerm = query.toLowerCase();

        movieCards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const genre = card.querySelector('.movie-info span:nth-child(2)').textContent.toLowerCase();
            
            if (title.includes(searchTerm) || genre.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    rateMovie(movieId, movieTitle) {
        if (!this.currentUserId) {
            this.showError('Please load a user profile first');
            return;
        }

        this.currentMovieId = movieId;
        const modal = document.getElementById('ratingModal');
        const modalMovieInfo = document.getElementById('modalMovieInfo');

        modalMovieInfo.innerHTML = `
            <h4>${movieTitle}</h4>
            <p>Please rate this movie:</p>
        `;

        modal.style.display = 'flex';
    }

    async submitRating() {
        const rating = parseInt(document.getElementById('ratingSelect').value);

        try {
            const response = await fetch('/api/rating', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.currentUserId,
                    movie_id: this.currentMovieId,
                    rating: rating
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showSuccess('Rating submitted successfully!');
                this.closeModal();
                // Refresh user profile
                if (this.currentUserId) {
                    this.loadUserProfile();
                }
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Failed to submit rating');
        }
    }

    async loadSystemStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();

            if (data.success) {
                this.displayStats(data.stats);
            }
        } catch (error) {
            console.error('Failed to load stats:', error);
        }
    }

    displayStats(stats) {
        const statsContainer = document.getElementById('systemStats');
        
        statsContainer.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>${stats.total_movies}</h3>
                    <p>Total Movies</p>
                </div>
                <div class="stat-card">
                    <h3>${stats.total_users}</h3>
                    <p>Active Users</p>
                </div>
                <div class="stat-card">
                    <h3>${stats.total_ratings}</h3>
                    <p>Total Ratings</p>
                </div>
                <div class="stat-card">
                    <h3>${stats.avg_rating}</h3>
                    <p>Average Rating</p>
                </div>
            </div>
        `;
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '';

        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }

        if (hasHalfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }

        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            stars += '<i class="far fa-star"></i>';
        }

        return stars;
    }

    showLoading(elementId) {
        const element = document.getElementById(elementId);
        element.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Loading...</div>';
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.error, .success');
        existingMessages.forEach(msg => msg.remove());

        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = type;
        messageDiv.textContent = message;

        // Insert at the top of the container
        const container = document.querySelector('.container');
        container.insertBefore(messageDiv, container.firstChild);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }

    closeModal() {
        document.getElementById('ratingModal').style.display = 'none';
    }
}

// Initialize the app when the page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new RecommendationApp();
});