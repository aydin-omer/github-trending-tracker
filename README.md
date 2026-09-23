# 📈 GitHub Trending Tracker

A dashboard that tracks GitHub's weekly trending repositories, updated automatically — no email, just a link you can bookmark and check anytime.

## What it does

Every Monday, this project automatically:

1. Fetches [GitHub's weekly trending page](https://github.com/trending?since=weekly) (all languages)
2. Parses out each repository's name, description, primary language, total stars, and stars gained this week
3. Rebuilds a static HTML dashboard with the results
4. Commits the updated page, which is served live via **GitHub Pages**

No inbox clutter, no manual browsing — just open the page whenever you want to see what's trending.

## Why

Checking GitHub Trending manually is easy to forget to do, and the page itself resets constantly. This project turns it into a standing, always-up-to-date reference — useful for scouting new tools, watching a particular ecosystem, or just staying current with what the developer community is excited about.

## How it works

- **Language:** Python
- **Automation:** [GitHub Actions](https://github.com/features/actions) scheduled workflow (cron job)
- **Data source:** GitHub's public trending page, parsed with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (GitHub has no official trending API)
- **Hosting:** [GitHub Pages](https://pages.github.com/) — a free static site served directly from this repository
- **No server, no database, no email, no secrets required**

## Architecture

```
.github/workflows/fetch.yml   → Runs weekly: fetch the trending page, rebuild the dashboard, commit
fetch_trending.py             → Scrapes github.com/trending and generates index.html
requirements.txt              → Python dependencies
index.html                    → The generated dashboard, served via GitHub Pages
```

## Setup

If you want to run your own copy of this dashboard:

1. Fork or clone this repository
2. No secrets are required — the data source is a public page, no API key needed
3. Enable GitHub Pages: **Settings → Pages → Source: Deploy from a branch → Branch: main, / (root)**
4. That's it — the workflow runs automatically every Monday. You can also trigger it manually from the **Actions** tab using **Run workflow**.
5. Your dashboard will be live at `https://<your-username>.github.io/<repo-name>/`

## Customization

- **Track a specific language instead of all:** change `TRENDING_URL` in `fetch_trending.py` to `https://github.com/trending/python?since=weekly` (swap `python` for any language)
- **Track daily or monthly trending instead of weekly:** change `since=weekly` to `since=daily` or `since=monthly` in `TRENDING_URL`
- **Change the schedule:** edit the `cron` expression in `.github/workflows/fetch.yml` ([crontab.guru](https://crontab.guru/) is helpful for this)
- **Show more or fewer repos:** GitHub's trending page returns roughly 25 repos per request; slice the `repos` list in `main()` if you want fewer

## Notes

- GitHub's trending page has no official public API, so this project scrapes the public HTML page directly. GitHub occasionally changes this page's structure, which can break the parsing selectors in `fetch_trending.py` — if the dashboard ever comes up empty, that's the first place to check.
- If an individual repo entry fails to parse (missing field, unexpected markup), it's skipped rather than crashing the entire run.
