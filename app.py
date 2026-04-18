import streamlit as st
from pipeline import run_diagnostics

st.set_page_config(page_title="Industrial Mechatronics AI", layout="wide")

st.title("⚙️ Mechatronics Diagnostic System v4 (Industrial Grade)")
st.write("Hybrid AI system for engineering fault analysis")

query = st.text_input("Enter system issue")

if query:
    result = run_diagnostics(query)

    st.markdown("## 🧠 Engineering Diagnosis")
    st.write(result["report"])

    st.markdown("## 📊 Confidence Score")
    st.progress(int(result["confidence"]))

    st.markdown("## 📄 System Mode")
    st.write(result["mode"])
