import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"


def ask_llm(prompt):
    """
    Bulletproof LLM wrapper:
    - Uses free HuggingFace inference
    - Handles API failures safely
    - Never crashes pipeline
    """

    try:
        response = requests.post(
            API_URL,
            json={"inputs": prompt},
            timeout=20
        )

        data = response.json()

        # ✅ Case 1: Normal successful response
        if isinstance(data, list) and len(data) > 0:
            if "generated_text" in data[0]:
                return data[0]["generated_text"]

        # ❌ Case 2: Model loading / API error
        if isinstance(data, dict) and "error" in data:
            return None

        # ❌ Case 3: Unexpected format
        return None

    except Exception:
        # ❌ Network failure fallback
        return None
