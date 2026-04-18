def rank_context(blocks):
    scored = []

    for b in blocks:
        score = 0

        if "motor" in b.lower():
            score += 3
        if "torque" in b.lower():
            score += 3
        if "heat" in b.lower():
            score += 2
        if "sensor" in b.lower():
            score += 2

        scored.append((score, b))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [b for _, b in scored[:3]]
