from core.query_normalizer import normalize_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval.local_kb import get_local_context
from retrieval.ranker import rank_context
from core.llm_engine import ask_llm
from diagnostics.fallback_physics import physics_fallback


# =========================
# 🧠 INTENT ENGINE
# =========================
def detect_intent(query):
    q = query.lower()

    if any(x in q for x in ["what is", "define", "explain", "describe"]):
        return "PROFESSOR"

    if any(x in q for x in ["why", "fault", "error", "heating", "not working"]):
        return "TECHNICIAN"

    return "PROFESSOR"


# =========================
# ⚙️ MAIN PIPELINE
# =========================
def run_diagnostics(query):

    query = normalize_query(query)
    intent = detect_intent(query)

    sources = []
    context = ""
    mode = ""

    # =========================
    # 📘 KNOWLEDGE MODE
    # =========================
    if intent == "PROFESSOR":

        prompt = f"""
You are a Mechatronics professor.

Explain clearly and structured.

Topic:
{query}

Format:
Definition:
Core Concepts:
Components:
Applications:
"""

        answer = ask_llm(prompt)

        return {
            "mode": "📘 PROFESSOR MODE",
            "answer": answer,
            "confidence": 90,
            "sources": ["llm"]
        }

    # =========================
    # ⚙️ DIAGNOSTIC MODE
    # =========================

    web_results = search_web(query)

    web_context = []
    for r in web_results:
        text = extract_text(r["url"])
        if text and len(text) > 120:
            web_context.append(text)

    local_context = get_local_context(query)
    physics_context = physics_fallback(query)

    # =========================
    # 🧠 CONTEXT DECISION ENGINE
    # =========================
    if len(web_context) >= 2:
        context = "\n".join(rank_context(web_context[:3]))
        mode = "🌐 WEB MODE"
        sources.append("web")

    elif local_context:
        context = local_context
        mode = "📚 LOCAL MODE"
        sources.append("local")

    else:
        context = physics_context
        mode = "⚙️ FALLBACK MODE"
        sources.append("physics")

    # =========================
    # 🤖 LLM EXECUTION
    # =========================
    prompt = f"""
You are a senior Mechatronics engineer.

Be precise.

Context:
{context}

Problem:
{query}

Format:
Diagnosis:
Root Cause:
Fix:
"""

    try:
        answer = ask_llm(prompt)
        sources.append("llm")
    except:
        answer = physics_context

    # =========================
    # 📦 STRICT OUTPUT CONTRACT
    # =========================
    return {
        "mode": f"⚙️ {mode}",
        "answer": answer,
        "confidence": 85 if "web" in sources else 70,
        "sources": sources
    }
