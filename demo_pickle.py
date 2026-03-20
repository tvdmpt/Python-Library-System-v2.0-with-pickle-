import pickle
import os
from library import Book, User, Librarian

def demonstrate_binary_files():
    print("\nдемонстрация чтения бинарных файлов\n")
    
    filename = 'library_data.pkl'
    
    if os.path.exists(filename):
        print(f"файл: {filename}")
        print(f"размер: {os.path.getsize(filename)} байт")
        
        with open(filename, 'rb') as f:
            binary_data = f.read(50)
            print(f"первые 50 байт: {binary_data}")
            
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            print(f"тип данных: {type(data)}")
            print(f"ключи: {list(data.keys())}")
            print(f"книг: {len(data['books'])}")
            print(f"пользователей: {len(data['users'])}")
            print(f"библиотекарей: {len(data['librarians'])}")
            print(f"\nданные:")
            print(f"  книги: {data['books']}")
            print(f"  пользователи: {data['users']}")
            print(f"  библиотекари: {data['librarians']}")
        print("-" * 50)
    else:
        print(f"файл {filename} не найден")
    
    input("\nнажмите enter для выхода...")

if __name__ == "__main__":
    demonstrate_binary_files()
