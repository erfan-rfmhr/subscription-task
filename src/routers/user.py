from authentication.auth import login_manager
from database.db_invoice import get_user_invoices, user_has_already_bought_this_subscription, buy_subscription, \
    activate_subscription, deactivate_subscription
from database.db_user import add_user, get_user
from database.db_subscription import get_subscription_price, get_subscription_name
from task_managment.task_scheduler import interval_decrease_credit, scheduler
from fastapi import APIRouter, Request, Form, status, Depends, Query
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


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    login_manager.set_cookie(response=response, token="")
    return response


@router.get("/account", response_class=HTMLResponse)
async def account(request: Request, user=Depends(login_manager)):
    # find all invoices for this user
    user_invoices = await get_user_invoices(user.id)
    active_subscriptions = []
    deactivated_subscriptions = []
    for invoice in user_invoices:
        if invoice.is_active:
            active_subscriptions.append(invoice.subscription_id)
        else:
            deactivated_subscriptions.append(invoice.subscription_id)
    return user_templates.TemplateResponse("account.html", {"request": request, "user": user,
                                                            "active_subscriptions": active_subscriptions,
                                                            "deactivated_subscriptions": deactivated_subscriptions})


@router.get('/buy')
async def buy(request: Request, user=Depends(login_manager), subscription_id: int = Query(...)):
    if not await user_has_already_bought_this_subscription(user.id, subscription_id):
        await buy_subscription(user.id, subscription_id)
    return RedirectResponse(url="/user/account", status_code=status.HTTP_302_FOUND)


@router.get('/activate')
async def activate(request: Request, user=Depends(login_manager), subscription_id: int = Query(...)):
    invoice = None
    if await user_has_already_bought_this_subscription(user.id, subscription_id):
        invoice = await activate_subscription(user.id, subscription_id)
    price = await get_subscription_price(subscription_id)
    scheduler.add_job(interval_decrease_credit, 'interval', seconds=3, args=[user.id, price],
                      id=f'{invoice.id}')
    return RedirectResponse(url="/user/account", status_code=status.HTTP_302_FOUND)


@router.get('/deactivate')
async def deactivate(request: Request, user=Depends(login_manager), subscription_id: int = Query(...)):
    invoice = None
    if await user_has_already_bought_this_subscription(user.id, subscription_id):
        invoice = await deactivate_subscription(user.id, subscription_id)
    scheduler.remove_job(f'{invoice.id}')
    return RedirectResponse(url="/user/account", status_code=status.HTTP_302_FOUND)


@router.get('/invoices', response_class=HTMLResponse)
async def invoices(request: Request, user=Depends(login_manager)):
    user_invoices = await get_user_invoices(user.id)
    info = []
    for invoice in user_invoices:
        subscription_name = await get_subscription_name(invoice.subscription_id)
        subscription_price = await get_subscription_price(invoice.subscription_id)
        info.append((invoice.id, "active" if invoice.is_active else "deactivated", subscription_name, subscription_price,
                     "10 min", invoice.start_date))
    return user_templates.TemplateResponse("invoices.html", {"request": request, "user": user, "info": info})
