def clean_query(query: str) -> str:
    query = query.lower().strip()

    mappings = {
        "motor hot": "dc motor overheating causes thermal analysis",
        "low torque": "torque loss in dc motor reasons engineering",
        "sensor error": "sensor noise calibration robotics issues"
    }

    for key, value in mappings.items():
        if key in query:
            return value

    return query
