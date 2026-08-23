class EvaluationTracker:
    def __init__(self):
        self.scores = {
            "answer_relevancy": [],
            "faithfulness": [],
            "context_recall": [],
            "latency": [],
            "cost_per_query": [],
        }

    def add_score(self, metric_name: str, score: float):
        """Appends a score to the specified metric if it is valid."""
        if metric_name in self.scores and score is not None:
            self.scores[metric_name].append(score)


tracker = EvaluationTracker()
