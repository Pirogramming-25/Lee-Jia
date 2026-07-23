from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

MODEL_ID = "unitary/toxic-bert"

@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model=MODEL_ID,
        device=get_pipeline_device(),
        top_k=None,  # 필수: multi-label 전체 반환
    )

def run_moderate(text: str) -> dict:
    pipe = get_moderator_pipeline()
    raw = pipe(text)[0]
    scores = sorted(raw, key=lambda x: x["score"], reverse=True)
    top = scores[0]
    return {
        "highest_label": top["label"],
        "highest_score": float(top["score"]),
        "all_scores": [
            {"label": s["label"], "score": float(s["score"])}
            for s in scores
        ],
    }