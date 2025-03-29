import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from classes.app_manager import AppManager

app = FastAPI()
# Mounting the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

load_dotenv()
app_manager = AppManager()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	menu: dict = app_manager.create_menu_for_index()
	template_response = templates.TemplateResponse(request=request, name="index.html", context={"menu": menu})
	return template_response

@app.get("/account", response_class=HTMLResponse)
async def account(request: Request):
	template_response = templates.TemplateResponse(request=request, name="account.html")
	return template_response

# @app.get("/auth", response_class=HTMLResponse)
# async def auth(request: Request):
# 	template_response = templates.TemplateResponse(request=request, name="auth.html")
# 	return template_response

@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
	template_response = templates.TemplateResponse(request=request, name="cart.html")
	return template_response

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
	template_response = templates.TemplateResponse(request=request, name="login.html")
	return template_response

@app.post("/process_login")
async def process_login(email: str = Form(), password: str = Form()):
	if app_manager.validate_login(email, password) is False:
		return HTMLResponse(status_code=401, content="Invalid credentials")

	jwt_token = app_manager.jwt_manager.create_token(data={"sub": email})
	response = RedirectResponse(url="/account", status_code=302)
	response.set_cookie(
		key="access_token",
		value=jwt_token,
		samesite="lax"
	)
	return response

@app.get("/ordered", response_class=HTMLResponse)
async def ordered(request: Request):
	template_response = templates.TemplateResponse(request=request, name="ordered.html")
	return template_response

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
	template_response = templates.TemplateResponse(request=request, name="register.html")
	return template_response

@app.post("/process_register")
async def register(email: str = Form(), password: str = Form()):
	app_manager.register_user(email, password)
	jwt_token = app_manager.jwt_manager.create_token(data={"sub": email})
	response = RedirectResponse(url="/account", status_code=302)
	response.set_cookie(
		key="access_token",
		value=jwt_token,
		samesite="lax"
	)
	return response

uvicorn.run(app, host="127.0.0.1", port=8001)