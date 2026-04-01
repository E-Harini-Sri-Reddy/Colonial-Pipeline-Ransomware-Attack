import os
import pandas as pd
import numpy as np
import joblib
import warnings

# 1. Suppress TensorFlow and Sklearn warnings for a cleaner output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings("ignore", category=UserWarning)

from tensorflow.keras.models import load_model

# Load model and tools
model = load_model("models/ransomware_model.keras")
scaler = joblib.load("models/scaler.pkl")
cat_encoder = joblib.load("models/category_encoder.pkl")

# Load dataset for sampling
data = pd.read_csv("datasets/Obfuscated-MalMem2022.csv")

# Take 20 random samples
samples = data.sample(20)

# Get the list of feature names the scaler expects
feature_cols = [col for col in data.columns if col not in ["Class", "Category"]]

print("\n" + "="*40)
print("RUNNING MALWARE ANALYSIS")
print("="*40)

for i, (_, sample) in enumerate(samples.iterrows(), start=1):
    
    # 2. Prepare Features as a DataFrame to keep feature names (removes Warning)
    features_df = pd.DataFrame([sample[feature_cols]])
    features_scaled = scaler.transform(features_df)

    # Predict Probabilities
    probs = model.predict(features_scaled, verbose=0)[0]
    
    # Get Top Prediction
    pred_idx = np.argmax(probs)
    pred_cat_name = cat_encoder.classes_[pred_idx]
    confidence = probs[pred_idx] * 100

    # Map Category to Class
    actual_class = sample["Class"]
    predicted_class = "Benign" if pred_cat_name == "Benign" else "Malware"

    # 3. Format Output
    print(f"------------------------")
    print(f"Record {i}:")
    print(f"Actual Class    : {actual_class}")
    print(f"Predicted Class : {predicted_class}")
    print(f"Confidence Level : {confidence:.1f}%")
    
    print("\nCategory Probabilities")
    # Sort and display categories
    class_probs = sorted(zip(cat_encoder.classes_, probs), key=lambda x: x[1], reverse=True)
    for name, prob in class_probs:
        if prob > 0.0001: 
            print(f"{name}: {prob*100:.2f}%")
    print("")

print("------------------------")