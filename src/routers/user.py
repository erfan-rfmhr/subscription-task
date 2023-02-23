from authentication.auth import login_manager
from database.db_user import add_user, get_user
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/user", tags=["user"])
user_templates = Jinja2Templates(directory="templates/user")


@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return user_templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    await add_user(username, password)
    access_token = login_manager.create_access_token(
        data={"sub": username}
    )
    response = RedirectResponse(url="/user/account", status_code=status.HTTP_302_FOUND)
    login_manager.set_cookie(response=response, token=access_token)
    return response


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return user_templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await get_user(username)
    if not user:
        return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)
    if not (password == user.password and username == user.username):
        return RedirectResponse(url="/user/login", status_code=status.HTTP_302_FOUND)
    access_token = login_manager.create_access_token(
        data={"sub": username}
    )
    response = RedirectResponse(url="/user/account", status_code=status.HTTP_302_FOUND)
    login_manager.set_cookie(response=response, token=access_token)
    return response


@router.get("/account", response_class=HTMLResponse)
async def account(request: Request, user=Depends(login_manager)):
    return user_templates.TemplateResponse("account.html", {"request": request, "user": user})
