def validate(text, mode):

    base = 60

    # boost confidence if web is involved
    if "WEB" in mode:
        base = 85
    elif "LOCAL" in mode:
        base = 70
    else:
        base = 75

    weak_signals = ["maybe", "possibly", "could be", "fallback"]

    for w in weak_signals:
        if w in text.lower():
            base -= 10

    return {
        "report": text,
        "confidence": max(base, 40),
        "mode": mode
    }
