from loguru import logger

class AppBaseException(Exception):
    """Base class for all custom exceptions."""
    def __init__(self, message: str = "Application error", status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class OrphanOrderException(AppBaseException):
    def __init__(self, message: str = "Order has no associated user."):
        super().__init__(message, status_code=400)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class NoItemsToRemoveException(AppBaseException):
    def __init__(self, message: str = "No items in cart to remove."):
        super().__init__(message, status_code=400)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class NoItemsInCartException(AppBaseException):
    def __init__(self, message: str = "No items in cart."):
        super().__init__(message, status_code=400)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class UserNotFoundException(AppBaseException):
    def __init__(self, message: str = "User not found."):
        super().__init__(message, status_code=404)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class UserAlreadyExistsException(AppBaseException):
    def __init__(self, message: str = "User with this email already exists."):
        super().__init__(message, status_code=409)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class PasswordIsTooShortException(AppBaseException):
    def __init__(self, min_length: int = 6):
        message = f"Password must be at least {min_length} characters long."
        super().__init__(message, status_code=422)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class InvalidPasswordException(AppBaseException):
    def __init__(self, message: str = "The password you entered is incorrect."):
        super().__init__(message, status_code=401)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class TokenExpiredException(AppBaseException):
    def __init__(self, message="Token has expired."):
        super().__init__(message, status_code=401)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")

class InvalidTokenException(AppBaseException):
    def __init__(self, message="Token is invalid."):
        super().__init__(message, status_code=401)
        logger.error(f"status_code: {self.status_code}, message: {self.message}")



