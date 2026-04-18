def validate(text, mode):

    base = 60

    if "physics" in mode.lower():
        base = 75
    if "web" in mode.lower():
        base = 85

    weak_words = ["maybe", "possibly", "depends"]

    for w in weak_words:
        if w in text.lower():
            base -= 10

    return {
        "report": text,
        "confidence": max(base, 40),
        "mode": mode
    }
