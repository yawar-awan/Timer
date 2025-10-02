import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import random
from typing import List, Dict, Tuple
import math

class RecommendationSystem:
    def __init__(self):
        self.movies_data = None
        self.user_ratings = None
        self.movie_features = None
        self.user_similarity_matrix = None
        self.movie_similarity_matrix = None
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        
    def load_sample_data(self):
        """Load sample movie data and user ratings"""
        # Sample movie data
        movies = [
            {"id": 1, "title": "The Dark Knight", "genre": "Action Crime Drama", "year": 2008, "rating": 9.0},
            {"id": 2, "title": "Inception", "genre": "Action Sci-Fi Thriller", "year": 2010, "rating": 8.8},
            {"id": 3, "title": "Pulp Fiction", "genre": "Crime Drama", "year": 1994, "rating": 8.9},
            {"id": 4, "title": "The Godfather", "genre": "Crime Drama", "year": 1972, "rating": 9.2},
            {"id": 5, "title": "Forrest Gump", "genre": "Drama Romance", "year": 1994, "rating": 8.8},
            {"id": 6, "title": "The Matrix", "genre": "Action Sci-Fi", "year": 1999, "rating": 8.7},
            {"id": 7, "title": "Goodfellas", "genre": "Crime Drama", "year": 1990, "rating": 8.7},
            {"id": 8, "title": "The Lord of the Rings", "genre": "Adventure Fantasy", "year": 2001, "rating": 8.8},
            {"id": 9, "title": "Titanic", "genre": "Drama Romance", "year": 1997, "rating": 7.8},
            {"id": 10, "title": "Avatar", "genre": "Action Adventure Sci-Fi", "year": 2009, "rating": 7.8},
            {"id": 11, "title": "Interstellar", "genre": "Adventure Drama Sci-Fi", "year": 2014, "rating": 8.6},
            {"id": 12, "title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "rating": 9.3},
            {"id": 13, "title": "Fight Club", "genre": "Drama Thriller", "year": 1999, "rating": 8.8},
            {"id": 14, "title": "The Avengers", "genre": "Action Adventure Sci-Fi", "year": 2012, "rating": 8.0},
            {"id": 15, "title": "Casablanca", "genre": "Drama Romance War", "year": 1942, "rating": 8.5}
        ]
        
        # Sample user ratings (user_id, movie_id, rating)
        ratings = [
            (1, 1, 5), (1, 2, 4), (1, 3, 5), (1, 4, 5), (1, 6, 4),
            (2, 1, 4), (2, 2, 5), (2, 5, 4), (2, 8, 5), (2, 12, 5),
            (3, 3, 5), (3, 4, 5), (3, 7, 4), (3, 9, 3), (3, 13, 4),
            (4, 2, 5), (4, 6, 4), (4, 10, 3), (4, 11, 5), (4, 14, 4),
            (5, 1, 5), (5, 3, 4), (5, 5, 4), (5, 8, 5), (5, 12, 5)
        ]
        
        self.movies_data = pd.DataFrame(movies)
        self.user_ratings = pd.DataFrame(ratings, columns=['user_id', 'movie_id', 'rating'])
        
        # Create user-movie rating matrix
        self.rating_matrix = self.user_ratings.pivot_table(
            index='user_id', columns='movie_id', values='rating', fill_value=0
        )
        
        return self.movies_data, self.user_ratings
    
    def collaborative_filtering(self, user_id: int, n_recommendations: int = 5) -> List[Dict]:
        """User-based collaborative filtering"""
        if user_id not in self.rating_matrix.index:
            return self._get_popular_movies(n_recommendations)
        
        # Calculate user similarity
        user_ratings = self.rating_matrix.loc[user_id]
        similarities = []
        
        for other_user in self.rating_matrix.index:
            if other_user != user_id:
                other_ratings = self.rating_matrix.loc[other_user]
                # Calculate cosine similarity
                common_movies = (user_ratings > 0) & (other_ratings > 0)
                if common_movies.sum() > 0:
                    sim = cosine_similarity(
                        user_ratings[common_movies].values.reshape(1, -1),
                        other_ratings[common_movies].values.reshape(1, -1)
                    )[0][0]
                    similarities.append((other_user, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get recommendations from similar users
        recommendations = {}
        for other_user, sim in similarities[:5]:  # Top 5 similar users
            other_ratings = self.rating_matrix.loc[other_user]
            for movie_id in other_ratings.index:
                if other_ratings[movie_id] > 0 and user_ratings[movie_id] == 0:
                    if movie_id not in recommendations:
                        recommendations[movie_id] = 0
                    recommendations[movie_id] += sim * other_ratings[movie_id]
        
        # Sort and return top recommendations
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        for movie_id, score in sorted_recs[:n_recommendations]:
            movie_info = self.movies_data[self.movies_data['id'] == movie_id].iloc[0]
            result.append({
                'id': movie_id,
                'title': movie_info['title'],
                'genre': movie_info['genre'],
                'year': movie_info['year'],
                'rating': movie_info['rating'],
                'score': round(score, 2)
            })
        
        return result
    
    def content_based_filtering(self, movie_id: int, n_recommendations: int = 5) -> List[Dict]:
        """Content-based filtering using movie features"""
        if movie_id not in self.movies_data['id'].values:
            return self._get_popular_movies(n_recommendations)
        
        # Create feature matrix from genres
        movie_features = self.tfidf_vectorizer.fit_transform(self.movies_data['genre'])
        
        # Get similarity matrix
        similarity_matrix = cosine_similarity(movie_features)
        
        # Get movie index
        movie_idx = self.movies_data[self.movies_data['id'] == movie_id].index[0]
        
        # Get similar movies
        similar_movies = similarity_matrix[movie_idx]
        similar_indices = similar_movies.argsort()[::-1][1:n_recommendations+1]  # Exclude the movie itself
        
        result = []
        for idx in similar_indices:
            movie_info = self.movies_data.iloc[idx]
            result.append({
                'id': movie_info['id'],
                'title': movie_info['title'],
                'genre': movie_info['genre'],
                'year': movie_info['year'],
                'rating': movie_info['rating'],
                'similarity': round(similar_movies[idx], 3)
            })
        
        return result
    
    def hybrid_recommendation(self, user_id: int, n_recommendations: int = 5) -> List[Dict]:
        """Hybrid approach combining collaborative and content-based filtering"""
        # Get collaborative filtering recommendations
        cf_recs = self.collaborative_filtering(user_id, n_recommendations * 2)
        
        # Get user's top-rated movies for content-based recommendations
        user_ratings = self.user_ratings[self.user_ratings['user_id'] == user_id]
        if len(user_ratings) > 0:
            top_movie = user_ratings.loc[user_ratings['rating'].idxmax(), 'movie_id']
            cb_recs = self.content_based_filtering(top_movie, n_recommendations)
        else:
            cb_recs = self._get_popular_movies(n_recommendations)
        
        # Combine and deduplicate
        all_recs = {}
        
        # Add collaborative filtering results with higher weight
        for rec in cf_recs:
            movie_id = rec['id']
            all_recs[movie_id] = rec.copy()
            all_recs[movie_id]['score'] = rec.get('score', 0) * 0.7
        
        # Add content-based results
        for rec in cb_recs:
            movie_id = rec['id']
            if movie_id in all_recs:
                all_recs[movie_id]['score'] += rec.get('similarity', 0) * 0.3
            else:
                all_recs[movie_id] = rec.copy()
                all_recs[movie_id]['score'] = rec.get('similarity', 0) * 0.3
        
        # Sort by combined score
        sorted_recs = sorted(all_recs.values(), key=lambda x: x['score'], reverse=True)
        return sorted_recs[:n_recommendations]
    
    def _get_popular_movies(self, n_recommendations: int) -> List[Dict]:
        """Get popular movies as fallback"""
        popular = self.movies_data.nlargest(n_recommendations, 'rating')
        return popular.to_dict('records')
    
    def get_user_profile(self, user_id: int) -> Dict:
        """Get user's rating profile"""
        user_ratings = self.user_ratings[self.user_ratings['user_id'] == user_id]
        if len(user_ratings) == 0:
            return {'user_id': user_id, 'ratings': [], 'avg_rating': 0, 'total_movies': 0}
        
        ratings_with_movies = []
        for _, rating in user_ratings.iterrows():
            movie_info = self.movies_data[self.movies_data['id'] == rating['movie_id']].iloc[0]
            ratings_with_movies.append({
                'movie_id': rating['movie_id'],
                'title': movie_info['title'],
                'rating': rating['rating'],
                'genre': movie_info['genre']
            })
        
        return {
            'user_id': user_id,
            'ratings': ratings_with_movies,
            'avg_rating': round(user_ratings['rating'].mean(), 2),
            'total_movies': len(user_ratings)
        }
    
    def add_rating(self, user_id: int, movie_id: int, rating: int):
        """Add a new rating"""
        new_rating = pd.DataFrame([{
            'user_id': user_id,
            'movie_id': movie_id,
            'rating': rating
        }])
        self.user_ratings = pd.concat([self.user_ratings, new_rating], ignore_index=True)
        
        # Update rating matrix
        self.rating_matrix = self.user_ratings.pivot_table(
            index='user_id', columns='movie_id', values='rating', fill_value=0
        )

# Initialize the recommendation system
rec_system = RecommendationSystem()
rec_system.load_sample_data()

def get_recommendations(user_id: int, method: str = 'hybrid', n_recommendations: int = 5):
    """Main function to get recommendations"""
    if method == 'collaborative':
        return rec_system.collaborative_filtering(user_id, n_recommendations)
    elif method == 'content':
        # For content-based, we'll use the user's highest rated movie
        user_ratings = rec_system.user_ratings[rec_system.user_ratings['user_id'] == user_id]
        if len(user_ratings) > 0:
            top_movie = user_ratings.loc[user_ratings['rating'].idxmax(), 'movie_id']
            return rec_system.content_based_filtering(top_movie, n_recommendations)
        else:
            return rec_system._get_popular_movies(n_recommendations)
    else:  # hybrid
        return rec_system.hybrid_recommendation(user_id, n_recommendations)

def get_movies():
    """Get all movies"""
    return rec_system.movies_data.to_dict('records')

def get_user_profile(user_id: int):
    """Get user profile"""
    return rec_system.get_user_profile(user_id)

def add_user_rating(user_id: int, movie_id: int, rating: int):
    """Add user rating"""
    rec_system.add_rating(user_id, movie_id, rating)
    return {"status": "success", "message": "Rating added successfully"}