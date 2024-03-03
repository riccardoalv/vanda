from transformers import pipeline


def summary(text):
    summarizer = pipeline(
        "summarization", model="Falconsai/medical_summarization")

    summary_text = summarizer(
        text,
        max_length=100,
        min_length=20,
        do_sample=False
    )

    return summary_text[0]['summary_text']
