import streamlit as st
from pipeline import run_diagnostics

st.set_page_config(page_title="Mechatronics AI", layout="centered")

st.title("⚙️ Mechatronics AI System (Bulletproof v6)")

query = st.text_input("Enter system issue")

if query:

    try:
        result = run_diagnostics(query)

        st.markdown("## 🧠 Answer")
        st.write(result["answer"])

        st.markdown("## 📊 Confidence")
        st.progress(result["confidence"])

        st.markdown("## 📄 Mode")
        st.write(result["mode"])

        st.markdown("## 🔎 Sources")
        st.write(", ".join(result["sources"]))

    except Exception as e:
        st.error("System error occurred")
        st.write(str(e))
