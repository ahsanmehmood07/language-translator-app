import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Lingo — Translator", page_icon="🌐", layout="centered")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #1e1b3a 0%, #2d2a5e 100%);
}

.block-container {
    padding-top: 3rem;
    max-width: 680px;
}

.app-title {
    text-align: center;
    font-size: 2.3rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.2rem;
}

.app-subtitle {
    text-align: center;
    color: #a8a5c9;
    font-size: 0.95rem;
    margin-bottom: 2rem;
}

.stTextArea textarea {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #f0f0f5 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    font-size: 1rem !important;
}

.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: #f0f0f5 !important;
}

.stButton > button {
    background: #6c63ff !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6rem 1rem !important;
    transition: background 0.15s ease !important;
}

.stButton > button:hover {
    background: #574fd6 !important;
}

label, .stMarkdown p {
    color: #d8d8ee !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<p class="app-title">🌐 Lingo</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Translate text instantly across 100+ languages</p>', unsafe_allow_html=True)

# ---------- LANGUAGE DATA ----------
languages = GoogleTranslator().get_supported_languages(as_dict=True)
lang_names = sorted(list(languages.keys()))
lang_titles = [name.title() for name in lang_names]

# ---------- LANGUAGE DROPDOWNS ----------
col1, col2 = st.columns(2)

with col1:
    source_display = st.selectbox("From", ["Detect language"] + lang_titles, index=0)

with col2:
    target_display = st.selectbox("To", lang_titles, index=lang_titles.index("English"))

# ---------- INPUT ----------
input_text = st.text_area("Enter text", height=150, placeholder="Type or paste your text here...")

# ---------- TRANSLATE BUTTON ----------
translate_clicked = st.button("Translate", use_container_width=True)

# ---------- CODE-TO-NAME LOOKUP ----------
src_code = "auto" if source_display == "Detect language" else languages[source_display.lower()]
tgt_code = languages[target_display.lower()]

# ---------- TRANSLATION LOGIC ----------
if translate_clicked:
    if input_text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        try:
            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)
            st.code(translated, language=None)

            try:
                tts = gTTS(text=translated, lang=tgt_code)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes.getvalue(), format="audio/mp3")
            except Exception:
                pass

        except Exception as e:
            st.error(f"Translation failed: {e}")

# ---------- FOOTER ----------
st.markdown("<br>", unsafe_allow_html=True)
st.caption("Built with Streamlit · Google Translate Engine · Final Year AI Project")