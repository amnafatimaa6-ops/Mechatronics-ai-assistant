def normalize_query(q):
    q = q.lower()

    if "motor heating" in q:
        return "dc motor overheating thermal analysis current torque loss"

    if "low torque" in q:
        return "torque loss dc motor mechanical electrical causes"

    return q
