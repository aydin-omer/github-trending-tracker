import requests
from bs4 import BeautifulSoup
import datetime

TRENDING_URL = "https://github.com/trending?since=weekly"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_trending_repos():
    resp = requests.get(TRENDING_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    repo_boxes = soup.select("article.Box-row")

    repos = []
    for box in repo_boxes:
        try:
            name_tag = box.select_one("h2 a")
            full_name = name_tag["href"].strip("/")
            url = "https://github.com/" + full_name

            desc_tag = box.select_one("p")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            lang_tag = box.select_one('span[itemprop="programmingLanguage"]')
            language = lang_tag.get_text(strip=True) if lang_tag else "Unknown"

            star_tag = box.select_one('a[href$="/stargazers"]')
            total_stars = star_tag.get_text(strip=True) if star_tag else "?"

            stars_week_tag = box.select_one("span.d-inline-block.float-sm-right")
            stars_this_week = stars_week_tag.get_text(strip=True) if stars_week_tag else "?"

            repos.append({
                "name": full_name,
                "url": url,
                "description": description,
                "language": language,
                "total_stars": total_stars,
                "stars_this_week": stars_this_week,
            })
        except Exception as e:
            print(f"Skipped one repo due to parsing error: {e}")
            continue

    return repos


def build_html(repos):
    rows = ""
    for i, repo in enumerate(repos, start=1):
        rows += f"""
        <tr>
          <td>{i}</td>
          <td><a href="{repo['url']}" target="_blank">{repo['name']}</a></td>
          <td>{repo['description']}</td>
          <td><span class="lang-badge">{repo['language']}</span></td>
          <td>⭐ {repo['total_stars']}</td>
          <td>{repo['stars_this_week']}</td>
        </tr>
        """

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GitHub Trending Tracker</title>
<style>
  body {{ font-family: -apple-system, Arial, sans-serif; margin: 40px; background: #0d1117; color: #e6edf3; }}
  h1 {{ margin-bottom: 4px; }}
  .subtitle {{ color: #8b949e; margin-bottom: 24px; }}
  table {{ width: 100%; border-collapse: collapse; background: #161b22; box-shadow: 0 1px 3px rgba(0,0,0,0.4); }}
  th, td {{ text-align: left; padding: 10px 14px; border-bottom: 1px solid #30363d; font-size: 14px; vertical-align: top; }}
  th {{ background: #21262d; }}
  a {{ color: #58a6ff; text-decoration: none; font-weight: 600; }}
  .lang-badge {{ background: #30363d; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
</style>
</head>
<body>
  <h1>📈 GitHub Trending Tracker</h1>
  <div class="subtitle">Last updated: {now} — Weekly trending, all languages</div>
  <table>
    <tr>
      <th>#</th>
      <th>Repository</th>
      <th>Description</th>
      <th>Language</th>
      <th>Total Stars</th>
      <th>Stars This Week</th>
    </tr>
    {rows}
  </table>
</body>
</html>
"""
    return html


def main():
    repos = fetch_trending_repos()
    print(f"Fetched {len(repos)} trending repos.")

    html = build_html(repos)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("index.html updated.")


if __name__ == "__main__":
    main()
