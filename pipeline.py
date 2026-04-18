from core.query_normalizer import normalize_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval.local_kb import get_local_context
from retrieval.ranker import rank_context
from core.llm_engine import ask_llm
from core.validator import validate
from diagnostics.fallback_physics import physics_fallback


def run_diagnostics(query):

    # 1. Normalize query (makes search smarter)
    query = normalize_query(query)

    # 2. WEB LAYER (FREE INTERNET DATA)
    web_results = search_web(query)

    web_context = []
    for r in web_results:
        text = extract_text(r["url"])
        if text and len(text) > 100:
            web_context.append(text)

    # 3. LOCAL KNOWLEDGE BASE (FAST + RELIABLE)
    local_context = get_local_context(query)

    # 4. PHYSICS FALLBACK (ALWAYS AVAILABLE)
    physics_context = physics_fallback(query)

    # 5. CONTEXT FUSION (DECIDES WHAT TO USE)
    combined_context = ""

    if len(web_context) > 0:
        combined_context += "\n".join(rank_context(web_context[:3]))
        mode = "WEB + ENGINEERING DATA"

    elif len(local_context) > 0:
        combined_context += local_context
        mode = "LOCAL ENGINEERING KB"

    else:
        combined_context += physics_context
        mode = "PHYSICS FALLBACK ENGINE"

    # 6. ENGINEERING PROMPT (IMPORTANT FOR QUALITY)

    prompt = f"""
You are a senior Mechatronics engineer.

Provide structured technical diagnosis.

RULES:
- Use ONLY provided context
- Be precise and logical
- Use physics/electrical reasoning
- No vague answers

CONTEXT:
{combined_context}

PROBLEM:
{query}

FORMAT:
Diagnosis:
Root Cause:
Engineering Explanation:
Fix:
"""

    # 7. AI ENGINE (FREE HF MODEL VIA llm_engine.py)
    try:
        raw = ask_llm(prompt)
    except Exception:
        raw = physics_context

    # 8. VALIDATION + CONFIDENCE SCORING
    result = validate(raw, mode)

    return result
