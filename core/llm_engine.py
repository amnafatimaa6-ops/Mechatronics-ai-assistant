import requests

def ask_llm(prompt):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-base",
            json={"inputs": prompt},
            timeout=20
        )

        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        return str(data)

    except:
        return "Engineering analysis: system operating under fallback reasoning mode."
