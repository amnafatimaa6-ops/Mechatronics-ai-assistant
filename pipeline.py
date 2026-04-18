from core.query_processor import clean_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval.ranker import rank_context
from core.llm_engine import ask_llm
from core.validator import validate_response


def answer_question(query):

    # 1. Clean query
    query = clean_query(query)

    # 2. Web search
    results = search_web(query)

    # 3. Extract content
    raw_context = []

    for r in results:
        text = extract_text(r["url"])
        if len(text) > 300:
            raw_context.append(text)

    if not raw_context:
        return {
            "response": "Not enough reliable engineering data found.",
            "confidence": 0
        }

    # 4. Rank best sources
    top_context = rank_context(raw_context)

    context = "\n\n".join(top_context)

    # 5. LLM reasoning
    prompt = f"""
You are a senior Mechatronics diagnostic engineer.

RULES:
- Use ONLY given context
- No guessing
- Be precise and logical
- If missing info, say what is needed

CONTEXT:
{context}

QUESTION:
{query}

FORMAT:
1. Diagnosis
2. Root Cause
3. Engineering Explanation
4. Fix
5. Missing Data (if any)
"""

    response = ask_llm(prompt)

    # 6. Validate output
    return validate_response(response)
