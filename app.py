# 💡 Save this script as `app.py` and run with `streamlit run app.py`

import streamlit as st
from PIL import Image
import pytesseract
import re
import json
import os

# OCR Function
def extract_text(img):
    return pytesseract.image_to_string(img)

# Field Extraction
def extract_fields(text):
    fields = {
        "name": re.search(r"Name[:\-]?\s*(.*)", text),
        "dob": re.search(r"DOB[:\-]?\s*(.*)", text),
        "gender": re.search(r"Gender[:\-]?\s*(.*)", text),
        "aadhar_number": re.search(r"Aadhar No[:\-]?\s*([0-9 ]+)", text),
        "address": re.search(r"Address[:\-]?\s*(.*)", text)
    }
    return {key: (match.group(1).strip() if match else "Not Found") for key, match in fields.items()}

# Compliance Check
def run_compliance(data):
    checks = {
        "name_present": data["name"] != "Not Found",
        "dob_valid": bool(re.match(r"\d{2}/\d{2}/\d{4}", data["dob"])),
        "aadhar_valid": bool(re.match(r"\d{4} \d{4} \d{4}", data["aadhar_number"])),
        "address_ok": len(data["address"]) > 10
    }
    checks["compliance_passed"] = all(checks.values())
    return checks

# UI
st.title("🧾 AgentFlowAI – KYC Automation Demo")
uploaded_file = st.file_uploader("Upload a KYC Document (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Document", use_column_width=True)

    text = extract_text(image)
    st.subheader("📜 OCR Text")
    st.text(text)

    fields = extract_fields(text)
    st.subheader("📦 Extracted Fields")
    st.json(fields)

    report = run_compliance(fields)
    st.subheader("✅ Compliance Check")
    st.json(report)
