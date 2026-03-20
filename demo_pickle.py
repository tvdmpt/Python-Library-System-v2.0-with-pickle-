import pickle
import os
from tvdmpt import Book, User, Librarian

def demonstrate_binary_files():
    print("\nдемонстрация чтения бинарных файлов\n")
    
    files = ['books.pkl', 'users.pkl', 'librarians.pkl']
    
    for filename in files:
        if os.path.exists(filename):
            print(f"\nфайл: {filename}")
            print(f"размер: {os.path.getsize(filename)} байт")
            
            with open(filename, 'rb') as f:
                binary_data = f.read(50)
                print(f"первые 50 байт: {binary_data}")
                
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                print(f"тип данных: {type(data)}")
                print(f"количество объектов: {len(data)}")
                print(f"данные: {data}")
            print("-" * 50)
        else:
            print(f"файл {filename} не найден")
    
    input("\nнажмите enter для выхода...")

if __name__ == "__main__":
    demonstrate_binary_files()