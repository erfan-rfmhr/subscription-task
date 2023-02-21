from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import user
from src.database.db import db_admin, Base, engine

app = FastAPI()

app.include_router(user.router)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
jinja_templates = Jinja2Templates(directory="templates")
db_admin.mount_app(app)
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return jinja_templates.TemplateResponse("home.html", {"request": request})
