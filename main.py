
from library.models import Book, ReferenceBook, Thesis
from library.services import Library
from library.exceptions import LibraryError


def display_menu():
    print("\n===== LIBRARY LENDING SYSTEM =====")
    print("1. View Books")
    print("2. Borrow Book")
    print("3. Return Book")
    print("4. Renew Book")
    print("5. Overdue Report")
    print("6. Exit")


def main():
    library = Library()

    library.add_item(Book("B001", "Python Programming"))
    library.add_item(Book("B002", "Object Oriented Programming"))
    library.add_item(ReferenceBook("R001", "Python Dictionary"))
    library.add_item(
        Thesis("T001", "Computer Science Research", "Prof. Santos")
    )

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                for item in library.list_items():
                    print(item, "|", "Lendable" if item.can_lend()
                          else "Reference Only")

            elif choice == "2":
                item_id = input("Enter Book ID: ")
                loan = library.borrow(item_id)
                print("Borrowed successfully!")
                print("Due date:", loan.due_date)

            elif choice == "3":
                item_id = input("Enter Book ID: ")
                library.return_item(item_id)
                print("Returned successfully!")

            elif choice == "4":
                item_id = input("Enter Book ID: ")
                loan = library.renew(item_id)
                print("Renewed successfully!")
                print("New due date:", loan.due_date)

            elif choice == "5":
                overdue = library.overdue_report()
                print("\n===== OVERDUE REPORT =====")
                if not overdue:
                    print("No overdue books.")
                else:
                    for loan in overdue:
                        print(loan.item, "| Due:", loan.due_date)

            elif choice == "6":
                print("Thank you for using the Library System!")
                break

            else:
                print("Invalid choice.")

        except LibraryError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
