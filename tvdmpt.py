import os
import pickle


class Storage:
    def save(self, data, filename='library_data.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load(self, filename='library_data.pkl'):
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    return pickle.load(f)
            except:
                return None
        return None


class Book:
    def __init__(self, title, author, status="доступна", borrower=None):
        self.__title = title
        self.__author = author
        self.__status = status
        self.__borrower = borrower

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_status(self):
        return self.__status

    def get_borrower(self):
        return self.__borrower

    def borrow(self, username):
        self.__status = "выдана"
        self.__borrower = username

    def return_book(self):
        self.__status = "доступна"
        self.__borrower = None

    def __str__(self):
        if self.__borrower:
            return f"'{self.__title}' - {self.__author} ({self.__status}, у {self.__borrower})"
        return f"'{self.__title}' - {self.__author} ({self.__status})"


class User:
    def __init__(self, name, borrowed_books=None):
        self.__name = name
        self.__borrowed_books = borrowed_books or []

    def get_name(self):
        return self.__name

    def get_borrowed_books(self):
        return self.__borrowed_books.copy()

    def add_book(self, book):
        self.__borrowed_books.append(book)

    def remove_book(self, title):
        for book in self.__borrowed_books[:]:
            if book.get_title().lower() == title.lower():
                self.__borrowed_books.remove(book)
                return True
        return False

    def __str__(self):
        books = ', '.join([b.get_title() for b in self.__borrowed_books]) or "нет книг"
        return f"{self.__name}: {books}"


class Librarian:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def __str__(self):
        return self.__name


class Person:
    def __init__(self, name):
        self.name = name

    def get_role(self):
        return "Человек"


class LibraryUser(User, Person):
    def __init__(self, name, borrowed_books=None):
        User.__init__(self, name, borrowed_books)
        Person.__init__(self, name)

    def get_role(self):
        return f"Пользователь: {self.get_name()}"


class LibraryLibrarian(Librarian, Person):
    def __init__(self, name):
        Librarian.__init__(self, name)
        Person.__init__(self, name)

    def get_role(self):
        return f"Библиотекарь: {self.get_name()}"


class Library:
    def __init__(self):
        self.storage = Storage()
        self.books = []
        self.users = []
        self.librarians = []
        self.current_user = None
        self.current_librarian = None
        self.load_data()

    def load_data(self):
        data = self.storage.load()
        if data:
            self.books = data.get('books', [])
            self.users = data.get('users', [])
            self.librarians = data.get('librarians', [])
        else:
            self.books = [
                Book("Война и мир", "Лев Толстой"),
                Book("Преступление и наказание", "Федор Достоевский"),
                Book("Мастер и Маргарита", "Михаил Булгаков")
            ]
            self.users = [
                User("Иван Петров"),
                User("Мария Иванова")
            ]
            self.librarians = [
                Librarian("Анна Сергеевна")
            ]

    def save_data(self):
        data = {
            'books': self.books,
            'users': self.users,
            'librarians': self.librarians
        }
        self.storage.save(data)

    def add_book(self, title, author):
        if not self.current_librarian:
            return "ошибка: требуется роль библиотекаря"
        self.books.append(Book(title, author))
        self.save_data()
        return f"книга '{title}' успешно добавлена"

    def remove_book(self, title):
        if not self.current_librarian:
            return "ошибка: требуется роль библиотекаря"
        for book in self.books:
            if book.get_title().lower() == title.lower():
                if book.get_status() == "выдана":
                    return f"ошибка: книга '{title}' выдана пользователю, удалить нельзя"
                self.books.remove(book)
                self.save_data()
                return f"книга '{title}' успешно удалена"
        return f"ошибка: книга '{title}' не найдена"

    def register_user(self, name):
        if not self.current_librarian:
            return "ошибка: требуется роль библиотекаря"
        for user in self.users:
            if user.get_name().lower() == name.lower():
                return f"ошибка: пользователь '{name}' уже существует"
        self.users.append(User(name))
        self.save_data()
        return f"пользователь '{name}' успешно зарегистрирован"

    def show_all_users(self):
        if not self.current_librarian:
            return "ошибка: требуется роль библиотекаря"
        if not self.users:
            return "список пользователей пуст"
        result = "\nсписок пользователей\n"
        for i, user in enumerate(self.users, 1):
            result += f"{i}. {user}\n"
        return result

    def show_all_books(self):
        if not self.current_librarian and not self.current_user:
            return "ошибка: требуется авторизация"
        if not self.books:
            return "список книг пуст"
        result = "\nвсе книги\n"
        for i, book in enumerate(self.books, 1):
            result += f"{i}. {book}\n"
        return result

    def show_available_books(self):
        if not self.current_user:
            return "ошибка: требуется авторизация пользователя"
        available = [b for b in self.books if b.get_status() == "доступна"]
        if not available:
            return "нет доступных книг"
        result = "\nдоступные книги\n"
        for i, book in enumerate(available, 1):
            result += f"{i}. '{book.get_title()}' - {book.get_author()}\n"
        return result

    def borrow_book(self, title):
        if not self.current_user:
            return "ошибка: требуется авторизация пользователя"
        for book in self.books:
            if book.get_title().lower() == title.lower():
                if book.get_status() == "выдана":
                    borrower = book.get_borrower()
                    return f"ошибка: книга '{title}' уже выдана пользователю {borrower}"
                book.borrow(self.current_user.get_name())
                self.current_user.add_book(book)
                self.save_data()
                return f"книга '{title}' успешно взята"
        return f"ошибка: книга '{title}' не найдена"

    def return_book(self, title):
        if not self.current_user:
            return "ошибка: требуется авторизация пользователя"
        if self.current_user.remove_book(title):
            for book in self.books:
                if book.get_title().lower() == title.lower():
                    book.return_book()
                    self.save_data()
                    return f"книга '{title}' успешно возвращена"
        return f"ошибка: у вас нет книги '{title}'"

    def show_my_books(self):
        if not self.current_user:
            return "ошибка: требуется авторизация пользователя"
        books = self.current_user.get_borrowed_books()
        if not books:
            return "у вас нет взятых книг"
        result = f"\nкниги пользователя {self.current_user.get_name()}\n"
        for i, book in enumerate(books, 1):
            result += f"{i}. '{book.get_title()}' - {book.get_author()}\n"
        return result


class LibraryApp:
    def __init__(self):
        self.library = Library()

    def run(self):
        print("\n" + "*" * 50)
        print("         добро пожаловать в библиотеку")
        print("*" * 50)

        while True:
            try:
                if not self.library.current_librarian and not self.library.current_user:
                    print("\nвыберите роль")
                    print("1. библиотекарь")
                    print("2. пользователь")
                    print("0. выход")

                    choice = input("ваш выбор: ")

                    if choice == "1":
                        name = input("введите имя библиотекаря: ")
                        found = False
                        for lib in self.library.librarians:
                            if lib.get_name().lower() == name.lower():
                                self.library.current_librarian = lib
                                self.library.current_user = None
                                print(f"\nдобро пожаловать, {lib.get_name()}!")
                                found = True
                                break
                        if not found:
                            print("\nошибка: библиотекарь не найден")

                    elif choice == "2":
                        name = input("введите имя пользователя: ")
                        found = False
                        for user in self.library.users:
                            if user.get_name().lower() == name.lower():
                                self.library.current_user = user
                                self.library.current_librarian = None
                                print(f"\nдобро пожаловать, {user.get_name()}!")
                                found = True
                                break
                        if not found:
                            print("\nошибка: пользователь не найден")

                    elif choice == "0":
                        print("\nсохраняем данные...")
                        self.library.save_data()
                        print("до свидания")
                        break

                    else:
                        print("\nневерный выбор")

                elif self.library.current_librarian:
                    print(f"\n{'*' * 50}")
                    print(f"меню библиотекаря: {self.library.current_librarian.get_name()}")
                    print(f"{'*' * 50}")
                    print("1. добавить новую книгу")
                    print("2. удалить книгу")
                    print("3. зарегистрировать пользователя")
                    print("4. список всех пользователей")
                    print("5. список всех книг")
                    print("0. выйти из аккаунта")

                    choice = input("ваш выбор: ")

                    if choice == "1":
                        title = input("название книги: ")
                        author = input("автор: ")
                        print("\n" + self.library.add_book(title, author))

                    elif choice == "2":
                        title = input("название книги для удаления: ")
                        print("\n" + self.library.remove_book(title))

                    elif choice == "3":
                        name = input("имя нового пользователя: ")
                        print("\n" + self.library.register_user(name))

                    elif choice == "4":
                        print(self.library.show_all_users())

                    elif choice == "5":
                        print(self.library.show_all_books())

                    elif choice == "0":
                        print("\nвыход из аккаунта...")
                        self.library.current_librarian = None

                    else:
                        print("\nневерный выбор")

                elif self.library.current_user:
                    print(f"\n{'*' * 50}")
                    print(f"меню пользователя: {self.library.current_user.get_name()}")
                    print(f"{'*' * 50}")
                    print("1. просмотреть доступные книги")
                    print("2. взять книгу")
                    print("3. вернуть книгу")
                    print("4. мои книги")
                    print("0. выйти из аккаунта")

                    choice = input("ваш выбор: ")

                    if choice == "1":
                        print(self.library.show_available_books())

                    elif choice == "2":
                        title = input("название книги: ")
                        print("\n" + self.library.borrow_book(title))

                    elif choice == "3":
                        title = input("название книги: ")
                        print("\n" + self.library.return_book(title))

                    elif choice == "4":
                        print(self.library.show_my_books())

                    elif choice == "0":
                        print("\nвыход из аккаунта...")
                        self.library.current_user = None

                    else:
                        print("\nневерный выбор")

                input("\nнажмите enter, чтобы продолжить...")

            except KeyboardInterrupt:
                print("\n\nзавершение работы...")
                self.library.save_data()
                break
            except Exception as e:
                print(f"\nошибка: {e}")
                input("\nнажмите enter, чтобы продолжить...")


if __name__ == "__main__":
    app = LibraryApp()
    app.run()
