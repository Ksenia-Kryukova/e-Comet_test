import pytest
from unittest import mock

from src.utils.github_parser import parse_and_save


@pytest.fixture
def mock_httpx_get(mocker):
    return mocker.patch("httpx.get")


def test_parse_and_save(mocker):
    mock_fetch_top_repositories = mocker.patch("src.utils.github_parser.fetch_top_repositories")
    mock_fetch_activity = mocker.patch("src.utils.github_parser.fetch_activity")
    mock_save_to_db = mocker.patch("src.utils.github_parser.save_to_db")

    mock_fetch_top_repositories.return_value = [
        {
            "full_name": "repo1",
            "owner": {"login": "owner1"},
            "stargazers_count": 100
        }
    ]
    mock_fetch_activity.return_value = (2, ["author1", "author2"])

    parse_and_save()

    mock_save_to_db.assert_any_call(
        {
            "repo": "repo1",
            "owner": "owner1",
            "position_cur": 1,
            "position_prev": None,
            "stars": 100,
            "watchers": 0,
            "forks": 0,
            "open_issues": 0,
            "language": None
         },
        "top100", mock.ANY
    )
    mock_save_to_db.assert_any_call(
        {
            "repo": "repo1",
            "date": mock.ANY,
            "commits": 2,
            "authors": ["author1", "author2"]
         },
        "activity", mock.ANY
    )
