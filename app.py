from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from recommendation_system import (
    get_recommendations, 
    get_movies, 
    get_user_profile, 
    add_user_rating,
    rec_system
)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/movies', methods=['GET'])
def api_get_movies():
    """Get all movies"""
    try:
        movies = get_movies()
        return jsonify({'success': True, 'movies': movies})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/recommendations/<int:user_id>', methods=['GET'])
def api_get_recommendations(user_id):
    """Get recommendations for a user"""
    try:
        method = request.args.get('method', 'hybrid')
        n_recommendations = int(request.args.get('n', 5))
        
        recommendations = get_recommendations(user_id, method, n_recommendations)
        return jsonify({
            'success': True, 
            'recommendations': recommendations,
            'method': method,
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/user/<int:user_id>', methods=['GET'])
def api_get_user_profile(user_id):
    """Get user profile"""
    try:
        profile = get_user_profile(user_id)
        return jsonify({'success': True, 'profile': profile})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/rating', methods=['POST'])
def api_add_rating():
    """Add a user rating"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        
        if not all([user_id, movie_id, rating]):
            return jsonify({'success': False, 'error': 'Missing required fields'})
        
        result = add_user_rating(user_id, movie_id, rating)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """Get system statistics"""
    try:
        stats = {
            'total_movies': len(rec_system.movies_data),
            'total_users': rec_system.user_ratings['user_id'].nunique(),
            'total_ratings': len(rec_system.user_ratings),
            'avg_rating': round(rec_system.user_ratings['rating'].mean(), 2)
        }
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)