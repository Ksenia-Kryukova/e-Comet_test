import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.endpoints import top100, activity
from src.exceptions import not_found_handler, internal_error_handler


app = FastAPI(
    title="GitHub Top 100 Parser",
    description="API для работы с данными о репозиториях GitHub.",
    version="1.0.0",
)

app.include_router(top100.router)
app.include_router(activity.router)
app.add_exception_handler(StarletteHTTPException, not_found_handler)
app.add_exception_handler(Exception, internal_error_handler)


if __name__ == "__main__":
    uvicorn.run(app="main:app")
