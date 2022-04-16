class BadRequestException(Exception):
    """Exception is raised when user input is invalid"""

    def __init__(self, message="Invalid user input"):
        self.message = message
        super().__init__(self.message)


class NotFoundException(Exception):
    """Exception is raised when requested data does not exist"""

    def __init__(self, message="Data not found"):
        self.message = message
        super().__init__(self.message)
