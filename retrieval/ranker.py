def rank_context(blocks):
    scored = []

    keywords = [
        "motor", "heat", "torque",
        "current", "voltage", "sensor",
        "friction", "efficiency"
    ]

    for b in blocks:
        score = 0
        text = b.lower()

        for k in keywords:
            if k in text:
                score += 2

        # bonus for meaningful content length
        score += min(len(text.split()) / 100, 5)

        scored.append((score, b))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [b for _, b in scored[:3]]
