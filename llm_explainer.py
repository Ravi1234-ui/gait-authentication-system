# llm_explainer.py

def explain_decision(summary: dict) -> str:
    """
    This function simulates LLM behavior.
    Replace with real LLM API if required.
    """

    if summary["decision"] == "ACCESS GRANTED":
        return (
            f"Access was granted because the walking pattern closely matched "
            f"{summary['person']}. The confidence score of {summary['confidence']} "
            f"is above the required threshold of {summary['threshold']}."
        )

    return (
        f"Access was denied because the walking pattern did not sufficiently "
        f"match any enrolled employee. The confidence score of "
        f"{summary['confidence']} was below the acceptable threshold."
    )
