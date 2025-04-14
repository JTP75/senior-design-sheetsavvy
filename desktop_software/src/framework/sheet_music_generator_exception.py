class SheetMusicGeneratorException(Exception):
    """Base exception for all sheet music generation exceptions"""

    default_message = "A sheet music generation-related error occurred"

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)