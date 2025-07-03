import streamlit as st
from transformers import pipeline, set_seed

# --- Custom CSS for vibrant pastel gradient, creative look, and emoji enhancements ---
st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(135deg, #fffbe7 0%, #ffe5ec 30%, #b7f9c2 65%, #ffe7c7 100%);
        /* pastel yellow: #fffbe7, pastel pink: #ffe5ec, pastel green: #b7f9c2, pastel orange: #ffe7c7 */
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        color: #22223b;
        font-size: 1.15rem;
    }
    .main {
        background-color: #fffbe7;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 24px 0 rgba(160, 120, 240, 0.08);
    }
    .stTextInput>div>div>input {
        background: #f6eaff;
        border-radius: 10px;
        color: #22223b;
        font-size: 1.1rem;
        border: 1.5px solid #ffb347;
        box-shadow: none;
        outline: none;
        transition: border 0.2s;
    }
    .stTextInput>div>div>input:focus, .stTextInput>div>div>input:active {
        background: #ffe5ec !important;
        color: #22223b !important;
        border: 2px solid #7b2ff2;
        box-shadow: 0 0 0 2px #b7f9c2;
    }
    .stTextInput>div>div>input::selection {
        background: #ffe7c7;
        color: #22223b;
    }
    /* Custom selectbox styling to remove white highlight and use pastel theme */
    .stSelectbox>div>div {
        background: #f6eaff !important;
        border-radius: 10px !important;
        border: 1.5px solid #ffb347 !important;
        color: #22223b !important;
        font-size: 1.1rem !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .stSelectbox>div>div:focus, .stSelectbox>div>div:active {
        background: #ffe5ec !important;
        color: #22223b !important;
        border: 2px solid #7b2ff2 !important;
        box-shadow: 0 0 0 2px #b7f9c2 !important;
        outline: none !important;
    }
    .stSelectbox>div>div>div>div {
        color: #22223b !important;
        background: #f6eaff !important;
        font-size: 1.1rem !important;
    }
    .stSelectbox>div>div>div>div:focus, .stSelectbox>div>div>div>div:active {
        background: #ffe5ec !important;
        color: #22223b !important;
    }
    .stSelectbox>div>div>div>div::selection {
        background: #ffe7c7 !important;
        color: #22223b !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ffb347 0%, #b7f9c2 100%);
        color: #22223b;
        border-radius: 16px;
        font-weight: bold;
        font-size: 1.18rem;
        padding: 0.8rem 2.5rem;
        border: none;
        box-shadow: 0 2px 12px 0 rgba(255, 182, 193, 0.13);
        transition: all 0.2s cubic-bezier(.4,0,.2,1);
        letter-spacing: 0.04em;
        outline: none;
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    .stButton>button:hover, .stButton>button:focus {
        background: linear-gradient(90deg, #b7f9c2 0%, #ffb347 100%);
        color: #fff;
        transform: translateY(-2px) scale(1.07);
        box-shadow: 0 4px 18px 0 rgba(123, 47, 242, 0.15);
        outline: none;
    }
    .story-card {
        background: #fff0f6;
        border-radius: 18px;
        padding: 1.7rem;
        margin-top: 1.7rem;
        box-shadow: 0 2px 14px 0 rgba(255, 182, 193, 0.13);
        animation: fadeIn 1.2s;
    }
    .story-card h3, .story-card p {
        color: #22223b;
        font-size: 1.22rem;
    }
    label, .css-1cpxqw2, .css-1y4p8pa, .css-1n76uvr, .css-1v0mbdj, .css-1y4p8pa, .css-1n76uvr {
        color: #22223b !important;
        font-size: 1.13rem !important;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px);}
        to { opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# --- Streamlit App ---
st.markdown("<h1 style='text-align: center; color: #7b2ff2; font-size: 2.8rem;'>Kahani-AI ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #22223b; font-size: 1.25rem;'>Let your imagination bloom! Enter a prompt and watch your story unfold.</p>", unsafe_allow_html=True)

@st.cache_resource
def load_generator(model_name):
    return pipeline('text-generation', model=model_name)

MODEL_OPTIONS = [
    ("gpt2-large", "GPT-2 Large 📝"),
    ("distilgpt2", "DistilGPT-2 ⚡")
]
model_labels = [label for _, label in MODEL_OPTIONS]
model_name = st.selectbox("Choose a model: 🤖", model_labels)
model_id = dict(zip(model_labels, [m for m, _ in MODEL_OPTIONS]))[model_name]

length = st.selectbox("Story length: 📏", ["Short", "Medium", "Long"])
length_map = {"Short": 200, "Medium": 350, "Long": 450}
max_length = length_map[length]

prompt = st.text_input("Your story prompt: ✍️", "")

if st.button("✨ Generate Story ✨"):
    if prompt.strip():
        set_seed(42)
        generator = load_generator(model_id)
        with st.spinner("🌸 Weaving your story..."):
            story = generator(
                prompt,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.9,
                pad_token_id=50256
            )[0]['generated_text']
        st.markdown(f"<div class='story-card'><h3>📖 Your AI-Generated Story:</h3><p>{story}</p></div>", unsafe_allow_html=True)
        st.download_button("⬇️ Download Story", story, file_name="story.txt")
    else:
        st.warning("Please enter a prompt to generate a story.")

st.markdown("<p style='text-align:center; color:#b983ff; font-size:0.95rem;'>Made with 💜 and 🤗 HuggingFace Transformers</p>", unsafe_allow_html=True) 