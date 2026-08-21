# Build complete customer risk profile
def build_risk_profile(
    score: float,
    level: str,
    reasons: list[str],
    positive_factors: list[str],
    components: dict,
    summary: dict,
) -> dict:

    # Return complete risk profile
    return {
        "risk_score": score,
        "risk_level": level,
        "risk_reasons": reasons,
        "positive_factors": positive_factors,
        "components": components,
        "risk_factor_summary": summary,
    }