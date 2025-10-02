# Movie Recommendation System

A comprehensive recommendation system that uses multiple AI algorithms to suggest movies to users based on their preferences and viewing history.

## Features

- **Multiple Recommendation Algorithms**:
  - Collaborative Filtering (User-based)
  - Content-Based Filtering
  - Hybrid Approach (Combines both methods)

- **Interactive Web Interface**:
  - User profile management
  - Movie rating system
  - Real-time recommendations
  - Movie catalog browsing
  - System statistics

- **Sample Dataset**:
  - 15 popular movies with genres and ratings
  - Pre-loaded user ratings for testing
  - Expandable movie database

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Getting Started

1. **Select a User**: Enter a user ID (1-5) and click "Load Profile" to see their rating history
2. **Get Recommendations**: Choose a recommendation method and click "Get Recommendations"
3. **Rate Movies**: Browse the movie catalog and rate movies to improve recommendations
4. **View Statistics**: Check system statistics to see overall usage

### Recommendation Methods

- **Hybrid (Recommended)**: Combines collaborative and content-based filtering for best results
- **Collaborative Filtering**: Recommends movies based on similar users' preferences
- **Content-Based**: Recommends movies similar to ones you've already rated highly

### API Endpoints

- `GET /api/movies` - Get all movies
- `GET /api/recommendations/<user_id>` - Get recommendations for a user
- `GET /api/user/<user_id>` - Get user profile
- `POST /api/rating` - Add a movie rating
- `GET /api/stats` - Get system statistics

## Sample Users

The system comes with 5 sample users with different rating patterns:

- **User 1**: Action and crime movie enthusiast
- **User 2**: Drama and fantasy lover
- **User 3**: Crime drama fan
- **User 4**: Sci-fi and action fan
- **User 5**: Classic movie lover

## Technical Details

### Algorithms Implemented

1. **Collaborative Filtering**:
   - Uses cosine similarity to find similar users
   - Recommends movies liked by similar users
   - Handles sparse data with fallback to popular movies

2. **Content-Based Filtering**:
   - Uses TF-IDF vectorization on movie genres
   - Calculates cosine similarity between movies
   - Recommends movies with similar content

3. **Hybrid Approach**:
   - Combines both methods with weighted scores
   - Collaborative filtering: 70% weight
   - Content-based filtering: 30% weight

### Data Structure

- **Movies**: ID, title, genre, year, IMDB rating
- **Ratings**: User ID, movie ID, rating (1-5 stars)
- **Users**: Dynamic user profiles based on rating history

## Customization

### Adding New Movies

Edit the `load_sample_data()` method in `recommendation_system.py` to add more movies to the dataset.

### Adding New Users

The system automatically creates new users when they rate movies. No manual user creation needed.

### Modifying Algorithms

The recommendation algorithms can be customized in the `RecommendationSystem` class methods:
- `collaborative_filtering()`
- `content_based_filtering()`
- `hybrid_recommendation()`

## Future Enhancements

- Machine learning model training
- Real-time recommendation updates
- Advanced user profiling
- Movie similarity visualization
- Recommendation explanation features
- Multi-domain recommendations (books, music, etc.)

## License

This project is open source and available under the MIT License.