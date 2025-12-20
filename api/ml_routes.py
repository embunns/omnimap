# api/ml_routes.py
# ADD THIS TO app.py or create as separate blueprint

from flask import Blueprint, request, jsonify, session
from utils.model_loader import predict_personality, recommend_activities, load_all_models

ml_bp = Blueprint('ml', __name__, url_prefix='/api/ml')

@ml_bp.route('/predict-personality', methods=['POST'])
def api_predict_personality():
    """
    Predict personality dari 200 jawaban
    
    Request body:
    {
        "answers": [1, 2, 3, ..., 5]  // 200 integers (1-5)
    }
    
    Response:
    {
        "success": true,
        "predictions": {
            "extraversion_t": 55.4,
            "agreeableness_t": 48.2,
            ...
        },
        "method": "manual_model"  // or "api_fallback"
    }
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        answers = data.get('answers')
        
        if not answers or len(answers) != 200:
            return jsonify({
                'success': False,
                'error': 'Must provide exactly 200 answers'
            }), 400
        
        # TRY MANUAL MODEL FIRST
        try:
            predictions = predict_personality(answers)
            
            if predictions:
                return jsonify({
                    'success': True,
                    'predictions': predictions,
                    'method': 'manual_model'
                })
        except Exception as e:
            print(f"⚠️ Manual model failed: {e}")
        
        # FALLBACK TO API (your existing API code)
        # TODO: Add your API prediction code here
        return jsonify({
            'success': False,
            'error': 'Both manual model and API failed',
            'message': 'Please ensure models are trained or API is configured'
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ml_bp.route('/recommend-activities', methods=['POST'])
def api_recommend_activities():
    """
    Get activity recommendations
    
    Request body:
    {
        "traits": {
            "extraversion_t": 55,
            "agreeableness_t": 48,
            ...
        },
        "top_n": 10
    }
    
    Response:
    {
        "success": true,
        "recommendations": [
            {"activity_id": 1, "match_percentage": 85},
            ...
        ],
        "method": "manual_model"
    }
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        traits = data.get('traits')
        top_n = data.get('top_n', 10)
        
        # TRY MANUAL MODEL FIRST
        try:
            recommendations = recommend_activities(traits, top_n=top_n)
            
            if recommendations:
                return jsonify({
                    'success': True,
                    'recommendations': [
                        {'activity_id': aid, 'match_percentage': match}
                        for aid, match in recommendations
                    ],
                    'method': 'manual_model'
                })
        except Exception as e:
            print(f"⚠️ Manual recommender failed: {e}")
        
        # FALLBACK TO EXISTING LOGIC
        # Your existing calculate_activity_match function
        return jsonify({
            'success': False,
            'error': 'Recommender not available'
        }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ml_bp.route('/model-status', methods=['GET'])
def api_model_status():
    """Check if ML models are loaded"""
    try:
        from utils.model_loader import _model_cache
        
        status = {
            'personality_model': 'personality' in _model_cache,
            'recommender_model': 'recommender' in _model_cache,
            'scaler': 'scaler' in _model_cache
        }
        
        return jsonify({
            'success': True,
            'models_loaded': status,
            'all_ready': all(status.values())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Register blueprint in app.py:
# from api.ml_routes import ml_bp
# app.register_blueprint(ml_bp)