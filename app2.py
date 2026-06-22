import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import time
import os

# ========================
# CONFIG PAGE
# ========================
st.set_page_config(
    page_title="Flower AI 🌸",
    page_icon="🌸",
    layout="centered"
)

# ========================
# STYLE CSS
# ========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
}
.pred-box {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ========================
# LOAD MODEL (robust)
# ========================
MODEL_PATH = "flower_classification_model.keras"

if not os.path.exists(MODEL_PATH):
    st.error(f"Model file not found at '{MODEL_PATH}'. Place the model in the app folder.")

if hasattr(st, "cache_resource"):
    @st.cache_resource
    def load_model():
        try:
            return tf.keras.models.load_model(MODEL_PATH)
        except Exception as e:
            st.error(f"Error loading model: {e}")
            raise
else:
    @st.cache(allow_output_mutation=True)
    def load_model():
        try:
            return tf.keras.models.load_model(MODEL_PATH)
        except Exception as e:
            st.error(f"Error loading model: {e}")
            raise

model = load_model()

classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

# ========================
# SIDEBAR
# ========================
st.sidebar.title("🌸 Flower AI")
st.sidebar.write("Upload une image pour classifier la fleur.")
st.sidebar.info("Modèle CNN entraîné sur 5 classes.")

# ========================
# HEADER
# ========================
st.markdown("<h1 style='text-align: center;'>🌸 Flower Classification App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI qui reconnaît les fleurs</p>", unsafe_allow_html=True)

# ========================
# UPLOAD
# ========================
uploaded_file = st.file_uploader("📤 Upload une image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    # Card image
    st.markdown("<div class='pred-box'>", unsafe_allow_html=True)
    st.image(image, caption="Image uploadée", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bouton prédiction
    if st.button("🔍 Lancer la prédiction"):
        with st.spinner("Analyse en cours... ⏳"):
            time.sleep(1)  # effet visuel

            img = image.resize((180, 180)) # redimensionner l'image donnee 
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array) # utiliser le modelempour predire 
            predicted_class = classes[np.argmax(prediction)]
            confidence = np.max(prediction)
        # Résultat
        st.markdown("<div class='pred-box'>", unsafe_allow_html=True)
        st.success(f"🌼 {predicted_class}")
        st.write(f"Confiance : {confidence:.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Probabilités
        st.subheader("📊 Probabilités")
        probs = prediction[0]

        prob_dict = {classes[i]: float(probs[i]) for i in range(len(classes))}
        st.bar_chart(prob_dict)