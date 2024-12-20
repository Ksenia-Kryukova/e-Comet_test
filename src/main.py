import uvicorn
from fastapi import FastAPI

# from api.endpoints.users import router_auth
# from api.endpoints.currency import router_currency


app = FastAPI()
# app.include_router(router_auth)
# app.include_router(router_currency)


if __name__ == "__main__":
    uvicorn.run(app="main:app")