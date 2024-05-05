class UserAlreadyExists(Exception):
    ...

class UserDoesNotExist(Exception):
    ...

class FileAlreadyExists(Exception):
    ...

class FileDoesNotExist(Exception):
    ...

class StorageLimitExceeded(Exception):
    """Exception raised when the storage limit is exceeded."""
    def __init__(self, message, current_plan_level=None, current_space=None, required_space=None):
        self.message = message
        self.current_plan_level = current_plan_level
        self.required_space = required_space
        super().__init__(message)
