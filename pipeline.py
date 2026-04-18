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

    # 2. WEB LAYER (internet retrieval)
    web_results = search_web(query)

    web_context = []
    for r in web_results:
        text = extract_text(r["url"])
        if text and len(text) > 100:
            web_context.append(text)

    # 3. LOCAL KNOWLEDGE BASE
    local_context = get_local_context(query)

    # 4. PHYSICS FALLBACK (always available)
    physics_context = physics_fallback(query)

    # 5. CONTEXT FUSION (DECISION BRAIN)

    if web_context and len(web_context) >= 2:
        combined_context = "\n".join(rank_context(web_context[:3]))
        mode = "🌐 WEB + ENGINEERING DATA"

    elif local_context:
        combined_context = local_context
        mode = "📚 LOCAL ENGINEERING KB"

    else:
        combined_context = physics_context
        mode = "⚙️ PHYSICS FALLBACK ENGINE"

    # 6. ENGINEERING AI PROMPT
    prompt = f"""
You are a senior Mechatronics engineer.

RULES:
- Use ONLY the provided context
- Be precise and technical
- Explain using physics/electrical principles
- Do NOT guess outside context

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

    # 7. AI RESPONSE (SAFE + FREE MODEL WRAPPED IN llm_engine.py)
    try:
        response = ask_llm(prompt)
    except Exception:
        response = physics_context

    # 8. VALIDATION + CONFIDENCE SCORING
    result = validate(response, mode)

    return result
