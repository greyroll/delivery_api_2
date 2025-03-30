class AppBaseException(Exception):
    """Base class for all custom exceptions."""
    def __init__(self, message: str = "Application error", status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class OrphanOrderException(AppBaseException):
    def __init__(self, message: str = "Order has no associated user."):
        super().__init__(message, status_code=400)

class NoItemsToRemoveException(AppBaseException):
    def __init__(self, message: str = "No items in cart to remove."):
        super().__init__(message, status_code=400)

class UserNotFoundException(AppBaseException):
    def __init__(self, message: str = "User not found."):
        super().__init__(message, status_code=404)

class UserAlreadyExistsException(AppBaseException):
    def __init__(self, message: str = "User with this email already exists."):
        super().__init__(message, status_code=409)

class PasswordIsTooShortException(AppBaseException):
    def __init__(self, min_length: int = 6):
        message = f"Password must be at least {min_length} characters long."
        super().__init__(message, status_code=422)

class InvalidPasswordException(AppBaseException):
    def __init__(self, message: str = "The password you entered is incorrect."):
        super().__init__(message, status_code=401)

