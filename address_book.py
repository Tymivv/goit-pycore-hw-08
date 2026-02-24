from collections import UserDict
from datetime import datetime, timedelta
from fields import Name, Phone, Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = Phone(new_phone).value
                return
        raise ValueError("Old phone not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday = self.birthday.value if self.birthday else "—"
        return f"{self.name.value}: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.to_date()
            birthday_this_year = bday.replace(year=today.year)

            if today <= birthday_this_year <= end_date:
                congrat_date = birthday_this_year

                if congrat_date.weekday() == 5:  # Saturday
                    congrat_date += timedelta(days=2)
                elif congrat_date.weekday() == 6:  # Sunday
                    congrat_date += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "birthday": congrat_date.strftime("%d.%m.%Y")
                })

        return result
