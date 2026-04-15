"""Claude AI client for delivery-risk analysis."""

import json
import os

import anthropic


def analyse_risk(metrics: list[dict]) -> str:
    """Send computed metrics to Claude and return a plain-text risk analysis.

    Parameters
    ----------
    metrics : list[dict]
        A list of per-repository metric dictionaries (output of
        ``compute_metrics``).

    Returns
    -------
    str
        Plain-text analysis from Claude.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: ANTHROPIC_API_KEY is not configured."

    client = anthropic.Anthropic(api_key=api_key)

    prompt = (
        "You are a software delivery risk analyst. "
        "Analyse the following repository health metrics and provide:\n"
        "1. A brief summary of overall delivery health.\n"
        "2. Key risks identified.\n"
        "3. Recommended actions to mitigate risks.\n\n"
        f"Metrics:\n{json.dumps(metrics, indent=2)}"
    )

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract plain text from the response
    return message.content[0].text
