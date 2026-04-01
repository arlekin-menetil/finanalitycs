import math


class ScoringModelV1:

    VERSION = "v1.0"

    @staticmethod
    def normalize(features):
        income = features["income"]
        dti = features["dti"]
        history_score = features["history_score"]
        active_loans = features["active_loans"]
        delinquency_count = features["delinquency_count"]

        normalized_dti = max(0, 1 - dti)

        if income > 0:
            normalized_income = min(1, math.log(income + 1) / math.log(20000))
        else:
            normalized_income = 0

        normalized_history = (history_score - 300) / 550
        normalized_history = max(0, min(1, normalized_history))

        normalized_loans = max(0, 1 - (active_loans / 10))

        normalized_delinquency = 0 if delinquency_count > 0 else 1

        return {
            "dti": normalized_dti,
            "income": normalized_income,
            "history": normalized_history,
            "loans": normalized_loans,
            "delinquency": normalized_delinquency,
        }

    @staticmethod
    def calculate(features):
        normalized = ScoringModelV1.normalize(features)

        weighted_score = (
            0.30 * normalized["dti"] +
            0.20 * normalized["income"] +
            0.30 * normalized["history"] +
            0.10 * normalized["loans"] +
            0.10 * normalized["delinquency"]
        )

        final_score = 300 + weighted_score * 550

        probability = 1 / (1 + math.exp(-(final_score - 575) / 40))

        if final_score >= 750:
            risk = "LOW"
        elif final_score >= 650:
            risk = "MEDIUM"
        elif final_score >= 550:
            risk = "HIGH"
        else:
            risk = "VERY_HIGH"

        return {
            "score": round(final_score),
            "approval_probability": round(probability, 4),
            "risk_category": risk,
            "model_version": ScoringModelV1.VERSION
        }