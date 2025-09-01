import streamlit as st
import pickle
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

st.title("📝 AI Research Abstract Generator")

# Load model + tokenizer from .pkl
@st.cache_resource
def load_model():
    with open("ai_abstract_generator.pkl", "rb") as f:
        saved = pickle.load(f)
    return saved["model"], saved["tokenizer"]

model, tokenizer = load_model()

# User input
topic = st.text_input("Enter your research topic:")

if st.button("Generate Abstract"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        # Encode input
        inputs = tokenizer.encode(topic, return_tensors="pt")
        # Generate abstract
        outputs = model.generate(
            inputs,
            max_length=150,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        abstract = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.subheader("Generated Abstract:")
        st.write(abstract)