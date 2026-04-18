def validate_response(text):
    weak_phrases = [
        "maybe", "possibly", "could be",
        "it depends", "not sure"
    ]

    confidence = 100

    for w in weak_phrases:
        if w in text.lower():
            confidence -= 10

    confidence = max(confidence, 40)

    return {
        "response": text,
        "confidence": confidence
    }
