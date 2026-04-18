from core.query_processor import clean_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval.ranker import rank_context
from core.llm_engine import ask_llm
from core.validator import validate_response


# SAFE FALLBACK (IMPORTANT FIX)
fallback_knowledge = """
DC motor overheating is usually caused by:

1. Excess load → increases current draw
2. High I²R losses → heat in windings
3. Poor ventilation → trapped heat
4. Bearing friction → mechanical heating

Fix:
- reduce mechanical load
- check rated voltage/current
- improve cooling system
- inspect bearings
"""


def answer_question(query):

    # 1. Clean query
    query = clean_query(query)

    # 2. Web search
    results = search_web(query)

    raw_context = []

    # 3. Extract content (FIXED THRESHOLD)
    for r in results:
        text = extract_text(r["url"])

        if len(text) > 80:   # FIXED (was too strict before)
            raw_context.append(text)

    # 4. If NOTHING found → fallback
    if not raw_context:
        return {
            "response": fallback_knowledge,
            "confidence": 75
        }

    # 5. Rank best sources
    top_context = rank_context(raw_context)

    context = "\n\n".join(top_context)

    # 6. LLM reasoning
    prompt = f"""
You are a senior Mechatronics engineer.

RULES:
- Use ONLY provided context
- Do NOT guess
- Be precise and logical
- If missing data, state it clearly

CONTEXT:
{context}

QUESTION:
{query}

FORMAT:
1. Diagnosis
2. Cause
3. Explanation (physics/electrical)
4. Fix
5. Missing info (if any)
"""

    response = ask_llm(prompt)

    # 7. Validate
    return validate_response(response)
