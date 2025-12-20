import pickle
import os
from functools import lru_cache

# Global model cache
_model_cache = {}

@lru_cache(maxsize=None)
def load_personality_model(model_path='ml_models/personality_classifier.pkl'):
    """Load personality prediction model (cached)"""
    if 'personality' in _model_cache:
        return _model_cache['personality']
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    print(f"📦 Loading personality model from {model_path}...")
    with open(model_path, 'rb') as f:
        model_package = pickle.load(f)
    
    _model_cache['personality'] = model_package
    print("✅ Personality model loaded successfully")
    return model_package

@lru_cache(maxsize=None)
def load_recommender_model(model_path='ml_models/activity_recommender.pkl'):
    """Load activity recommender model (cached)"""
    if 'recommender' in _model_cache:
        return _model_cache['recommender']
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    print(f"📦 Loading recommender model from {model_path}...")
    with open(model_path, 'rb') as f:
        recommender = pickle.load(f)
    
    _model_cache['recommender'] = recommender
    print("✅ Recommender model loaded successfully")
    return recommender

@lru_cache(maxsize=None)
def load_scaler(scaler_path='ml_training/data/processed/scaler.pkl'):
    """Load feature scaler (cached)"""
    if 'scaler' in _model_cache:
        return _model_cache['scaler']
    
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler not found: {scaler_path}")
    
    print(f"📦 Loading scaler from {scaler_path}...")
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    
    _model_cache['scaler'] = scaler
    print("✅ Scaler loaded successfully")
    return scaler

def load_all_models():
    """Load all models at app startup"""
    print("🚀 Loading all ML models...")
    try:
        personality = load_personality_model()
        recommender = load_recommender_model()
        scaler = load_scaler()
        print("✅ All models loaded successfully!")
        return True
    except FileNotFoundError as e:
        print(f"⚠️ Model loading failed: {e}")
        print("💡 Please train models first by running:")
        print("   1. python ml_training/scripts/1_preprocess_data.py")
        print("   2. python ml_training/scripts/2_train_personality.py")
        print("   3. python ml_training/scripts/3_train_recommender.py")
        return False

def predict_personality(answers):
    """
    Predict personality from 200 answers
    
    Args:
        answers: list/array of 200 integer answers (1-5)
    
    Returns:
        dict with Big Five T-scores
    """
    try:
        model_package = load_personality_model()
        scaler = load_scaler()
        
        # Preprocess
        import numpy as np
        X = np.array(answers).reshape(1, -1)
        X_scaled = scaler.transform(X)
        
        # Predict
        predictions = model_package['model'].predict(X_scaled)[0]
        
        # Format results
        trait_names = ['extraversion_t', 'agreeableness_t', 'conscientiousness_t',
                       'neuroticism_t', 'openness_t']
        
        results = {trait: float(score) for trait, score in zip(trait_names, predictions)}
        
        return results
    
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return None

def recommend_activities(user_traits, top_n=10):
    """
    Recommend activities based on user traits
    
    Args:
        user_traits: dict or list of Big Five T-scores
        top_n: number of recommendations
    
    Returns:
        list of (activity_id, match_percentage)
    """
    try:
        recommender = load_recommender_model()
        
        # Convert to array if dict
        if isinstance(user_traits, dict):
            trait_order = ['extraversion_t', 'agreeableness_t', 'conscientiousness_t',
                          'neuroticism_t', 'openness_t']
            user_traits = [user_traits.get(t, 50) for t in trait_order]
        
        # Get recommendations
        recommendations = recommender.recommend(user_traits, top_n=top_n)
        
        return recommendations
    
    except Exception as e:
        print(f"❌ Recommendation error: {e}")
        return []