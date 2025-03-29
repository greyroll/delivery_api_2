import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

class JWTManager:
    def __init__(self, algorithm: str = "HS256", expiration_minutes: int = 60):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def create_token(self, data: dict) -> str:
        """
        Создает JWT-токен с полезной нагрузкой data и устанавливает время истечения.
        """
        payload = data.copy()
        # Добавляем время истечения токена
        payload["exp"] = datetime.now() + timedelta(minutes=self.expiration_minutes)
        token = jwt.encode(payload, key=self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token: str) -> Optional[dict]:
        """
        Декодирует и проверяет JWT-токен.
        Возвращает полезную нагрузку, если токен корректен, или None в случае ошибки.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # Здесь можно добавить дополнительную логику обработки истекшего токена
            print("Token expired")
        except jwt.InvalidTokenError:
            # Обработка ошибки декодирования или неверного токена
            print("Invalid token")
        return None


