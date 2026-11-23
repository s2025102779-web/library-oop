
from abc import ABC, abstractmethod


class LibraryItem(ABC):
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title

    @property
    def item_id(self):
        return self._item_id

    @item_id.setter
    def item_id(self, value):
        if not str(value).strip():
            raise ValueError("Item ID cannot be empty.")
        self._item_id = str(value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be empty.")
        self._title = value.strip()

    def can_lend(self):
        return True

    @abstractmethod
    def loan_days(self):
        pass

    def __str__(self):
        return f"{self.item_id} - {self.title}"


class Book(LibraryItem):
    def loan_days(self):
        return 14


class ReferenceBook(Book):
    def can_lend(self):
        return False


class Thesis(LibraryItem):
    def __init__(self, item_id, title, adviser):
        super().__init__(item_id, title)
        self.adviser = adviser

    @property
    def adviser(self):
        return self._adviser

    @adviser.setter
    def adviser(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Adviser cannot be empty.")
        self._adviser = value.strip()

    def loan_days(self):
        return 3
