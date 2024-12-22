import pytest
from unittest import mock

from src.utils.github_parser import fetch_activity
from src.core.config import settings

TOKEN = settings.GITHUB_TOKEN

@pytest.fixture
def mock_httpx_get(mocker):
    return mocker.patch("httpx.get")


def test_fetch_activity(mock_httpx_get):
    mock_response = mock.Mock()
    mock_response.raise_for_status = mock.Mock()
    mock_response.json.return_value = [
        {"commit": {"author": {"name": "author1"}}},
        {"commit": {"author": {"name": "author2"}}}
    ]
    mock_httpx_get.return_value = mock_response

    commits, authors = fetch_activity("owner", "repo", "2024-01-01", "2024-01-07")

    assert commits == 2
    assert authors == ["author1", "author2"]
    mock_httpx_get.assert_called_once_with(
        "https://api.github.com/repos/owner/repo/commits",
        headers={f'"Authorization": "Bearer {TOKEN}"'},
        params={"since": "2024-01-01", "until": "2024-01-07"}
    )
