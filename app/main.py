from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, pasted, management


@asynccontextmanager
async def lifespan(app: FastAPI):
    # db.create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(pasted.router)
app.include_router(management.router)
