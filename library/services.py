
from dataclasses import dataclass
from datetime import date, timedelta

from library.exceptions import (
    LibraryError,
    BookNotFoundError,
    BookAlreadyBorrowedError,
    BookNotBorrowedError,
    NotLendableError
)


@dataclass
class Loan:
    item: object
    borrowed_on: date
    due_date: date
    renewed: bool = False


class Library:
    def __init__(self):
        self._items = {}
        self._loans = {}

    def add_item(self, item):
        if item.item_id in self._items:
            raise LibraryError("Item ID already exists.")
        self._items[item.item_id] = item

    def get_item(self, item_id):
        item = self._items.get(str(item_id))
        if item is None:
            raise BookNotFoundError("Book not found.")
        return item

    def borrow(self, item_id, today=None):
        today = today or date.today()
        item_id = str(item_id)
        item = self.get_item(item_id)

        if not item.can_lend():
            raise NotLendableError("This item cannot be borrowed.")

        if item_id in self._loans:
            raise BookAlreadyBorrowedError("Already borrowed.")

        loan = Loan(
            item,
            today,
            today + timedelta(days=item.loan_days())
        )
        self._loans[item_id] = loan
        return loan

    def return_item(self, item_id):
        item_id = str(item_id)
        if item_id not in self._loans:
            raise BookNotBorrowedError("Book is not borrowed.")
        return self._loans.pop(item_id)

    def renew(self, item_id, today=None):
        today = today or date.today()
        item_id = str(item_id)

        if item_id not in self._loans:
            raise BookNotBorrowedError("Book is not borrowed.")

        loan = self._loans[item_id]

        if today > loan.due_date:
            raise LibraryError("Overdue loans cannot be renewed.")

        if loan.renewed:
            raise LibraryError("Already renewed.")

        loan.due_date += timedelta(days=loan.item.loan_days())
        loan.renewed = True
        return loan

    def overdue_report(self, today=None):
        today = today or date.today()
        return [
            loan for loan in self._loans.values()
            if today > loan.due_date
        ]

    def list_items(self):
        return list(self._items.values())

    def list_loans(self):
        return list(self._loans.values())
