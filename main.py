import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from loguru import logger

from classes.app_manager import AppManager
from classes.custom_exceptions import AppBaseException
from orm_models import OrderORMModel, UserORMModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logger.add("logfile.log", level="DEBUG")

load_dotenv()
app_manager = AppManager()


@app.exception_handler(AppBaseException)
async def app_exception_handler(request: Request, exc: AppBaseException):
	return templates.TemplateResponse(
		request=request,
		name="error.html",
		status_code=exc.status_code,
		context={
			"status_code": exc.status_code,
			"detail": exc.message,
			"title": "Something went wrong",
		},
	)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	added = request.query_params.get("added")
	token = request.cookies.get("access_token")
	context: dict = app_manager.get_auth_context(token)
	logger.debug(context)
	if context["is_logged_in"] == True:
		order: OrderORMModel = app_manager.get_order_by_auth_context(context)
		logger.debug(order.cart_count)
	else:
		order = None
	menu: dict = app_manager.create_menu_for_index()
	template_response = templates.TemplateResponse(request=request, name="index.html", context={"menu": menu, "context": context, "order": order, "added": added})
	return template_response


@app.get("/account", response_class=HTMLResponse)
async def account(request: Request):
	token = request.cookies.get("access_token")
	logger.debug(token)
	context: dict = app_manager.get_auth_context(token)
	order: OrderORMModel = app_manager.get_order_by_auth_context(context)
	template_response = templates.TemplateResponse(request=request, name="account.html", context={"context": context, "order": order})
	return template_response

# @app.get("/auth", response_class=HTMLResponse)
# async def auth(request: Request):
# 	template_response = templates.TemplateResponse(request=request, name="auth.html")
# 	return template_response

@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
	deleted = request.query_params.get("deleted")
	token = request.cookies.get("access_token")
	try:
		context: dict = app_manager.get_auth_context(token)
		order: OrderORMModel = app_manager.get_order_by_auth_context(context)
	except AppBaseException:
		context = {"is_logged_in": False}
		order = None
	template_response = templates.TemplateResponse(request=request, name="cart.html", context={"context": context, "order": order, "deleted": deleted})
	return template_response

@app.get("/addtocart/{item_id}")
async def add_to_cart(item_id: int, request: Request):
	token = request.cookies.get("access_token")
	logger.debug(token)
	if not app_manager.get_auth_context(token)["is_logged_in"]:
		return RedirectResponse(url="/login", status_code=302)
	context: dict = app_manager.get_auth_context(token)
	user_id = context["user_id"]
	app_manager.cart_manager.add_to_cart(item_id, user_id)
	return RedirectResponse(url="/?added=1", status_code=302)

@app.get("/removefromcart/{item_id}")
async def remove_from_cart(item_id: int, request: Request):
	token = request.cookies.get("access_token")
	if token is None:
		return RedirectResponse(url="/login", status_code=302)
	context: dict = app_manager.get_auth_context(token)
	user_id = context["user_id"]
	app_manager.cart_manager.remove_from_cart(item_id, user_id)
	return RedirectResponse(url="/cart?deleted=1", status_code=302)

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
	template_response = templates.TemplateResponse(request=request, name="login.html")
	return template_response

@app.post("/process_login")
async def process_login(email: str = Form(), password: str = Form()):
	logger.debug(f"email: {email}, password: {password}")
	app_manager.validate_login(email, password)

	user_id = app_manager.user_manager.get_user_id_by_email(email)
	jwt_token = app_manager.jwt_manager.create_token(user_id)

	response = RedirectResponse(url="/account", status_code=302)
	response.set_cookie(
		key="access_token",
		value=jwt_token,
		samesite="lax"
	)
	return response

@app.get("/logout")
async def logout(request: Request):
	response = RedirectResponse(url="/", status_code=302)
	response.delete_cookie(key="access_token")
	return response


@app.post("/order")
async def order(request: Request, name: str = Form(), address: str = Form(), phone: str = Form()):
	token = request.cookies.get("access_token")
	context: dict = app_manager.get_auth_context(token)
	user_id = context["user_id"]
	app_manager.cart_manager.checkout(user_id, name, address, phone)
	response = RedirectResponse(url="/ordered", status_code=302)
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
	user_id = app_manager.user_manager.get_user_id_by_email(email)
	jwt_token = app_manager.jwt_manager.create_token(user_id)
	response = RedirectResponse(url="/account", status_code=302)
	response.set_cookie(
		key="access_token",
		value=jwt_token,
		samesite="lax"
	)
	return response

uvicorn.run(app, host="127.0.0.1", port=8001)