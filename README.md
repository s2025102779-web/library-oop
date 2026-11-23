
# Library Lending System

A simple Library Lending System built using Python and Object-Oriented Programming (OOP).

## Features
- Add and view library items
- Borrow and return books
- Reference books cannot be borrowed
- Thesis items have a 3-day loan period
- Renew borrowed books once
- View overdue loans
- Handles library errors using custom exceptions

## Project Structure
- `library/models.py` - Library item classes
- `library/services.py` - Library operations
- `library/exceptions.py` - Custom exceptions
- `main.py` - Main program
- `tests/` - Unit tests

## How to Run

1. Activate the virtual environment.
2. Run:

   `python main.py`

## How to Run Tests

   `python -m unittest -v`
