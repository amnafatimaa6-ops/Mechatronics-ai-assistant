def clean_query(query: str) -> str:
    query = query.lower().strip()

    mappings = {
        "motor heating": "dc motor overheating causes thermal analysis current torque heat",
        "motor hot": "dc motor overheating reasons thermal failure",
        "low torque": "torque loss dc motor causes engineering analysis",
        "sensor error": "sensor noise calibration robotics issues"
    }

    for k, v in mappings.items():
        if k in query:
            return v

    return query
