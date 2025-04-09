# 🚚 Delivery API 

Delivery API — это FastAPI-приложение, реализующее простую систему управления заказами для службы доставки. В проекте используется Pydantic для валидации, SQLModel для ORM, JWT-авторизация и шаблоны Jinja2 для фронтенда.

---

## 📦 Возможности

- Регистрация и вход пользователей
- Просмотр и оформление заказов
- История заказов
- Авторизация через JWT (хранится в cookies)
- Отображение корзины, продуктов, аккаунта
- Простой UI с использованием Jinja2-шаблонов

---
## ⚙️ Технологии

- Python 3.11+
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [Loguru](https://github.com/Delgan/loguru)
- [Uvicorn](https://www.uvicorn.org/) — ASGI сервер
- JWT авторизация
- SQLite 

---

## 🚀 Установка и запуск

1. **Клонируй репозиторий**

```bash
git clone https://github.com/greyroll/delivery_api_2.git
cd delivery_api_2
```

2. **Создай и активируй виртуальное окружение**

```bash
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows
```

3. **Установи зависимости**

```bash
pip install -r requirements.txt
```

4. **Создай .env файл (если используется)**

```env
# .env
JWT_SECRET_KEY=your_secret_key
```

5. **Запусти сервер**

```bash
uvicorn main:app --reload
```
