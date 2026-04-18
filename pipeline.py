from core.query_normalizer import normalize_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval.local_kb import get_local_context
from retrieval.ranker import rank_context
from core.llm_engine import ask_llm
from core.validator import validate
from diagnostics.fallback_physics import physics_fallback


# =========================
# 🧠 INTELLIGENCE ENGINE
# =========================

def detect_intent(query):
    q = query.lower()

    if any(x in q for x in ["what is", "define", "explain", "describe"]):
        return "PROFESSOR"

    if any(x in q for x in ["why", "error", "fault", "not working", "heating", "failure"]):
        return "TECHNICIAN"

    if any(x in q for x in ["research", "compare", "analyze", "deep"]):
        return "RESEARCH"

    return "PROFESSOR"


def run_diagnostics(query):

    query = normalize_query(query)
    intent = detect_intent(query)

    # =========================
    # 📘 PROFESSOR MODE
    # =========================
    if intent == "PROFESSOR":

        prompt = f"""
You are a world-class Mechatronics professor.

Explain clearly and deeply.

Question:
{query}

Format:
Definition:
Core Principles:
Components:
Applications:
Real-world Example:
"""

        response = ask_llm(prompt)
        return validate(response, "📘 PROFESSOR MODE")


    # =========================
    # ⚙️ TECHNICIAN MODE
    # =========================

    web_results = search_web(query)

    web_context = []
    for r in web_results:
        text = extract_text(r["url"])
        if text and len(text) > 120:
            web_context.append(text)

    local_context = get_local_context(query)
    physics_context = physics_fallback(query)

    # SMART FUSION ENGINE
    if len(web_context) >= 2:
        combined_context = "\n".join(rank_context(web_context[:3]))
        mode = "🌐 WEB + TECHNICAL DATA"

    elif local_context:
        combined_context = local_context
        mode = "📚 LOCAL ENGINEERING KB"

    else:
        combined_context = physics_context
        mode = "⚙️ PHYSICS FALLBACK ENGINE"


    prompt = f"""
You are a senior Mechatronics diagnostics engineer.

Be precise and technical.

Context:
{combined_context}

Problem:
{query}

Format:
Diagnosis:
Root Cause:
Engineering Explanation:
Fix:
"""

    try:
        response = ask_llm(prompt)
    except:
        response = physics_context

    return validate(response, mode)
