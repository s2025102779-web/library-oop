
import unittest
from datetime import date, timedelta

from library.models import Book, ReferenceBook, Thesis
from library.services import Library
from library.exceptions import (
    LibraryError,
    BookNotFoundError,
    BookAlreadyBorrowedError,
    BookNotBorrowedError,
    NotLendableError
)


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.today = date(2026, 11, 22)

        self.book = Book("B001", "Python Programming")
        self.reference = ReferenceBook("R001", "Python Dictionary")
        self.thesis = Thesis(
            "T001", "Computer Science Research", "Prof. Santos"
        )

        self.library.add_item(self.book)
        self.library.add_item(self.reference)
        self.library.add_item(self.thesis)

    def test_add_book(self):
        self.assertEqual(len(self.library.list_items()), 3)

    def test_borrow_book(self):
        loan = self.library.borrow("B001", self.today)
        self.assertEqual(
            loan.due_date,
            self.today + timedelta(days=14)
        )

    def test_book_already_borrowed(self):
        self.library.borrow("B001", self.today)
        with self.assertRaises(BookAlreadyBorrowedError):
            self.library.borrow("B001", self.today)

    def test_book_not_found(self):
        with self.assertRaises(BookNotFoundError):
            self.library.borrow("B999", self.today)

    def test_return_book(self):
        self.library.borrow("B001", self.today)
        self.library.return_item("B001")
        self.assertEqual(len(self.library.list_loans()), 0)

    def test_return_not_borrowed_book(self):
        with self.assertRaises(BookNotBorrowedError):
            self.library.return_item("B001")

    def test_reference_book_cannot_be_borrowed(self):
        self.assertFalse(self.reference.can_lend())
        with self.assertRaises(NotLendableError):
            self.library.borrow("R001", self.today)

    def test_thesis_has_three_day_loan(self):
        loan = self.library.borrow("T001", self.today)
        self.assertEqual(
            loan.due_date,
            self.today + timedelta(days=3)
        )
        self.assertEqual(self.thesis.adviser, "Prof. Santos")

    def test_renew_book(self):
        loan = self.library.borrow("B001", self.today)
        original_due_date = loan.due_date
        self.library.renew("B001", self.today)
        self.assertEqual(
            loan.due_date,
            original_due_date + timedelta(days=14)
        )

    def test_cannot_renew_twice(self):
        self.library.borrow("B001", self.today)
        self.library.renew("B001", self.today)
        with self.assertRaises(LibraryError):
            self.library.renew("B001", self.today)

    def test_cannot_renew_overdue_book(self):
        self.library.borrow("B001", self.today)
        overdue_date = self.today + timedelta(days=15)
        with self.assertRaises(LibraryError):
            self.library.renew("B001", overdue_date)

    def test_overdue_report(self):
        self.library.borrow("B001", self.today)
        overdue = self.library.overdue_report(
            self.today + timedelta(days=15)
        )
        self.assertEqual(len(overdue), 1)


if __name__ == "__main__":
    unittest.main()
