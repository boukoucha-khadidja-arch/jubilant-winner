# =========================================
# C3 - Strategy Pattern for Submission Evaluation
# =========================================


# -------- Strategy Interface --------
class EvaluationStrategy:
    def evaluate(self, submission):
        raise NotImplementedError


# -------- Concrete Strategies --------
class RuleBasedEvaluation(EvaluationStrategy):
    def evaluate(self, submission):
        print("Rule-based evaluation applied")
        return "approved"


class PeerReviewEvaluation(EvaluationStrategy):
    def evaluate(self, submission):
        print("Peer review evaluation applied")
        return "approved"


class MachineLearningEvaluation(EvaluationStrategy):
    def evaluate(self, submission):
        print("Machine learning evaluation applied (mocked)")
        return "rejected"


# -------- Context --------
class SubmissionEvaluator:
    def __init__(self, strategy: EvaluationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: EvaluationStrategy):
        self.strategy = strategy

    def evaluate(self, submission):
        return self.strategy.evaluate(submission)


# -------- Submission --------
class Submission:
    def __init__(self, title):
        self.title = title


# -------- Test --------
if __name__ == "__main__":

    submission = Submission("Paper 1")

    evaluator = SubmissionEvaluator(RuleBasedEvaluation())
    print("Result:", evaluator.evaluate(submission))

    evaluator.set_strategy(PeerReviewEvaluation())
    print("Result:", evaluator.evaluate(submission))

    evaluator.set_strategy(MachineLearningEvaluation())
    print("Result:", evaluator.evaluate(submission))
