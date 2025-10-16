def run_underwriting_check(credit_score, income, loan_amount):
    """Simulates an underwriting decision based on simple rules."""
    if credit_score < 650:
        return {"approved": False, "reason": "Credit score is too low."}
    if (loan_amount / income) > 4.0:
        return {"approved": False, "reason": "Debt-to-income ratio is too high."}

    return {"approved": True, "reason": "Customer profile meets preliminary criteria."}