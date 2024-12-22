import pytest
from pytest_mock import mocker
from unittest import mock

from src.utils.github_parser import fetch_top_repositories
from core.config import settings

TOKEN = settings.GITHUB_TOKEN


@pytest.fixture
def mock_httpx_get(mocker):
    return mocker.patch("httpx.get")


def test_fetch_top_repositories(mock_httpx_get):
    mock_response = mock.Mock()
    mock_response.raise_for_status = mock.Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "full_name": "repo1",
                "owner": {"login": "owner1"},
                "stargazers_count": 100
            }
        ]
    }
    mock_httpx_get.return_value = mock_response

    result = fetch_top_repositories()

    assert result == [
        {
            "full_name": "repo1",
            "owner": {"login": "owner1"},
            "stargazers_count": 100
        }
    ]
    mock_httpx_get.assert_called_once_with(
        "https://api.github.com/search/repositories",
        headers={f'"Authorization": "Bearer {TOKEN}"'},
        params={
            "q": "stars:>1",
            "sort": "stars",
            "order": "desc",
            "per_page": 100
        }
    )
