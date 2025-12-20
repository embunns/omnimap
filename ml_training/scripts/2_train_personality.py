import numpy as np
import pickle
import json
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

def load_processed_data(data_dir):
    """Load preprocessed data"""
    print(f"📂 Loading data from {data_dir}...")
    
    X_train = np.load(f'{data_dir}/X_train.npy')
    X_val = np.load(f'{data_dir}/X_val.npy')
    X_test = np.load(f'{data_dir}/X_test.npy')
    y_train = np.load(f'{data_dir}/y_train.npy')
    y_val = np.load(f'{data_dir}/y_val.npy')
    y_test = np.load(f'{data_dir}/y_test.npy')
    
    with open(f'{data_dir}/metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print(f"✅ Data loaded successfully")
    return X_train, X_val, X_test, y_train, y_val, y_test, metadata

def train_personality_model(X_train, y_train, X_val, y_val):
    """Train neural network for personality prediction"""
    print("🧠 Training personality model...")
    
    # Model architecture
    model = MLPRegressor(
        hidden_layer_sizes=(256, 128, 64),  # 3 hidden layers
        activation='relu',
        solver='adam',
        batch_size=32,
        learning_rate='adaptive',
        learning_rate_init=0.001,
        max_iter=100,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        random_state=42,
        verbose=True
    )
    
    # Train
    model.fit(X_train, y_train)
    
    # Validation metrics
    y_val_pred = model.predict(X_val)
    val_mse = mean_squared_error(y_val, y_val_pred)
    val_mae = mean_absolute_error(y_val, y_val_pred)
    val_r2 = r2_score(y_val, y_val_pred)
    
    print(f"\n📊 Validation Metrics:")
    print(f"   MSE: {val_mse:.4f}")
    print(f"   MAE: {val_mae:.4f}")
    print(f"   R²: {val_r2:.4f}")
    
    return model

def evaluate_model(model, X_test, y_test, label_names):
    """Evaluate model on test set"""
    print("\n📈 Evaluating on test set...")
    
    y_pred = model.predict(X_test)
    
    # Overall metrics
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n🎯 Test Metrics:")
    print(f"   MSE: {mse:.4f}")
    print(f"   MAE: {mae:.4f}")
    print(f"   R²: {r2:.4f}")
    
    # Per-trait metrics
    print(f"\n📊 Per-trait MAE:")
    for i, trait in enumerate(label_names):
        trait_mae = mean_absolute_error(y_test[:, i], y_pred[:, i])
        print(f"   {trait}: {trait_mae:.4f}")
    
    return {
        'mse': float(mse),
        'mae': float(mae),
        'r2': float(r2)
    }

def save_model(model, metrics, output_path):
    """Save trained model"""
    print(f"\n💾 Saving model to {output_path}...")
    
    model_package = {
        'model': model,
        'metrics': metrics,
        'model_type': 'MLPRegressor',
        'trained_date': str(np.datetime64('now'))
    }
    
    with open(output_path, 'wb') as f:
        pickle.dump(model_package, f)
    
    print("✅ Model saved successfully!")

def main():
    # Paths
    data_dir = 'ml_training/data/processed'
    model_dir = 'ml_models'
    
    # 1. Load data
    X_train, X_val, X_test, y_train, y_val, y_test, metadata = load_processed_data(data_dir)
    
    # 2. Train model
    model = train_personality_model(X_train, y_train, X_val, y_val)
    
    # 3. Evaluate
    metrics = evaluate_model(model, X_test, y_test, metadata['label_names'])
    
    # 4. Save model
    import os
    os.makedirs(model_dir, exist_ok=True)
    save_model(model, metrics, f'{model_dir}/personality_classifier.pkl')
    
    print("\n🎉 Training complete!")
    print(f"📁 Model saved to: {model_dir}/personality_classifier.pkl")
    print("\nNext step: Run 3_train_recommender.py")

if __name__ == '__main__':
    main()