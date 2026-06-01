"""Reading decision ordering and helpers."""

READING_DECISION_RANK = {
    "SKIP": 0,
    "SKIM": 1,
    "READ": 2,
    "DEEP_READ": 3,
    "ESCALATE": 4,
}


def is_flagged(decision: str) -> bool:
    """Return whether a decision should be highlighted in summaries."""

    return READING_DECISION_RANK.get(decision, 0) >= READING_DECISION_RANK["DEEP_READ"]
