import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("flower_classification_model.keras")

model = load_model()

classes = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

st.title("🌸 Flower Classification App")

uploaded_file = st.file_uploader("Upload une image", type=["jpg","png","jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Image uploadée")

    st.write("⏳ Prédiction en cours...")

    # Préprocessing
    img = image.resize((180, 180))  # ⚠️ adapte si besoin
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # DEBUG
    st.write("Shape input :", img_array.shape)

    # Prédiction
    prediction = model.predict(img_array)

    st.write("Raw prediction :", prediction)

    predicted_class = classes[np.argmax(prediction)]
    confidence = np.max(prediction)

    st.success(f"🌼 Prédiction : {predicted_class}")
    st.write(f"Confiance : {confidence:.2f}")