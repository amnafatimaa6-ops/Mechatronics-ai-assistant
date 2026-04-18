def fuse_contexts(web, local, fallback):

    score_web = len(web)
    score_local = len(local)
    score_fb = len(fallback)

    # Weighted decision system
    if score_web > 2:
        mode = "WEB + LOCAL HYBRID"
        context = "\n".join(web[:3]) + "\n" + local

    elif score_local > 0:
        mode = "LOCAL ENGINEERING KB"
        context = local

    else:
        mode = "PHYSICS FALLBACK ENGINE"
        context = fallback

    return context, mode
