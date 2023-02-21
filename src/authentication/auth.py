import os

from dotenv import load_dotenv
from fastapi_login import LoginManager

load_dotenv()

login_manager = LoginManager(os.getenv("SECRET_KEY"), token_url="/user/login", use_cookie=True, use_header=False)
