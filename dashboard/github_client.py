"""GitHub REST API client for fetching repository data."""

import os

import requests


def _headers():
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _base_url():
    return "https://api.github.com"


def get_pulls(org: str, repo: str) -> list:
    """Fetch open pull requests for a repository."""
    url = f"{_base_url()}/repos/{org}/{repo}/pulls"
    params = {"state": "open", "per_page": 100}
    resp = requests.get(url, headers=_headers(), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_issues(org: str, repo: str) -> list:
    """Fetch open issues (excluding pull requests) for a repository."""
    url = f"{_base_url()}/repos/{org}/{repo}/issues"
    params = {"state": "open", "per_page": 100}
    resp = requests.get(url, headers=_headers(), params=params, timeout=30)
    resp.raise_for_status()
    # GitHub's issues endpoint also returns pull requests; filter them out
    return [i for i in resp.json() if "pull_request" not in i]


def get_commits(org: str, repo: str, per_page: int = 30) -> list:
    """Fetch recent commits for a repository."""
    url = f"{_base_url()}/repos/{org}/{repo}/commits"
    params = {"per_page": per_page}
    resp = requests.get(url, headers=_headers(), params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_repo_data(org: str, repo: str) -> dict:
    """Fetch pulls, issues and commits for a single repository."""
    return {
        "repo": repo,
        "pulls": get_pulls(org, repo),
        "issues": get_issues(org, repo),
        "commits": get_commits(org, repo),
    }
