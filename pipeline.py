from core.query_normalizer import normalize_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval import local_kb
from diagnostics.fallback_physics import physics_fallback
from core.fusion_engine import fuse_contexts
from core.llm_engine import ask_llm
from core.validator import validate


def run_diagnostics(query):

    query = normalize_query(query)

    # 1. WEB LAYER
    web_results = search_web(query)
    web_context = []

    for r in web_results:
        text = extract_text(r["url"])
        if len(text) > 100:
            web_context.append(text)

    # 2. LOCAL KB
    local_context = get_local_context(query)

    # 3. FALLBACK ENGINE
    physics_context = physics_fallback(query)

    # 4. FUSION (MOST IMPORTANT PART)
    context, mode = fuse_contexts(web_context, local_context, physics_context)

    # 5. LLM REASONING
    prompt = f"""
You are a senior industrial Mechatronics diagnostic engineer.

Rules:
- Use ONLY given context
- Be precise, no guessing
- Always explain using physics/electrical laws

Context:
{context}

Problem:
{query}

Format:
Diagnosis:
Root Cause:
Engineering Analysis:
Fix:
Missing Parameters:
"""

    raw = ask_llm(prompt)

    # 6. VALIDATION
    return validate(raw, mode)
