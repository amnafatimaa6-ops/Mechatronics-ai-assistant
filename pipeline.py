from core.query_normalizer import normalize_query
from retrieval.web_search import search_web
from retrieval.web_loader import extract_text
from retrieval.local_kb import get_local_context
from retrieval.ranker import rank_context
from core.llm_engine import ask_llm
from diagnostics.fallback_physics import physics_fallback


# =========================
# 🧠 INTENT DETECTION
# =========================
def detect_intent(query):
    q = query.lower()

    if any(x in q for x in ["what is", "define", "explain", "describe"]):
        return "PROFESSOR"

    if any(x in q for x in ["why", "fault", "error", "heating", "not working"]):
        return "TECHNICIAN"

    return "PROFESSOR"


# =========================
# 🛡 SAFE WEB PIPELINE
# =========================
def safe_web_context(query):
    try:
        results = search_web(query)

        texts = []
        for r in results[:3]:
            try:
                text = extract_text(r["url"])
                if text:
                    texts.append(text[:1200])
            except:
                continue

        return texts

    except:
        return []


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
    # 📘 PROFESSOR MODE
    # =========================
    if intent == "PROFESSOR":

        prompt = f"""
You are a Mechatronics professor.

Explain clearly:

{query}

Format:
Definition:
Core Concepts:
Applications:
"""

        try:
            answer = ask_llm(prompt)
        except:
            answer = "Mechatronics combines mechanical, electrical, and control systems."

        return {
            "answer": answer,
            "mode": "📘 PROFESSOR MODE",
            "confidence": 90,
            "sources": ["llm"]
        }

    # =========================
    # ⚙️ TECHNICIAN MODE
    # =========================

    web_context = safe_web_context(query)
    local_context = get_local_context(query)
    physics_context = physics_fallback(query)

    # -------------------------
    # CONTEXT DECISION ENGINE
    # -------------------------
    if len(web_context) >= 2:
        context = "\n".join(rank_context(web_context[:3]))
        mode = "🌐 WEB ENGINE"
        sources.append("web")

    elif local_context:
        context = local_context
        mode = "📚 LOCAL ENGINE"
        sources.append("local")

    else:
        context = physics_context
        mode = "⚙️ FALLBACK ENGINE"
        sources.append("physics")

    # -------------------------
    # LLM EXECUTION (SAFE)
    # -------------------------
    prompt = f"""
You are a senior Mechatronics engineer.

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
    # FINAL OUTPUT CONTRACT
    # =========================
    return {
        "answer": answer,
        "mode": mode,
        "confidence": 85 if "web" in sources else 70,
        "sources": sources
    }
