import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"


def ask_llm(prompt):

    try:
        response = requests.post(
            API_URL,
            json={"inputs": prompt},
            timeout=20
        )

        data = response.json()

        # VALID RESPONSE
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        # MODEL LOADING CASE (IMPORTANT FIX)
        if isinstance(data, dict) and "error" in data:
            return None

        return None

    except:
        return None
