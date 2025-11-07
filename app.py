# ================================================================
# Chatbot Asta UX Dark Theme + Streaming Respons Gemini
# ================================================================

import os
import streamlit as st
import google.generativeai as genai
from pathlib import Path

# ---------------------- Konfigurasi ----------------------------
st.set_page_config(page_title="Chatbot Asta", page_icon="💬", layout="wide")

st.title("💬 Chatbot Asta ")

# ================= Sidebar =================
st.sidebar.title("⚙️ Kontrol Asta Chatbot")

# Gambar Asta di sidebar
asta_img_path = r"C:\UTS\Asta.png"
if Path(asta_img_path).exists():
    st.sidebar.image(asta_img_path, caption="Asta Chatbot", width="stretch")

# ================= Input API Key =================
api_key_input = st.sidebar.text_input(
    "Masukkan GEMINI API Key",
    type="password",
    placeholder="PASTE_KEY_KAMU"
)

if api_key_input:
    API_KEY = api_key_input.strip()
    genai.configure(api_key=API_KEY)
else:
    API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    if not API_KEY:
        st.sidebar.error("❌ API Key belum diset. Masukkan di atas atau di environment variable.")
        st.stop()

# Pilihan Gaya Bahasa
gaya_bahasa = st.sidebar.radio("Gaya Bahasa", ["Santai", "Humoris", "Formal"], index=0)

# Tombol Reset Chat
if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.messages = []
    st.session_state.user_budget = None
    st.warning("Chat direset. Silakan ketik pesan baru di input bawah.")

# ================= Setup Gemini =================
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if not API_KEY:
    st.sidebar.error("❌ API Key belum diset")
    st.stop()

genai.configure(api_key=API_KEY)
GMODEL = genai.GenerativeModel("models/gemini-2.0-flash")

# ================= State Chat =================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Halo! Asta di sini 👋. Ada yang bisa aku bantu hari ini?"
    }]

# ================= Tampilkan riwayat chat =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= Input User =================
user_input = st.chat_input("Tulis pesan kamu di sini...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ================= Prompt Gemini =================
    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-10:]])

    prompt = f"""
    Kamu adalah Asta, asisten AI serba bisa.
    Gaya bahasa: {gaya_bahasa} (formal/humoris/santai sesuai pilihan).
    Riwayat percakapan:
    {context}
    
    Jawab pesan terakhir user secara natural dan sesuai gaya bahasa yang dipilih.
    Sertakan emoji secukupnya jika santai atau humoris, jangan berlebihan jika formal.
    """

    # ================= Streaming Generate =================
    placeholder = st.empty()
    full_text = ""
    try:
        for event in GMODEL.generate_content(prompt, stream=True):
            chunk = getattr(event, "text", "")
            full_text += chunk
            placeholder.markdown(full_text)
    except Exception as e:
        full_text = f"⚠️ Server sibuk atau kuota habis. Coba lagi sebentar 😅\n\nDetail: {e}"
        placeholder.markdown(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})