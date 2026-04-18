import streamlit as st
from pipeline import answer_question

st.set_page_config(page_title="Mechatronics AI System", layout="wide")

st.title("⚙️ Mechatronics AI Diagnostic System")
st.write("Engineering assistant for motors, torque, sensors, robotics")

query = st.text_input("💬 Enter your engineering problem")

if query:
    result = answer_question(query)

    st.markdown("## 🧠 Diagnosis")
    st.write(result["response"])

    st.markdown("## 📊 Confidence")
    st.progress(result["confidence"])
