from transformers import pipeline


class PlagiarismDetectorService:
    def __init__(self, model_name: str = "roberta-base-openai-detector"):
        self.detector = pipeline(
            "text-classification",
            model=model_name,
            device=0
        )

    def check_plagiarism(self, text: str) -> float:
        result = self.detector(text)
        return result[0]["score"] if result[0]["label"] == "fake" else 1 - result[0]["score"]
