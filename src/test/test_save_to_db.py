from unittest import mock
from psycopg2 import sql

from src.utils.github_parser import save_to_db


def test_save_to_db():
    mock_connection = mock.MagicMock()
    mock_cursor = mock.MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    data = {"repo": "repo1", "stars": 100}
    table_name = "top100"

    save_to_db(data, table_name, mock_connection)

    execute_args, execute_kwargs = mock_cursor.execute.call_args

    expected_query = sql.SQL(
        """
        INSERT INTO {table} ({fields})
        VALUES ({values})
        ON CONFLICT DO NOTHING
        """
    ).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(", ").join(map(sql.Identifier, data.keys())),
        values=sql.SQL(", ").join(sql.Placeholder() * len(data)),
    )

    assert execute_args[0].__class__ == expected_query.__class__, "Типы запросов не совпадают"
    assert execute_args[1] == list(data.values()), "Параметры запроса не совпадают"

    mock_connection.commit.assert_called_once()
