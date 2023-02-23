import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database.db import Base, db_admin, engine
from database.db_subscription import create_subscriptions
from routers import user
from task_managment.task_scheduler import scheduler

app = FastAPI()

app.include_router(user.router)

# Add the CORS middleware to your FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/statics", StaticFiles(directory="statics"), name="statics")
jinja_templates = Jinja2Templates(directory="templates")
db_admin.mount_app(app)
Base.metadata.create_all(bind=engine)
# create subscriptions if they don't exist
asyncio.run(create_subscriptions())


@app.on_event("startup")
async def start_task():
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_task():
    print("shutdown")
    scheduler.shutdown()
    await db_admin.db.async_close()


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return jinja_templates.TemplateResponse("home.html", {"request": request})


# 401 error handler
@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc: Exception):
    return jinja_templates.TemplateResponse("errors/401.html", {"request": request})


# 404 error handler
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    return jinja_templates.TemplateResponse("errors/404.html", {"request": request})


# 500 error handler
@app.exception_handler(500)
async def internal_server_error_exception_handler(request: Request, exc: Exception):
    return jinja_templates.TemplateResponse("errors/500.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
