class PerformanceAnalyzer:
    def __init__(self, scores):
        self.scores = scores

    def highest(self):
        return max(self.scores)

    def lowest(self):
        return min(self.scores)

    def improvement(self):
        return self.scores[-1] - self.scores[0]