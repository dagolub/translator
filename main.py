import uvicorn  # type: ignore
from fastapi import FastAPI
from route import users, login, translator
from config.config import settings
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix=f"{settings.API_V1_STR}", tags=["login"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(
    translator.router, prefix=f"{settings.API_V1_STR}/translator", tags=["translator"]
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec
