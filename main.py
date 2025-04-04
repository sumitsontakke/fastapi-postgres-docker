from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware

from apis.base import api_router
from core.config import log
from core.config import settings
from db.base import Base
from db.session import engine

# https://www.fastapitutorial.com/blog/creating-tables-in-fastapi/
# from db.session import engine
# from db.base_class import Base
# APIs route file to maintain all route entries


def create_tables():
    Base.metadata.create_all(bind=engine)


# include router i.e. api routes defined in base file to this app
def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.add_middleware(CORSMiddleware, allow_origins=["*"])
    create_tables()
    include_router(app)
    return app


app = start_application()
log.info("Welcome!")


@app.get("/")
def home():
    return {"msg": "Hello FastAPI🚀"}


@app.get("/userinfo")
def defaultuser():
    return {"user_name": "Sumit Jain", "user_role": "Coding World Explorer"}
