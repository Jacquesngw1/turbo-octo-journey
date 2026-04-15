"""AI Delivery Dashboard – Flask application."""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

from dashboard.github_client import fetch_repo_data
from dashboard.metrics import compute_metrics
from dashboard.claude_client import analyse_risk

load_dotenv()

app = Flask(__name__)


def _get_env(name: str) -> str | None:
    """Return an environment variable value or *None*."""
    val = os.environ.get(name)
    if val is not None:
        val = val.strip()
    return val if val else None


def _parse_repos() -> list[str]:
    """Parse the comma-separated GITHUB_REPOS env var."""
    raw = _get_env("GITHUB_REPOS")
    if not raw:
        return []
    return [r.strip() for r in raw.split(",") if r.strip()]


# ── Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Render the dashboard UI."""
    return render_template("dashboard.html")


@app.route("/api/metrics")
def api_metrics():
    """Return delivery-health metrics as JSON."""
    org = _get_env("GITHUB_ORG")
    repos = _parse_repos()

    if not org:
        return jsonify({"error": "GITHUB_ORG environment variable is not set."}), 400
    if not repos:
        return jsonify({"error": "GITHUB_REPOS environment variable is not set or empty."}), 400
    if not _get_env("GITHUB_TOKEN"):
        return jsonify({"error": "GITHUB_TOKEN environment variable is not set."}), 400

    results = []
    for repo in repos:
        try:
            raw = fetch_repo_data(org, repo)
            metrics = compute_metrics(raw)
            results.append(metrics)
        except Exception as exc:
            results.append({"repo": repo, "error": str(exc)})

    return jsonify(results)


@app.route("/api/risk")
def api_risk():
    """Return AI-powered risk analysis as JSON."""
    org = _get_env("GITHUB_ORG")
    repos = _parse_repos()

    if not org:
        return jsonify({"error": "GITHUB_ORG environment variable is not set."}), 400
    if not repos:
        return jsonify({"error": "GITHUB_REPOS environment variable is not set or empty."}), 400
    if not _get_env("GITHUB_TOKEN"):
        return jsonify({"error": "GITHUB_TOKEN environment variable is not set."}), 400
    if not _get_env("ANTHROPIC_API_KEY"):
        return jsonify({"error": "ANTHROPIC_API_KEY environment variable is not set."}), 400

    metrics_list = []
    for repo in repos:
        try:
            raw = fetch_repo_data(org, repo)
            metrics = compute_metrics(raw)
            metrics_list.append(metrics)
        except Exception as exc:
            metrics_list.append({"repo": repo, "error": str(exc)})

    try:
        analysis = analyse_risk(metrics_list)
    except Exception as exc:
        return jsonify({"error": f"Claude analysis failed: {exc}"}), 500

    return jsonify({"analysis": analysis})


# ── Entrypoint ────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=True)
