import httpx
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta

from core.config import settings


GITHUB_API_URL = "https://api.github.com"
TOKEN = settings.GITHUB_TOKEN


def fetch_top_repositories():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"q": "stars:>1", "sort": "stars", "order": "desc", "per_page": 100}
    response = httpx.get(f"{GITHUB_API_URL}/search/repositories", headers=headers, params=params)
    response.raise_for_status()
    return response.json()["items"]


def fetch_activity(owner, repo, since, until):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"since": since, "until": until}
    response = httpx.get(f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits", headers=headers, params=params)
    response.raise_for_status()
    commits = response.json()
    authors = {commit["commit"]["author"]["name"] for commit in commits if "author" in commit}
    return len(commits), list(authors)


def save_to_db(data, table_name, connection):
    with connection.cursor() as cursor:
        query = sql.SQL("""
            INSERT INTO {table} ({fields})
            VALUES ({values})
            ON CONFLICT DO NOTHING
        """).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, data.keys())),
            values=sql.SQL(', ').join(sql.Placeholder() * len(data))
        )
        cursor.execute(query, list(data.values()))
        connection.commit()


def parse_and_save():
    connection = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )

    top_repos = fetch_top_repositories()
    for i, repo in enumerate(top_repos, start=1):
        repo_data = {
            "repo": repo["full_name"],
            "owner": repo["owner"]["login"],
            "position_cur": i,
            "position_prev": None,  # Это поле можно обновлять позже
            "stars": repo["stargazers_count"],
            "watchers": repo["watchers_count"],
            "forks": repo["forks_count"],
            "open_issues": repo["open_issues_count"],
            "language": repo.get("language"),
        }
        save_to_db(repo_data, "top100", connection)

        since = (datetime.datetime() - timedelta(days=7)).isoformat()
        until = datetime.datetime().isoformat()
        commits, authors = fetch_activity(repo["owner"]["login"], repo["name"], since, until)
        activity_data = {
            "repo": repo["full_name"],
            "date": datetime.datetime().date(),
            "commits": commits,
            "authors": authors,
        }
        save_to_db(activity_data, "activity", connection)

    connection.close()