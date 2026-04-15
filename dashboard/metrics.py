"""Compute health metrics from raw GitHub data."""

from datetime import datetime, timezone


def _age_days(iso_date: str) -> float:
    """Return the age in days of an ISO-8601 timestamp."""
    created = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - created).total_seconds() / 86400


def compute_metrics(raw: dict) -> dict:
    """Derive delivery-health metrics from raw GitHub repo data.

    Parameters
    ----------
    raw : dict
        Must contain keys ``repo``, ``pulls``, ``issues``, ``commits``.

    Returns
    -------
    dict
        Computed metrics including counts, averages, and risk flags.
    """
    pulls = raw.get("pulls", [])
    issues = raw.get("issues", [])
    commits = raw.get("commits", [])

    open_prs = len(pulls)
    open_issues = len(issues)
    recent_commits = len(commits)

    # Average age of open PRs (days)
    pr_ages = [_age_days(p["created_at"]) for p in pulls if "created_at" in p]
    avg_pr_age = round(sum(pr_ages) / len(pr_ages), 1) if pr_ages else 0.0

    # Average age of open issues (days)
    issue_ages = [_age_days(i["created_at"]) for i in issues if "created_at" in i]
    avg_issue_age = round(sum(issue_ages) / len(issue_ages), 1) if issue_ages else 0.0

    # Simple health score (0-100, higher is better)
    score = 100
    if open_prs > 10:
        score -= min((open_prs - 10) * 2, 30)
    if avg_pr_age > 7:
        score -= min(int(avg_pr_age - 7) * 3, 30)
    if open_issues > 20:
        score -= min((open_issues - 20), 20)
    if recent_commits < 5:
        score -= (5 - recent_commits) * 4
    score = max(score, 0)

    # Risk flags
    risk_flags = []
    if avg_pr_age > 14:
        risk_flags.append("Stale PRs (avg age > 14 days)")
    if open_prs > 15:
        risk_flags.append("High open PR count")
    if open_issues > 30:
        risk_flags.append("High open issue count")
    if recent_commits == 0:
        risk_flags.append("No recent commits")

    return {
        "repo": raw.get("repo", "unknown"),
        "open_prs": open_prs,
        "open_issues": open_issues,
        "recent_commits": recent_commits,
        "avg_pr_age_days": avg_pr_age,
        "avg_issue_age_days": avg_issue_age,
        "health_score": score,
        "risk_flags": risk_flags,
    }
