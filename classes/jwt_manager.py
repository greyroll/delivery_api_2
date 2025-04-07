import os
import jwt
from datetime import datetime, timedelta, timezone

from loguru import logger



class JWTManager:
    def __init__(self, algorithm: str = "HS256", expiration_minutes: int = 60):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def create_token(self, user_id: int) -> str:
        """
        Создает JWT-токен с полезной нагрузкой data и устанавливает время истечения.
        """
        payload = {"sub": str(user_id)}
        # Добавляем время истечения токена
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=self.expiration_minutes)
        payload["exp"] = int(expire_time.timestamp())
        token = jwt.encode(payload, key=self.secret_key, algorithm=self.algorithm)
        logger.debug(f"JWTManager.create_token: token created: {token}, user: {payload['sub']}")
        return token

    def get_payload_or_none(self, token: str | None) -> dict | None:
        """
        Проверяет JWT-токен и возвращает payload, если токен валиден.
        Если токен невалиден или истёк — возвращает None.
        """
        if token is None:
            logger.debug("JWTManager.get_payload_or_none: token is None")
            return None
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            logger.debug("JWTManager.get_payload_or_none: token is invalid")
            return None



