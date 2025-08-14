class Book:
    # Class variable to store all Book instances
    all = []

    def __init__(self, title):
        self.title = title  # Calls the title.setter for validation
        Book.all.append(self)  # Add this Book instance to the list of all books

    @property
    def title(self):
        return self._title  # Getter for title

    @title.setter
    def title(self, value):
        # Validate that title is a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise Exception("title must be a non-empty string")
        self._title = value.strip()

    def contracts(self):
        """Return all Contract instances for this book."""
        # Loop through all contracts and return only those linked to this book
        return [contract for contract in Contract.all if contract.book == self]

    def authors(self):
        """Return all Author instances who have a contract for this book."""
        # Get all contracts for this book and return their authors
        return [contract.author for contract in self.contracts()]


class Author:
    # Class variable to store all Author instances
    all = []

    def __init__(self, name):
        self.name = name  # Calls the name.setter for validation
        Author.all.append(self)  # Add this Author instance to the list of all authors

    @property
    def name(self):
        return self._name  # Getter for name

    @name.setter
    def name(self, value):
        # Validate that name is a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise Exception("name must be a non-empty string")
        self._name = value.strip()

    def contracts(self):
        """Return all Contract instances for this author."""
        # Loop through all contracts and return only those linked to this author
        return [contract for contract in Contract.all if contract.author == self]

    def books(self):
        """Return all books for this author (via contracts)."""
        # Get all contracts for this author and return the linked books
        return [contract.book for contract in self.contracts()]

    def sign_contract(self, book, date, royalties):
        """Create and return a new Contract with given book, date, royalties."""
        # Creates a new Contract instance linking this author with the book
        return Contract(self, book, date, royalties)

    def total_royalties(self):
        """Return the sum of royalties from all contracts."""
        # Add up all royalties from this author's contracts
        return sum(contract.royalties for contract in self.contracts())


class Contract:
    # Class variable to store all Contract instances
    all = []

    def __init__(self, author, book, date, royalties):
        # Calls property setters to validate before assigning
        self.author = author
        self.book = book
        self.date = date
        self.royalties = royalties
        Contract.all.append(self)  # Add this contract to the list of all contracts

    @property
    def author(self):
        return self._author  # Getter for author

    @author.setter
    def author(self, value):
        # Author must be an Author instance
        if not isinstance(value, Author):
            raise Exception("author must be an instance of Author")
        self._author = value

    @property
    def book(self):
        return self._book  # Getter for book

    @book.setter
    def book(self, value):
        # Book must be a Book instance
        if not isinstance(value, Book):
            raise Exception("book must be an instance of Book")
        self._book = value

    @property
    def date(self):
        return self._date  # Getter for date

    @date.setter
    def date(self, value):
        # Date must be a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise Exception("date must be a non-empty string")
        self._date = value.strip()

    @property
    def royalties(self):
        return self._royalties  # Getter for royalties

    @royalties.setter
    def royalties(self, value):
        # Royalties must be a non-negative integer
        if not isinstance(value, int) or value < 0:
            raise Exception("royalties must be a non-negative integer")
        self._royalties = value

    @classmethod
    def contracts_by_date(cls, date):
        """Return all contracts matching the given date."""
        # Return a list of contracts whose date matches the given date
        return [contract for contract in cls.all if contract.date == date]


# ---------- Example Usage ----------
if __name__ == "__main__":
    # Create Authors
    author1 = Author("John Doe")
    author2 = Author("Jane Smith")

    # Create Books
    book1 = Book("Python Mastery")
    book2 = Book("Data Science Essentials")

    # Sign Contracts (link authors to books)
    c1 = author1.sign_contract(book1, "2025-08-14", 15)
    c2 = author1.sign_contract(book2, "2025-08-14", 20)
    c3 = author2.sign_contract(book2, "2025-08-15", 25)

    # Test Author methods
    print([b.title for b in author1.books()])  # → ['Python Mastery', 'Data Science Essentials']
    print(author1.total_royalties())  # → 35

    # Test Contract method
    same_day_contracts = Contract.contracts_by_date("2025-08-14")
    print([(c.author.name, c.book.title) for c in same_day_contracts])
    # → [('John Doe', 'Python Mastery'), ('John Doe', 'Data Science Essentials')]

