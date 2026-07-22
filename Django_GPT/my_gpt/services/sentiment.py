from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"

@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        device=get_pipeline_device(),
        top_k=None,  # 전체 레이블 점수를 받고 싶으면
    )

def run_sentiment(text: str) -> dict:
    pipe = get_sentiment_pipeline()
    raw = pipe(text)[0]  # top_k=None이면 list[dict]
    # 정렬 및 최고 라벨 추출
    scores = sorted(raw, key=lambda x: x["score"], reverse=True)
    top = scores[0]
    return {
        "label": top["label"],
        "score": float(top["score"]),
        "all_scores": [
            {"label": s["label"], "score": float(s["score"])}
            for s in scores
        ],
    }