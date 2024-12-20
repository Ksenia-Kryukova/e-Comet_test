from fastapi import APIRouter, Depends, HTTPException, Query
from db.connection import get_db

from api.schemas.schemas import Activity


router = APIRouter(prefix="/api/repos", tags=["Activity"])


@router.get("/{owner}/{repo}/activity", response_model=list[Activity])
async def get_commit_activity(
    owner: str,
    repo: str,
    since: str = Query(..., description="Начало периода (YYYY-MM-DD)"),
    until: str = Query(..., description="Конец периода (YYYY-MM-DD)"),
    db=Depends(get_db)
):
    '''Информация об активности репозитория по коммитам за выбранный промежуток времени по дням.
    '''
    query = """
        SELECT date, commits, authors
        FROM activity
        WHERE repo_id = (SELECT id FROM top100 WHERE repo = $1 AND owner = $2)
            AND date BETWEEN $3 AND $4
        ORDER BY date ASC
    """
    async with db.acquire() as connection:
        rows = await connection.fetch(query, repo, owner, since, until)
    if not rows:
        raise HTTPException(status_code=404, detail="No activity found for the given repository and period")
    return [dict(row) for row in rows]