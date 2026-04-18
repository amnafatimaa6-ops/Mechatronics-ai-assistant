import streamlit as st
from pipeline import run_diagnostics

st.title("⚙️ Mechatronics AI System (Production)")

query = st.text_input("Enter system issue")

if query:
    result = run_diagnostics(query)

    st.markdown("## 🧠 Answer")
    st.write(result["answer"])

    st.markdown("## 📊 Confidence")
    st.progress(result["confidence"])

    st.markdown("## 📄 Mode")
    st.write(result["mode"])

    st.markdown("## 🔎 Sources")
    st.write(", ".join(result["sources"]))
