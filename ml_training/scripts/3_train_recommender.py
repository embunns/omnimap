import numpy as np
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

class ActivityRecommender:
    """Simple content-based recommender using cosine similarity"""
    
    def __init__(self):
        self.activity_profiles = None
        self.activity_ids = None
        self.trait_names = ['extraversion_t', 'agreeableness_t', 
                           'conscientiousness_t', 'neuroticism_t', 'openness_t']
    
    def fit(self, activities_df):
        """
        Fit recommender with activity profiles
        
        activities_df should have columns:
        - id: activity ID
        - required_traits: comma-separated traits (e.g., 'extraversion,openness')
        - You can manually create this or use existing Activity table
        """
        print("🎯 Training recommendation system...")
        
        # Create activity trait profiles (manual mapping)
        # Format: {'activity_id': [extraversion, agreeableness, conscientiousness, neuroticism, openness]}
        
        # EXAMPLE: Manual trait requirements untuk activities
        activity_profiles = {
            1: [0.7, 0.3, 0.5, -0.2, 0.8],  # UKM Seni (high openness, extraversion)
            2: [0.6, 0.4, 0.5, -0.1, 0.7],  # UKM Fotografi
            3: [0.5, 0.3, 0.6, -0.1, 0.9],  # Forum Sinema
            4: [0.9, 0.4, 0.5, -0.2, 0.7],  # Teater (very high extraversion)
            5: [0.4, 0.5, 0.8, -0.1, 0.6],  # Animasi (high conscientiousness)
            6: [0.6, 0.6, 0.5, -0.1, 0.7],  # SAWANDA
            7: [0.8, 0.5, 0.8, -0.1, 0.5],  # BEM (high extraversion, conscientiousness)
            8: [0.5, 0.6, 0.9, -0.2, 0.6],  # Hackathon (high conscientiousness)
        }
        
        self.activity_ids = list(activity_profiles.keys())
        self.activity_profiles = np.array([activity_profiles[aid] for aid in self.activity_ids])
        
        print(f"✅ Trained with {len(self.activity_ids)} activities")
        return self
    
    def recommend(self, user_traits, top_n=5):
        """
        Recommend activities based on user traits
        
        user_traits: array of [extraversion, agreeableness, conscientiousness, neuroticism, openness]
        Returns: list of (activity_id, similarity_score) sorted by score
        """
        # Normalize user traits to [-1, 1] range (assuming T-scores 20-80)
        user_normalized = (np.array(user_traits) - 50) / 30  # T-score normalization
        
        # Calculate cosine similarity
        similarities = cosine_similarity([user_normalized], self.activity_profiles)[0]
        
        # Convert to match percentage (0-100)
        match_percentages = ((similarities + 1) / 2) * 100
        
        # Sort and get top N
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        recommendations = [
            (self.activity_ids[idx], int(match_percentages[idx]))
            for idx in top_indices
        ]
        
        return recommendations
    
    def explain_recommendation(self, user_traits, activity_id):
        """Explain why an activity was recommended"""
        user_normalized = (np.array(user_traits) - 50) / 30
        activity_idx = self.activity_ids.index(activity_id)
        activity_profile = self.activity_profiles[activity_idx]
        
        # Calculate trait-by-trait match
        trait_matches = {}
        for i, trait in enumerate(self.trait_names):
            user_val = user_normalized[i]
            activity_val = activity_profile[i]
            match = 1 - abs(user_val - activity_val) / 2  # 0-1 scale
            trait_matches[trait] = match * 100
        
        return trait_matches

def save_recommender(recommender, output_path):
    """Save recommender model"""
    print(f"\n💾 Saving recommender to {output_path}...")
    
    with open(output_path, 'wb') as f:
        pickle.dump(recommender, f)
    
    print("✅ Recommender saved successfully!")

def test_recommender(recommender):
    """Test recommender with sample data"""
    print("\n🧪 Testing recommender...")
    
    # Test case: High extraversion, high openness user
    test_user = [65, 50, 50, 40, 70]  # T-scores
    print(f"\nTest user traits: {test_user}")
    
    recommendations = recommender.recommend(test_user, top_n=5)
    print("\nTop 5 recommendations:")
    for activity_id, match_pct in recommendations:
        print(f"   Activity {activity_id}: {match_pct}% match")
        
        # Explain
        explanation = recommender.explain_recommendation(test_user, activity_id)
        print(f"      Trait matches: {explanation}")

def main():
    # 1. Initialize and train recommender
    recommender = ActivityRecommender()
    recommender.fit(None)  # Uses manual profiles
    
    # 2. Test recommender
    test_recommender(recommender)
    
    # 3. Save recommender
    import os
    model_dir = 'ml_models'
    os.makedirs(model_dir, exist_ok=True)
    save_recommender(recommender, f'{model_dir}/activity_recommender.pkl')
    
    print("\n🎉 Recommender training complete!")
    print(f"📁 Model saved to: {model_dir}/activity_recommender.pkl")

if __name__ == '__main__':
    main()