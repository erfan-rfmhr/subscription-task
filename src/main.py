import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database.db import Base, db_admin, engine
from database.db_subscription import create_subscriptions
from routers import user

app = FastAPI()

app.include_router(user.router)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
jinja_templates = Jinja2Templates(directory="templates")
db_admin.mount_app(app)
Base.metadata.create_all(bind=engine)
# create subscriptions if they don't exist
asyncio.run(create_subscriptions())


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return jinja_templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
