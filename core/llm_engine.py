import requests
import time

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"


def ask_llm(prompt):

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250
        }
    }

    for attempt in range(2):  # retry system (VERY IMPORTANT)
        try:
            response = requests.post(API_URL, json=payload, timeout=25)
            data = response.json()

            # CASE 1: normal HF output
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]

            # CASE 2: model loading / error response
            if isinstance(data, dict) and "error" in data:
                time.sleep(2)
                continue

            # CASE 3: weird fallback response
            if isinstance(data, list):
                return str(data)

        except Exception:
            time.sleep(2)
            continue

    # FINAL FALLBACK (ONLY IF API FAILS)
    return generate_local_engineering_response(prompt)


def generate_local_engineering_response(prompt):
    return """
MECHATRONICS ENGINEERING EXPLANATION

Mechatronics is an interdisciplinary field combining:

- Mechanical Engineering (structure, motion, dynamics)
- Electrical Engineering (circuits, power systems)
- Control Systems (feedback loops, PID control)
- Computer Science (automation, embedded systems)

Applications include:
- Robotics
- CNC machines
- Autonomous systems
- Smart manufacturing

This system is currently operating in offline reasoning mode.
"""
