from fastapi import APIRouter, Depends, HTTPException, status

# from core.security import get_current_user
# from api.models.token import TokenData
# from api.models.currency import Currency, CurrencyResponse
# from utils.external_api import 


router_api_repos = APIRouter(prefix="/api/repos", tags=["api", "repos"])


@router_api_repos.get("/top100")
async def get_top100():
    '''Отображение топ 100 публичных репозиториев из PostgresSQL.
    '''
    pass


@router_api_repos.get("/{owner}/{repo}/activity")
async def get_commit_activity(owner, repo,  since, until):
    '''Информация об активности репозитория по коммитам за выбранный промежуток времени по дням. 
    '''
    pass