import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px  # Great for interactive charts
from tensorflow.keras.models import load_model

# --- Page Config ---
st.set_page_config(
    page_title="AI Malware Analytics",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Memory Threat Analytics Dashboard")


# --- Load Models & Assets ---
@st.cache_resource
def load_assets():
    model = load_model("models/ransomware_model.keras")
    scaler = joblib.load("models/scaler.pkl")
    cat_encoder = joblib.load("models/category_encoder.pkl")
    return model, scaler, cat_encoder


model, scaler, cat_encoder = load_assets()


# --- File Upload ---
uploaded_file = st.file_uploader("Upload Memory Dump CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Drop non-feature columns if present
    features = df.drop(columns=['Class', 'Category'], errors='ignore')

    if st.button('🚀 Run Deep Scan'):

        # --- 1. Prediction Logic ---
        scaled_features = scaler.transform(features)
        predictions = model.predict(scaled_features)

        # --- 2. Process Results ---
        pred_indices = np.argmax(predictions, axis=1)
        confidences = np.max(predictions, axis=1) * 100
        labels = [cat_encoder.classes_[i] for i in pred_indices]

        results_df = pd.DataFrame({
            "Classification": labels,
            "Confidence": confidences
        })

        # --- 3. DASHBOARD SECTION ---
        st.divider()
        st.subheader("📊 Scan Analysis Summary")

        col1, col2 = st.columns([1, 1])

        with col1:
            # Pie Chart: Threat Distribution
            fig_pie = px.pie(
                results_df,
                names='Classification',
                title="Threat Distribution",
                color='Classification',
                color_discrete_map={
                    'Benign': '#2ecc71',
                    'Ransomware': '#e74c3c',
                    'Spyware': '#f1c40f'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Metrics & Statistics
            threat_count = results_df[
                results_df['Classification'] != 'Benign'
            ].shape[0]

            avg_conf = results_df['Confidence'].mean()

            st.metric(
                "Total Threats Detected",
                threat_count,
                delta=f"{threat_count / len(df) * 100:.1f}% of total"
            )

            st.metric(
                "Average Model Confidence",
                f"{avg_conf:.2f}%"
            )

            # Bar Chart: Breakdown
            counts = (
                results_df['Classification']
                .value_counts()
                .reset_index()
            )

            counts.columns = ['Classification', 'Count']

            fig_bar = px.bar(
                counts,
                x='Classification',
                y='Count',
                title="Detection Count by Type"
            )

            st.plotly_chart(fig_bar, use_container_width=True)

        # --- 4. DETAILED DATA TABLE ---
        with st.expander("📄 View Raw Detection Logs"):
            st.dataframe(results_df, use_container_width=True)