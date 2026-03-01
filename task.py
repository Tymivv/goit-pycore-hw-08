import pickle
from collections import UserDict
from datetime import datetime, timedelta


# ===================== DECORATOR =====================
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments."
        except AttributeError:
            return "Contact not found."
    return wrapper


# ===================== FIELDS =====================
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def to_date(self):
        return datetime.strptime(self.value, "%d.%m.%Y").date()


# ===================== RECORD =====================
class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        phone = self.find_phone(old_phone)
        if phone is None:
            raise ValueError("Old phone number not found")
        phone.value = Phone(new_phone).value

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = self.birthday.value if self.birthday else "—"
        return f"{self.name.value}: {phones}, birthday: {bday}"


# ===================== ADDRESS BOOK =====================
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def __str__(self):
        if not self.data:
            return "Address book is empty."
        return "\n".join(str(record) for record in self.data.values())

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.to_date()
            this_year = bday.replace(year=today.year)

            if today <= this_year <= end:
                congrat_date = this_year
                if congrat_date.weekday() == 5:
                    congrat_date += timedelta(days=2)
                elif congrat_date.weekday() == 6:
                    congrat_date += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "birthday": congrat_date.strftime("%d.%m.%Y")
                })

        return result



# ===================== HANDLERS =====================
@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return "; ".join(p.value for p in record.phones)


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return "Birthday not set."
    return record.birthday.value


@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"{b['name']}: {b['birthday']}" for b in upcoming)


# ===================== MAIN =====================
def parse_input(user_input: str):
    if not user_input.strip():
        return "", []
    parts = user_input.strip().split()
    return parts[0].lower(), parts[1:]


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        command, args = parse_input(input("Enter a command: "))

        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        elif command == "":
            continue

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
