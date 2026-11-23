
class LibraryError(Exception):
    """Base exception for library errors."""
    pass


class BookNotFoundError(LibraryError):
    pass


class BookAlreadyBorrowedError(LibraryError):
    pass


class BookNotBorrowedError(LibraryError):
    pass


class NotLendableError(LibraryError):
    pass
