from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

MODEL_ID = "sshleifer/distilbart-cnn-6-6"

@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model=MODEL_ID,
        device=get_pipeline_device(),
    )

def run_summarize(text: str, *, do_sample: bool = False) -> dict:
    pipe = get_summarizer_pipeline()
    result = pipe(
        text,
        max_length=180,
        min_length=40,
        do_sample=do_sample,
        top_p=0.9 if do_sample else 1.0,
        temperature=0.8 if do_sample else 1.0,
    )
    summary = result[0]["summary_text"].strip()
    ratio = (len(summary) / len(text)) * 100 if text else 0
    return {
        "summary": summary,
        "original_length": len(text),
        "summary_length": len(summary),
        "ratio": round(ratio, 2),
    }