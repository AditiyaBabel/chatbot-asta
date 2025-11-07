import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.0-flash")
resp = model.generate_content("Halo! Tes koneksi Gemini API.")
print(resp.text)