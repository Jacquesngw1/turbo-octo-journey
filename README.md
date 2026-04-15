# AI Delivery Dashboard

Real-time repository health metrics and AI-powered risk analysis dashboard.

## Features

- **Health Metrics** – Monitors open PRs, issues, commits, and computes a health score for each configured repository.
- **AI Risk Analysis** – Sends metrics to Claude for an intelligent risk assessment with actionable recommendations.
- **Auto-Refresh** – Dashboard refreshes metrics every 60 seconds.

## Quick Start

### Prerequisites

- Python 3.12+
- A GitHub personal access token with `repo` read permissions
- An Anthropic API key (for the AI risk analysis feature)

### 1. Clone and configure

```bash
git clone https://github.com/Jacquesngw1/turbo-octo-journey.git
cd turbo-octo-journey
cp .env.example .env
# Edit .env and fill in your tokens and repository list
```

### 2. Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open <http://localhost:5050> in your browser.

### 3. Run with Docker

```bash
docker compose up --build
```

Open <http://localhost:5050> in your browser.

## Environment Variables

| Variable | Description |
|---|---|
| `GITHUB_TOKEN` | GitHub personal access token |
| `GITHUB_ORG` | GitHub organization or username |
| `GITHUB_REPOS` | Comma-separated list of repository names |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude |

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Dashboard UI |
| `GET /api/metrics` | JSON health metrics for all configured repos |
| `GET /api/risk` | JSON AI-powered risk analysis |

## Project Structure

```
├── app.py                  # Flask application
├── dashboard/
│   ├── __init__.py
│   ├── github_client.py    # GitHub REST API client
│   ├── metrics.py          # Health metric computation
│   └── claude_client.py    # Claude AI risk analysis client
├── templates/
│   └── dashboard.html      # Dashboard frontend
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```