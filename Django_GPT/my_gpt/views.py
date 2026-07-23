# my_gpt/views.py
import json
import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .decorators import model_login_required
from .models import InferenceHistory
from .services.sentiment import run_sentiment
from .services.summarizer import run_summarize
from .services.moderator import run_moderate

logger = logging.getLogger(__name__)


# ---------- 공통 유틸 ----------
def _parse_text(request, min_len, max_len, short_msg, long_msg):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, ("올바른 JSON 요청이 아닙니다.", 400)
    text = body.get("text")
    if not isinstance(text, str):
        return None, ("입력 형식이 올바르지 않습니다.", 400)
    text = text.strip()
    if not text:
        return None, ("분석할 문장을 입력해주세요.", 400)
    if len(text) < min_len:
        return None, (short_msg, 400)
    if len(text) > max_len:
        return None, (long_msg, 400)
    return text, None


def _recent_histories(user, task):
    if not user.is_authenticated:
        return []
    return list(
        InferenceHistory.objects
        .filter(user=user, task=task)
        .order_by("-created_at")[:5]
    )


# ---------- 감정 분석 (비로그인 허용) ----------
def sentiment_page(request):
    return render(request, "my_gpt/sentiment.html", {
        "histories": _recent_histories(request.user, InferenceHistory.Task.SENTIMENT),
        "model_id": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    })


@require_POST
def sentiment_run(request):
    text, err = _parse_text(
        request, 1, 1000,
        "분석할 문장을 입력해주세요.",
        "문장은 1,000자 이하로 입력해주세요.",
    )
    if err:
        return JsonResponse({"error": err[0]}, status=err[1])
    try:
        result = run_sentiment(text)
    except Exception:
        logger.exception("Sentiment inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    if request.user.is_authenticated:
        InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SENTIMENT,
            input_text=text,
            output_text=result["label"],
            result_data=result,
        )
    return JsonResponse({"result": result})


# ---------- 문서 요약 (로그인 필수) ----------
@model_login_required
def summarize_page(request):
    return render(request, "my_gpt/summarize.html", {
        "histories": _recent_histories(request.user, InferenceHistory.Task.SUMMARIZE),
        "model_id": "sshleifer/distilbart-cnn-6-6",
    })


@model_login_required
@require_POST
def summarize_run(request):
    text, err = _parse_text(
        request, 100, 5000,
        "요약할 문서는 100자 이상 입력해주세요.",
        "문서는 5,000자 이하로 입력해주세요.",
    )
    if err:
        return JsonResponse({"error": err[0]}, status=err[1])
    try:
        result = run_summarize(text)
    except Exception:
        logger.exception("Summarize inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.SUMMARIZE,
        input_text=text,
        output_text=result["summary"],
        result_data=result,
    )
    return JsonResponse({"result": result})


# ---------- 유해 표현 분석 (로그인 필수) ----------
@model_login_required
def moderate_page(request):
    return render(request, "my_gpt/moderate.html", {
        "histories": _recent_histories(request.user, InferenceHistory.Task.MODERATE),
        "model_id": "unitary/toxic-bert",
    })


@model_login_required
@require_POST
def moderate_run(request):
    text, err = _parse_text(
        request, 1, 1000,
        "분석할 문장을 입력해주세요.",
        "문장은 1,000자 이하로 입력해주세요.",
    )
    if err:
        return JsonResponse({"error": err[0]}, status=err[1])
    try:
        result = run_moderate(text)
    except Exception:
        logger.exception("Moderate inference failed.")
        return JsonResponse(
            {"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."},
            status=502,
        )

    InferenceHistory.objects.create(
        user=request.user,
        task=InferenceHistory.Task.MODERATE,
        input_text=text,
        output_text=result["highest_label"],
        result_data=result,
    )
    return JsonResponse({"result": result})