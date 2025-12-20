import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import json
import os
import pickle

def load_excel_data(file_path):
    """Load data from Excel file"""
    print(f"📂 Loading data from {file_path}...")
    df = pd.read_excel(file_path)
    print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def clean_data(df):
    """Clean and prepare data"""
    print("🧹 Cleaning data...")
    
    # Handle missing values
    df = df.fillna(0)
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    print(f"✅ Data cleaned: {len(df)} rows remaining")
    return df

def calculate_scores_from_answers(df, answer_cols):
    """
    Calculate raw scores and T-scores from answers
    Menggunakan scoring logic dari app.py
    """
    print("🧮 Calculating personality scores from answers...")
    
    # Mapping pertanyaan ke traits (sesuai dengan tes OMNI standar)
    # Setiap trait punya 8 pertanyaan
    trait_questions = {
        'energy': list(range(0, 8)),
        'sociability': list(range(8, 16)),
        'assertiveness': list(range(16, 24)),
        'excitement': list(range(24, 32)),
        'warmth': list(range(32, 40)),
        'trustfulness': list(range(40, 48)),
        'sincerity': list(range(48, 56)),
        'modesty': list(range(56, 64)),
        'dutifulness': list(range(64, 72)),
        'orderliness': list(range(72, 80)),
        'self_reliance': list(range(80, 88)),
        'ambition': list(range(88, 96)),
        'anxiety': list(range(96, 104)),
        'depression': list(range(104, 112)),
        'moodiness': list(range(112, 120)),
        'irritability': list(range(120, 128)),
        'aestheticism': list(range(128, 136)),
        'intellect': list(range(136, 144)),
        'flexibility': list(range(144, 152)),
        'tolerance': list(range(152, 160)),
        'exhibitionism': list(range(160, 168)),
        'self_indulgence': list(range(168, 176)),
        'impulsiveness': list(range(176, 184)),
        'hostility': list(range(184, 192)),
        'conventionality': list(range(192, 200))
    }
    
    # Calculate raw scores for each trait
    answers_array = df[answer_cols].values
    
    trait_raw_scores = {}
    for trait, indices in trait_questions.items():
        # Sum of answers for this trait (8 questions, each 1-5)
        trait_raw_scores[trait] = answers_array[:, indices].sum(axis=1)
    
    # Calculate Big Five domain scores
    domain_mapping = {
        'extraversion': ['energy', 'sociability', 'assertiveness', 'excitement'],
        'agreeableness': ['warmth', 'trustfulness', 'sincerity', 'modesty'],
        'conscientiousness': ['dutifulness', 'orderliness', 'self_reliance', 'ambition'],
        'neuroticism': ['anxiety', 'depression', 'moodiness', 'irritability'],
        'openness': ['aestheticism', 'intellect', 'flexibility', 'tolerance']
    }
    
    domain_raw_scores = {}
    for domain, facets in domain_mapping.items():
        domain_raw_scores[domain] = sum(trait_raw_scores[f] for f in facets)
    
    # Convert to T-scores (simplified: mean=50, sd=10)
    # T-score = 50 + 10 * (raw - mean) / sd
    trait_t_scores = {}
    
    for trait, raw_scores in trait_raw_scores.items():
        mean = raw_scores.mean()
        std = raw_scores.std()
        if std > 0:
            t_scores = 50 + 10 * (raw_scores - mean) / std
        else:
            t_scores = np.full_like(raw_scores, 50.0)
        # Clamp to reasonable range (20-80)
        trait_t_scores[trait] = np.clip(t_scores, 20, 80)
    
    for domain, raw_scores in domain_raw_scores.items():
        mean = raw_scores.mean()
        std = raw_scores.std()
        if std > 0:
            t_scores = 50 + 10 * (raw_scores - mean) / std
        else:
            t_scores = np.full_like(raw_scores, 50.0)
        trait_t_scores[domain] = np.clip(t_scores, 20, 80)
    
    print(f"✅ Calculated scores for {len(trait_t_scores)} traits")
    
    return trait_t_scores

def extract_features_labels(df):
    """Extract features (answers) and labels (personality scores)"""
    print("🎯 Extracting features and labels...")
    
    # Cek kolom yang tersedia
    print(f"📊 Total columns: {len(df.columns)}")
    print(f"📋 Column names sample: {df.columns[:10].tolist()}")
    
    # AUTO-DETECT answer columns (biasanya Q1-Q200 atau soal_1-soal_200)
    answer_cols = []
    for col in df.columns:
        # Cek berbagai format: Q1, soal_1, jawaban_1, dll
        if any(pattern in str(col).lower() for pattern in ['q', 'soal', 'jawab', 'answer']):
            if any(char.isdigit() for char in str(col)):
                answer_cols.append(col)
    
    # Sort kolom berdasarkan nomor
    import re
    def get_number(s):
        nums = re.findall(r'\d+', str(s))
        return int(nums[0]) if nums else 0
    
    answer_cols = sorted(answer_cols, key=get_number)
    
    # Take first 200 answer columns
    if len(answer_cols) >= 200:
        answer_cols = answer_cols[:200]
        print(f"✅ Found {len(answer_cols)} answer columns")
        print(f"📝 Using: {answer_cols[0]} to {answer_cols[-1]}")
    else:
        raise ValueError(f"❌ Only found {len(answer_cols)} answer columns, need 200!")
    
    X = df[answer_cols].values
    
    # AUTO-DETECT trait columns (yang ada _t suffix)
    trait_cols = [col for col in df.columns if str(col).endswith('_t')]
    
    if len(trait_cols) == 0:
        print("⚠️ No T-score columns found in Excel")
        print("🧮 Calculating T-scores from answers...")
        
        # Calculate scores from answers
        trait_scores = calculate_scores_from_answers(df, answer_cols)
        
        # Big Five domains
        big_five_names = ['extraversion', 'agreeableness', 'conscientiousness', 
                         'neuroticism', 'openness']
        y_big_five = np.column_stack([trait_scores[name] for name in big_five_names])
        
        # All traits (25 facets + 5 domains)
        all_trait_names = list(trait_scores.keys())
        y_all = np.column_stack([trait_scores[name] for name in all_trait_names])
        
        trait_cols = [f"{name}_t" for name in all_trait_names]
        
        print(f"✅ Calculated {len(trait_cols)} trait T-scores")
    else:
        print(f"✅ Found {len(trait_cols)} trait columns: {trait_cols[:5]}...")
        
        # Extract Big Five if available
        big_five_cols = [col for col in trait_cols if any(domain in col.lower() 
                         for domain in ['extraversion', 'agreeableness', 'conscientiousness', 
                                       'neuroticism', 'openness'])]
        
        if len(big_five_cols) >= 5:
            y_big_five = df[big_five_cols[:5]].values
            print(f"✅ Big Five columns: {big_five_cols[:5]}")
        else:
            print(f"⚠️ Warning: Only found {len(big_five_cols)} Big Five traits")
            y_big_five = df[trait_cols[:5]].values if len(trait_cols) >= 5 else None
        
        # All traits
        y_all = df[trait_cols].values if len(trait_cols) > 0 else None
    
    print(f"✅ Features shape: {X.shape}")
    print(f"✅ Big Five labels shape: {y_big_five.shape}")
    print(f"✅ All traits labels shape: {y_all.shape}")
    
    return X, y_big_five, y_all, answer_cols, trait_cols

def split_and_scale_data(X, y, test_size=0.15, val_size=0.15):
    """Split data into train/val/test and scale"""
    print("✂️ Splitting data...")
    
    # First split: train+val vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Second split: train vs val
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_ratio, random_state=42
    )
    
    print(f"✅ Train: {X_train.shape[0]} samples")
    print(f"✅ Val: {X_val.shape[0]} samples")
    print(f"✅ Test: {X_test.shape[0]} samples")
    
    # Scale features
    print("⚖️ Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    return (X_train_scaled, X_val_scaled, X_test_scaled,
            y_train, y_val, y_test, scaler)

def save_processed_data(X_train, X_val, X_test, y_train, y_val, y_test, 
                       scaler, feature_names, label_names, output_dir):
    """Save processed data"""
    print(f"💾 Saving processed data to {output_dir}...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Save splits as numpy arrays (faster for training)
    np.save(f'{output_dir}/X_train.npy', X_train)
    np.save(f'{output_dir}/X_val.npy', X_val)
    np.save(f'{output_dir}/X_test.npy', X_test)
    np.save(f'{output_dir}/y_train.npy', y_train)
    np.save(f'{output_dir}/y_val.npy', y_val)
    np.save(f'{output_dir}/y_test.npy', y_test)
    
    # Save scaler
    with open(f'{output_dir}/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Save metadata
    metadata = {
        'n_features': X_train.shape[1],
        'n_labels': y_train.shape[1],
        'n_train': X_train.shape[0],
        'n_val': X_val.shape[0],
        'n_test': X_test.shape[0],
        'feature_names': feature_names,
        'label_names': label_names,
        'preprocessing_date': str(pd.Timestamp.now())
    }
    
    with open(f'{output_dir}/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ All data saved successfully!")
    print(f"📊 Metadata: {metadata}")

def main():
    # Paths
    excel_path = 'ml_training/data/raw/data_tes_omni.xlsx'
    output_dir = 'ml_training/data/processed'
    
    # 1. Load data
    df = load_excel_data(excel_path)
    
    # 2. Clean data
    df = clean_data(df)
    
    # 3. Extract features and labels
    X, y_big_five, y_all, feature_names, label_names = extract_features_labels(df)
    
    # 4. Split and scale (using Big Five for simplicity)
    # Anda bisa ganti y_big_five dengan y_all jika ingin prediksi semua traits
    splits = split_and_scale_data(X, y_big_five)
    X_train, X_val, X_test, y_train, y_val, y_test, scaler = splits
    
    # 5. Save everything
    save_processed_data(
        X_train, X_val, X_test, y_train, y_val, y_test,
        scaler, feature_names, label_names[:5], output_dir  # Big Five labels
    )
    
    print("\n🎉 Preprocessing complete!")
    print(f"📁 Output directory: {output_dir}")
    print("\nNext step: Run 2_train_personality.py")

if __name__ == '__main__':
    main()