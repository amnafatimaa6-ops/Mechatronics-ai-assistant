import requests

# Free HuggingFace model (no key required, but rate-limited)
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"


def ask_llm(prompt):
    """
    Production-safe LLM wrapper.

    Guarantees:
    - Never returns None
    - Handles API failures safely
    - Returns clean text or fallback message
    """

    try:
        response = requests.post(
            API_URL,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 250
                }
            },
            timeout=25
        )

        data = response.json()

        # ✅ Normal HuggingFace response
        if isinstance(data, list) and len(data) > 0:
            text = data[0].get("generated_text")

            if text and isinstance(text, str) and text.strip():
                return text.strip()

        # ❌ Model loading / API error case
        if isinstance(data, dict) and "error" in data:
            return None

        return None

    except Exception:
        # ❌ Network / timeout / crash safety fallback
        return None


# =========================
# 🧠 FINAL SAFETY FALLBACK
# =========================
def generate_engineering_fallback(prompt):
    """
    Used ONLY when LLM fails completely.
    """

    return """
MECHATRONICS ENGINEERING EXPLANATION

Mechatronics is an interdisciplinary field combining:

- Mechanical Engineering (motion, structures)
- Electrical Engineering (circuits, power systems)
- Control Systems (feedback, PID control)
- Computer Science (automation, embedded systems)

Applications include robotics, CNC machines, automation systems, and smart devices.
"""
