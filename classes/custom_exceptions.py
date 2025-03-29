class OrphanOrderException(Exception):
	pass

class NoItemsToRemoveException(Exception):
	pass

class UserNotFoundException(Exception):
	pass

class UserAlreadyExistsException(Exception):
	pass

class PasswordIsTooShortException(Exception):
	pass