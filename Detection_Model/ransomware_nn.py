import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# Load and Clean
data = pd.read_csv("datasets/Obfuscated-MalMem2022.csv")
def clean_category(cat):
    if 'Benign' in cat: return 'Benign'
    if 'Ransomware' in cat: return 'Ransomware'
    if 'Spyware' in cat: return 'Spyware'
    if 'Trojan' in cat: return 'Trojan'
    return 'Malware'

data['Category'] = data['Category'].apply(clean_category)
cat_encoder = LabelEncoder()
data['Category_Encoded'] = cat_encoder.fit_transform(data['Category'])
joblib.dump(cat_encoder, "models/category_encoder.pkl")

X = data.drop(["Class", "Category", "Category_Encoded"], axis=1)
y = data["Category_Encoded"]
feature_cols = list(X.columns)
joblib.dump(feature_cols, "models/feature_cols.pkl")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
joblib.dump(scaler, "models/scaler.pkl")

# Model
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    BatchNormalization(),
    Dense(len(cat_encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

history = model.fit(X_train, y_train, epochs=30, batch_size=64, validation_split=0.2, callbacks=[early_stop])
model.save("models/ransomware_model.keras")

# --- PLOTTING SECTION ---
def save_plots(history, X_test, y_test, model, encoder):
    # 1. Accuracy & Loss
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train')
    plt.plot(history.history['val_accuracy'], label='Val')
    plt.title('Model Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Val')
    plt.title('Model Loss')
    plt.legend()
    plt.savefig('plots/accuracy_loss.png')

    # 2. Confusion Matrix
    y_pred = np.argmax(model.predict(X_test), axis=1)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=encoder.classes_, yticklabels=encoder.classes_, cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig('plots/confusion_matrix.png')

    # 3. ROC Curve
    y_pred_proba = model.predict(X_test)
    plt.figure(figsize=(10, 8))
    for i in range(len(encoder.classes_)):
        fpr, tpr, _ = roc_curve(y_test == i, y_pred_proba[:, i])
        plt.plot(fpr, tpr, label=f'{encoder.classes_[i]} (AUC = {auc(fpr, tpr):.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title('ROC Curve')
    plt.legend()
    plt.savefig('plots/roc_auc.png')

save_plots(history, X_test, y_test, model, cat_encoder)
print("Training Complete. Plots saved to /plots/")