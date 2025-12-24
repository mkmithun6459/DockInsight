import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
from PIL import Image
import pytesseract
import io
load_dotenv()

# ===============================
# CONFIGURATION
# ===============================

# 🔴 PASTE YOUR GEMINI API KEY HERE
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a model that works with your SDK
model = genai.GenerativeModel("models/gemini-2.5-flash")

# 🔴 WINDOWS USERS: Update this path if needed
#pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mithun\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe"
# ===============================
# STREAMLIT UI
# ===============================

st.set_page_config(page_title="DocInsight", layout="centered")

st.title("📄 DocInsight")
st.write(
    "Upload a **PDF or image**, or paste text below. "
    "The system will generate a **summary** and **key insights**."
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload a PDF or Image (PNG/JPG)",
    type=["pdf", "png", "jpg", "jpeg"]
)

# Text area (fallback)
document_text = st.text_area(
    "Or paste document text here",
    height=250
)

# ===============================
# HELPER FUNCTION
# ===============================

def extract_text_from_file(file):
    extracted_text = ""

    # PDF handling
    if file.type == "application/pdf":
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

    # Image handling
    else:
        image = Image.open(file)
        extracted_text = pytesseract.image_to_string(image)

    return extracted_text.strip()

# ===============================
# ANALYSIS BUTTON
# ===============================

if st.button("Analyze Document"):
    final_text = ""

    if uploaded_file is not None:
        final_text = extract_text_from_file(uploaded_file)
    else:
        final_text = document_text.strip()

    if final_text == "":
        st.warning("Please upload a document or paste some text.")
    else:
        prompt = f"""
        Analyze the following document and provide:

        1. A short, clear summary (3–4 lines)
        2. Key insights or important points in bullet form

        Document:
        {final_text}
        """

        with st.spinner("Analyzing document..."):
            response = model.generate_content(prompt)

        st.subheader("📌 Summary & Key Insights")
        st.write(response.text)

# ===============================
# FOOTER
# ===============================

st.markdown("---")
st.caption(
    "⚙️ Powered by Google Gemini | MVP for DocInsight"
)


