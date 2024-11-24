import json
import os

DATA_FILE = "library.json"  # Файл для хранения данных


class Book:
    next_id = 1  # Для автоматической генерации ID

    def __init__(self, title, author, year, status="в наличии", book_id=None):
        self.id = book_id if book_id is not None else Book.next_id
        Book.next_id = max(Book.next_id, self.id + 1)
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f"[{self.id}] {self.title} by {self.author}, {self.year}, Status: {self.status}"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author, "year": self.year, "status": self.status}


class Library:
    def __init__(self):
        self.books = []
        self.load_books()

    def load_books(self):
        """Загрузка данных из файла."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for book_data in data:
                        book = Book(
                            title=book_data["title"],
                            author=book_data["author"],
                            year=book_data["year"],
                            status=book_data["status"],
                            book_id=book_data["id"],
                        )
                        self.books.append(book)
                print("Данные загружены из файла.")
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
        else:
            print("Файл данных не найден, библиотека пуста.")

    def save_books(self):
        """Сохранение данных в файл."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                data = [book.to_dict() for book in self.books]
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Данные сохранены.")
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def add_book(self, title, author, year):
        """Добавление новой книги."""
        try:
            book = Book(title, author, year)
            self.books.append(book)
            self.save_books()
            print("Книга добавлена успешно!")
            print(book)
        except Exception as e:
            print(f"Ошибка при добавлении книги: {e}")

    def delete_book(self, book_id):
        """Удаление книги по ID."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query):
        """Поиск книги по названию, автору или году."""
        results = [
            book for book in self.books
            if query.lower() in book.title.lower()
            or query.lower() in book.author.lower()
            or query == str(book.year)
        ]
        if results:
            print("Найденные книги:")
            for book in results:
                print(book)
        else:
            print("Книги по запросу не найдены.")

    def display_books(self):
        """Отображение всех книг в библиотеке."""
        if not self.books:
            print("Библиотека пуста.")
            return
        print("Список всех книг:")
        for book in self.books:
            print(book)

    def update_status(self, book_id, status):
        """Обновление статуса книги."""
        valid_statuses = ["в наличии", "выдана"]
        if status not in valid_statuses:
            print(f"Ошибка: Статус должен быть одним из следующих: {', '.join(valid_statuses)}")
            return

        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                print(f"Статус книги с ID {book_id} обновлен на '{status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")



def main():
    library = Library()
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Отобразить все книги")
        print("5. Обновить статус книги")
        print("6. Выход")

        choice = input("Введите номер действия: ")
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "3":
            query = input("Введите название, автора или год для поиска: ")
            library.search_books(query)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги для обновления статуса: "))
                status = input("Введите новый статус (в наличии/выдана): ").strip()
                library.update_status(book_id, status)
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
