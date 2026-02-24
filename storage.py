import pickle
from address_book import AddressBook


FILENAME = "addressbook.pkl"


def save_data(book, filename=FILENAME):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename=FILENAME):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()
