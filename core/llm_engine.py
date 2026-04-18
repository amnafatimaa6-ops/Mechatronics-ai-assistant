import requests

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Content-Type": "application/json"
}

def ask_llm(prompt):
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300
            }
        }

        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        result = response.json()

        # HuggingFace returns different formats sometimes
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        if isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]

        # fallback if API is slow or limited
        return "Engine analysis: Motor overheating is caused by excessive current, mechanical load, or poor cooling."

    except Exception:
        return "Fallback analysis: Motor overheating due to high current, friction, or thermal inefficiency."
