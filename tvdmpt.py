import os
import pickle


class Storage:
    def save(self, data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load(self, filename):
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
        data = self.storage.load('books.pkl')
        if data:
            self.books = data
        else:
            self.books = [
                Book("Война и мир", "Лев Толстой"),
                Book("Преступление и наказание", "Федор Достоевский"),
                Book("Мастер и Маргарита", "Михаил Булгаков")
            ]

        data = self.storage.load('users.pkl')
        if data:
            self.users = data
        else:
            self.users = [
                User("Иван Петров"),
                User("Мария Иванова")
            ]

        data = self.storage.load('librarians.pkl')
        if data:
            self.librarians = data
        else:
            self.librarians = [
                Librarian("Анна Сергеевна")
            ]

    def save_data(self):
        self.storage.save(self.books, 'books.pkl')
        self.storage.save(self.users, 'users.pkl')
        self.storage.save(self.librarians, 'librarians.pkl')

    def add_book(self, title, author):
        if not self.current_librarian:
            return "Ошибка: Требуется роль библиотекаря!"
        self.books.append(Book(title, author))
        self.save_data()
        return f"Книга '{title}' успешно добавлена!"

    def remove_book(self, title):
        if not self.current_librarian:
            return "Ошибка: Требуется роль библиотекаря!"
        for book in self.books:
            if book.get_title().lower() == title.lower():
                if book.get_status() == "выдана":
                    return f"Ошибка: Книга '{title}' выдана пользователю, удалить нельзя!"
                self.books.remove(book)
                self.save_data()
                return f"Книга '{title}' успешно удалена!"
        return f"Ошибка: Книга '{title}' не найдена!"

    def register_user(self, name):
        if not self.current_librarian:
            return "Ошибка: Требуется роль библиотекаря!"
        for user in self.users:
            if user.get_name().lower() == name.lower():
                return f"Ошибка: Пользователь '{name}' уже существует!"
        self.users.append(User(name))
        self.save_data()
        return f"Пользователь '{name}' успешно зарегистрирован!"

    def show_all_users(self):
        if not self.current_librarian:
            return "Ошибка: Требуется роль библиотекаря!"
        if not self.users:
            return "Список пользователей пуст."
        result = "\nСПИСОК ПОЛЬЗОВАТЕЛЕЙ\n"
        for i, user in enumerate(self.users, 1):
            result += f"{i}. {user}\n"
        return result

    def show_all_books(self):
        if not self.current_librarian and not self.current_user:
            return "Ошибка: Требуется авторизация!"
        if not self.books:
            return "Список книг пуст."
        result = "\nВСЕ КНИГИ\n"
        for i, book in enumerate(self.books, 1):
            result += f"{i}. {book}\n"
        return result

    def show_available_books(self):
        if not self.current_user:
            return "Ошибка: Требуется авторизация пользователя!"
        available = [b for b in self.books if b.get_status() == "доступна"]
        if not available:
            return "Нет доступных книг."
        result = "\nДОСТУПНЫЕ КНИГИ\n"
        for i, book in enumerate(available, 1):
            result += f"{i}. '{book.get_title()}' - {book.get_author()}\n"
        return result

    def borrow_book(self, title):
        if not self.current_user:
            return "Ошибка: Требуется авторизация пользователя!"
        for book in self.books:
            if book.get_title().lower() == title.lower():
                if book.get_status() == "выдана":
                    borrower = book.get_borrower()
                    return f"Ошибка: Книга '{title}' уже выдана пользователю {borrower}!"
                book.borrow(self.current_user.get_name())
                self.current_user.add_book(book)
                self.save_data()
                return f"Книга '{title}' успешно взята!"
        return f"Ошибка: Книга '{title}' не найдена!"

    def return_book(self, title):
        if not self.current_user:
            return "Ошибка: Требуется авторизация пользователя!"
        if self.current_user.remove_book(title):
            for book in self.books:
                if book.get_title().lower() == title.lower():
                    book.return_book()
                    self.save_data()
                    return f"Книга '{title}' успешно возвращена!"
        return f"Ошибка: У вас нет книги '{title}'!"

    def show_my_books(self):
        if not self.current_user:
            return "Ошибка: Требуется авторизация пользователя!"
        books = self.current_user.get_borrowed_books()
        if not books:
            return "У вас нет взятых книг."
        result = f"\nКНИГИ ПОЛЬЗОВАТЕЛЯ {self.current_user.get_name()}\n"
        for i, book in enumerate(books, 1):
            result += f"{i}. '{book.get_title()}' - {book.get_author()}\n"
        return result


class LibraryApp:
    def __init__(self):
        self.library = Library()

    def run(self):
        print("\n" + "*" * 50)
        print("         ДОБРО ПОЖАЛОВАТЬ В БИБЛИОТЕКУ")
        print("*" * 50)

        while True:
            try:
                if not self.library.current_librarian and not self.library.current_user:
                    print("\nВЫБЕРИТЕ РОЛЬ")
                    print("1. Библиотекарь")
                    print("2. Пользователь")
                    print("0. Выход")

                    choice = input("Ваш выбор: ")

                    if choice == "1":
                        name = input("Введите имя библиотекаря: ")
                        found = False
                        for lib in self.library.librarians:
                            if lib.get_name().lower() == name.lower():
                                self.library.current_librarian = lib
                                self.library.current_user = None
                                print(f"\nДобро пожаловать, {lib.get_name()}!")
                                found = True
                                break
                        if not found:
                            print("\nОшибка: Библиотекарь не найден!")

                    elif choice == "2":
                        name = input("Введите имя пользователя: ")
                        found = False
                        for user in self.library.users:
                            if user.get_name().lower() == name.lower():
                                self.library.current_user = user
                                self.library.current_librarian = None
                                print(f"\nДобро пожаловать, {user.get_name()}!")
                                found = True
                                break
                        if not found:
                            print("\nОшибка: Пользователь не найден! Обратитесь к библиотекарю.")

                    elif choice == "0":
                        print("\nСохраняем данные...")
                        self.library.save_data()
                        print("До свидания!")
                        break

                    else:
                        print("\nНеверный выбор!")

                elif self.library.current_librarian:
                    print(f"\n{'*' * 50}")
                    print(f"МЕНЮ БИБЛИОТЕКАРЯ: {self.library.current_librarian.get_name()}")
                    print(f"{'*' * 50}")
                    print("1. Добавить новую книгу")
                    print("2. Удалить книгу")
                    print("3. Зарегистрировать пользователя")
                    print("4. Список всех пользователей")
                    print("5. Список всех книг")
                    print("0. Выйти из аккаунта")

                    choice = input("Ваш выбор: ")

                    if choice == "1":
                        title = input("Название книги: ")
                        author = input("Автор: ")
                        print("\n" + self.library.add_book(title, author))

                    elif choice == "2":
                        title = input("Название книги для удаления: ")
                        print("\n" + self.library.remove_book(title))

                    elif choice == "3":
                        name = input("Имя нового пользователя: ")
                        print("\n" + self.library.register_user(name))

                    elif choice == "4":
                        print(self.library.show_all_users())

                    elif choice == "5":
                        print(self.library.show_all_books())

                    elif choice == "0":
                        print("\nВыход из аккаунта...")
                        self.library.current_librarian = None

                    else:
                        print("\nНеверный выбор!")

                elif self.library.current_user:
                    print(f"\n{'*' * 50}")
                    print(f"МЕНЮ ПОЛЬЗОВАТЕЛЯ: {self.library.current_user.get_name()}")
                    print(f"{'*' * 50}")
                    print("1. Просмотреть доступные книги")
                    print("2. Взять книгу")
                    print("3. Вернуть книгу")
                    print("4. Мои книги")
                    print("0. Выйти из аккаунта")

                    choice = input("Ваш выбор: ")

                    if choice == "1":
                        print(self.library.show_available_books())

                    elif choice == "2":
                        title = input("Название книги: ")
                        print("\n" + self.library.borrow_book(title))

                    elif choice == "3":
                        title = input("Название книги: ")
                        print("\n" + self.library.return_book(title))

                    elif choice == "4":
                        print(self.library.show_my_books())

                    elif choice == "0":
                        print("\nВыход из аккаунта...")
                        self.library.current_user = None

                    else:
                        print("\nНеверный выбор!")

                input("\nНажмите Enter, чтобы продолжить...")

            except KeyboardInterrupt:
                print("\n\nЗавершение работы...")
                self.library.save_data()
                break
            except Exception as e:
                print(f"\nОшибка: {e}")
                input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    app = LibraryApp()
    app.run()