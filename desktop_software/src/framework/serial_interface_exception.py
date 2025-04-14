class SerialInterfaceException(Exception):
    """Base exception for all serial interface exceptions"""

    default_message = "A serial communication-related error occurred"

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)