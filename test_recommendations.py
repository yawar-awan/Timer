#!/usr/bin/env python3
"""
Test script for the recommendation system
"""

from recommendation_system import get_recommendations, get_movies, get_user_profile, add_user_rating

def test_recommendation_system():
    print("🎬 Movie Recommendation System Test")
    print("=" * 50)
    
    # Test 1: Get all movies
    print("\n1. Available Movies:")
    movies = get_movies()
    for movie in movies[:5]:  # Show first 5 movies
        print(f"   • {movie['title']} ({movie['year']}) - {movie['genre']}")
    print(f"   ... and {len(movies) - 5} more movies")
    
    # Test 2: Get user profile
    print("\n2. User Profile (User 1):")
    profile = get_user_profile(1)
    print(f"   User ID: {profile['user_id']}")
    print(f"   Movies Rated: {profile['total_movies']}")
    print(f"   Average Rating: {profile['avg_rating']}/5")
    print("   Rated Movies:")
    for rating in profile['ratings'][:3]:  # Show first 3 ratings
        print(f"     • {rating['title']} - {rating['rating']}/5 stars")
    
    # Test 3: Collaborative Filtering
    print("\n3. Collaborative Filtering Recommendations:")
    cf_recs = get_recommendations(1, 'collaborative', 3)
    for rec in cf_recs:
        print(f"   • {rec['title']} (Score: {rec.get('score', 'N/A')})")
    
    # Test 4: Content-Based Filtering
    print("\n4. Content-Based Recommendations:")
    cb_recs = get_recommendations(1, 'content', 3)
    for rec in cb_recs:
        print(f"   • {rec['title']} (Similarity: {rec.get('similarity', 'N/A')})")
    
    # Test 5: Hybrid Recommendations
    print("\n5. Hybrid Recommendations:")
    hybrid_recs = get_recommendations(1, 'hybrid', 3)
    for rec in hybrid_recs:
        print(f"   • {rec['title']} (Score: {rec.get('score', 'N/A')})")
    
    # Test 6: Add new rating
    print("\n6. Adding New Rating:")
    result = add_user_rating(1, 10, 4)  # User 1 rates Avatar 4 stars
    print(f"   Result: {result['message']}")
    
    # Test 7: Get updated recommendations
    print("\n7. Updated Recommendations after new rating:")
    updated_recs = get_recommendations(1, 'hybrid', 3)
    for rec in updated_recs:
        print(f"   • {rec['title']} (Score: {rec.get('score', 'N/A')})")
    
    print("\n✅ All tests completed successfully!")
    print("\n🌐 The web interface is running at: http://localhost:5000")
    print("   Try different users (1-5) and recommendation methods!")

if __name__ == "__main__":
    test_recommendation_system()