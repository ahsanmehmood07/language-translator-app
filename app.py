import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="centered")

st.markdown("""
    <style>
    .main-title {text-align:center;font-size:2.3rem;font-weight:700;color:#2E86AB;margin-bottom:0px;}
    .subtitle {text-align:center;color:gray;margin-bottom:30px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌐 Language Translator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Translate text instantly between multiple languages</p>', unsafe_allow_html=True)

languages = GoogleTranslator().get_supported_languages(as_dict=True)
lang_names = list(languages.keys())

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From (Source Language)", ["auto"] + lang_names, index=0)
with col2:
    target_lang = st.selectbox("To (Target Language)", lang_names, index=lang_names.index("english"))

input_text = st.text_area("Enter text to translate:", height=150, placeholder="Type or paste your text here...")

translate_btn = st.button("🔄 Translate", use_container_width=True)

if translate_btn:
    if input_text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        try:
            src_code = "auto" if source_lang == "auto" else languages[source_lang]
            tgt_code = languages[target_lang]

            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)

            st.success("Translation complete!")
            st.text_area("Translated Text:", value=translated, height=150)
            st.code(translated, language=None)

            try:
                tts = gTTS(text=translated, lang=tgt_code)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                st.audio(audio_bytes.getvalue(), format="audio/mp3")
            except Exception:
                st.info("Voice output not available for this language.")

        except Exception as e:
            st.error(f"Translation failed: {e}")

st.markdown("---")
st.caption("Built with Streamlit & Google Translate Engine")