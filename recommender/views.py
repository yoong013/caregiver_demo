# recommender/views.py
from django.shortcuts import render
from .retriever import get_recommendations

def recommend(request):
    result = None
    error  = None

    if request.method == "POST":
        # 1) grab the POSTed text, default to empty string if missing
        condition = request.POST.get("query", "").strip()

        # 2) bail early if they submitted empty
        if not condition:
            error = "Please enter an elderly health condition."
        else:
            # 3) pass it in as a keyword to ensure it's bound to `query`
            answer, docs = get_recommendations(condition)
            bullets = [line.strip(" -") for line in answer.splitlines() if line.strip()]
            result = {"bullets": bullets, "docs": docs}


    return render(request,
                  "recommender/recommend.html",
                  {
                    "result": result,
                    "error":  error,
                  })
