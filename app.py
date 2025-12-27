import streamlit as st
import pandas as pd
import joblib

# -------------------------------
# Load the pre-trained model & artifacts
# -------------------------------
model, scaler, expected_columns = None, None, []

try:
    model = joblib.load("randomforestmodel.pkl")
    scaler = joblib.load("scaler.pkl")
    expected_columns = joblib.load("columns.pkl")
    st.success("✅ Artifacts loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading artifacts: {e}")
    expected_columns = ["feature1", "feature2", "feature3"]

# -------------------------------
# App UI
# -------------------------------
st.set_page_config(page_title="Vehicle Performance Prediction", page_icon="🚗", layout="centered")

st.title("🚗 Vehicle Performance Prediction App")
st.markdown("---")

st.header("📊 Enter Vehicle Data")
user_input = {}
cols = st.columns(len(expected_columns))
for i, col in enumerate(expected_columns):
    with cols[i]:
        user_input[col] = st.number_input(f"{col}", value=0.0)

input_df = pd.DataFrame([user_input])

st.write("### 🔎 Input Data Preview")
st.dataframe(input_df, use_container_width=True)

# -------------------------------
# Prediction Button
# -------------------------------
st.markdown("---")
if st.button("🚀 Predict Performance"):
    if model is not None and scaler is not None:
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)

        # Map numeric prediction to labels
        label_map = {
            0: ("Low Performance", "#8B0000"),     # Dark Red
            1: ("Medium Performance", "#FF8C00"),  # Dark Orange
            2: ("High Performance", "#006400")     # Dark Green
        }
        pred_label, bg_color = label_map.get(prediction[0], ("Unknown", "#333333"))

        # Styled output card with darker colors
        st.markdown(
            f"""
            <div style="background-color:{bg_color};
                        padding:20px;
                        border-radius:10px;
                        text-align:center;
                        font-size:22px;
                        color:white;">
                🎯 <b>Predicted Performance:</b> {pred_label}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Model not available, showing input only.")
