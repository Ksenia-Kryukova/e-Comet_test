from fastapi import APIRouter, Depends, Query

from src.db.connection import get_db
from src.api.schemas.schemas import Repo


router = APIRouter(prefix="/api/repos", tags=["Repositories"])


@router.get("/top100", response_model=list[Repo])
async def get_top100(
    order_by: str = Query(
        "stars",
        regex="^(stars|forks|watchers|open_issues)$",
        description="Поле для сортировки"
    ),
    direction: str = Query(
        "desc",
        regex="^(asc|desc)$",
        description="Направление сортировки"
    ),
    db=Depends(get_db)
):
    '''Отображение топ 100 публичных репозиториев из PostgresSQL.
    '''
    query = f"""
        SELECT repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
        FROM top100
        ORDER BY {order_by} {direction.upper()}
        LIMIT 100
    """
    async with db.acquire() as connection:
        rows = await connection.fetch(query)
    return [dict(row) for row in rows]
