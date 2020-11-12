from fastapi import FastAPI

from . import __version__
from .apis import root, user

app = FastAPI(
    title='My sample API',
    description='My sample API application using FastAPI + SQLAlchemy + MySQL/PostgreSQL + pytest-docker',
    version='{}'.format(__version__)
)

# APIs
app.include_router(root.router)
app.include_router(user.router)
