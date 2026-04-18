def validate_response(text):
    weak_phrases = [
        "maybe", "possibly", "could be",
        "it depends", "not sure"
    ]

    confidence = 100

    for phrase in weak_phrases:
        if phrase in text.lower():
            confidence -= 10

    confidence = max(confidence, 20)

    return {
        "response": text,
        "confidence": confidence
    }
