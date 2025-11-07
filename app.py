import os
import streamlit as st
import google.generativeai as genai
from pathlib import Path

# ---------------------- Konfigurasi UI ----------------------------
st.set_page_config(page_title="Chatbot Asta", page_icon="💬", layout="wide")
st.title("💬 Chatbot Asta")

# ================= Sidebar =================
st.sidebar.title("⚙️ Kontrol Asta Chatbot")

# Gambar Asta opsional
asta_img_path = r"C:\UTS\Asta.png"
if Path(asta_img_path).exists():
    st.sidebar.image(asta_img_path, caption="Asta Chatbot", width=150)

# ================= API Key Langsung =================
API_KEY = "AIzaSyDTktXRrngdKy2yLfhsDdMBloH-38AqY5U"  # Ganti dengan key asli kamu
genai.configure(api_key=API_KEY)

# ================= Mode Peran =================
role = st.sidebar.selectbox("🎭 Pilih Mode Peran Asta:", [
    "Teman Santai",
    "Humoris",
    "Guru Sabar",
    "Motivator",
    "Penjelas Teknis"
])

# ================= Reset Chat =================
if st.sidebar.button("🔄 Reset Percakapan"):
    st.session_state.messages = []

# ================= Setup Model =================
GMODEL = genai.GenerativeModel("models/gemini-2.0-flash")

# ================= State Chat =================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Halo! Asta siap membantu 🚀"
    }]

# ================= Tampilkan Chat =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= Input User =================
user_input = st.chat_input("Tulis pesan di sini...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ====== Prompt Berbasis Peran ======
    prompts = {
        "Teman Santai": "Gunakan bahasa santai, hangat, nyaman, seperti ngobrol dengan sahabat.",
        "Humoris": "Gunakan humor ringan, lucu, tapi tetap relevan.",
        "Guru Sabar": "Gunakan penjelasan runtut, sabar, dan tidak menggurui.",
        "Motivator": "Gunakan kata-kata penyemangat, empati, dan dorongan positif.",
        "Penjelas Teknis": "Jelaskan detail teknis dengan struktur jelas dan contoh."
    }

    system_instruction = prompts[role]

    context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-10:]])

    final_prompt = f"""
    Kamu bernama Asta, asisten AI.
    Peran yang harus kamu gunakan: **{role}**
    Instruksi gaya: {system_instruction}

    Riwayat percakapan:
    {context}

    Jawab pesan terakhir user secara alami dan relevan.
    """

    # ============= Streaming Response =============
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        try:
            for event in GMODEL.generate_content(final_prompt, stream=True):
                chunk = getattr(event, "text", "")
                full_text += chunk
                placeholder.markdown(full_text)
        except Exception as e:
            full_text = f"⚠️ Terjadi kendala.\n\nDetail: {e}"
            placeholder.markdown(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})