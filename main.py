import hashlib
import os

class SimplifiedDigitalSignature:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.document_path = None
        self.document_hash = None
        self.signature = None
        self.load_existing_data()
    
    def load_existing_data(self):
        """Завантаження збережених даних при запуску програми"""
        try:
            # Завантажуємо ключі, якщо вони є
            if os.path.exists("private_key.txt"):
                with open("private_key.txt", "r") as f:
                    self.private_key = int(f.read().strip())
                print("✅ Завантажено приватний ключ з файлу")
            
            if os.path.exists("public_key.txt"):
                with open("public_key.txt", "r") as f:
                    self.public_key = int(f.read().strip())
                print("✅ Завантажено публічний ключ з файлу")
            
            # Завантажуємо підпис, якщо він є
            if os.path.exists("signature.txt"):
                with open("signature.txt", "r") as f:
                    self.signature = int(f.read().strip())
                print("✅ Завантажено цифровий підпис з файлу")
                
        except Exception as e:
            print(f"❌ Помилка при завантаженні даних: {e}")
        
    def generate_keys(self, last_name, birth_date, secret_word):
        """Генерація пари ключів на основі персональних даних"""
        personal_data = f"{last_name}{birth_date}{secret_word}"
        self.private_key = int(hashlib.sha256(personal_data.encode()).hexdigest()[:8], 16)
        self.public_key = (self.private_key * 7) % 1000007
        
        print(f"\n=== Ключі згенеровано ===")
        print(f"Приватний ключ: {self.private_key}")
        print(f"Публічний ключ: {self.public_key}")
        
        # Зберігаємо ключі у файли
        with open("private_key.txt", "w") as f:
            f.write(str(self.private_key))
        with open("public_key.txt", "w") as f:
            f.write(str(self.public_key))
        print("✅ Ключі збережено у файли: private_key.txt та public_key.txt")
        
        return self.private_key, self.public_key
    
    def create_document_hash(self, document_path):
        """Створення хешу документа з файлу"""
        try:
            with open(document_path, 'rb') as f:
                file_content = f.read()
            
            self.document_path = document_path
            self.document_hash = int(hashlib.sha256(file_content).hexdigest()[:8], 16)
            
            print(f"\nХеш документа '{document_path}': {self.document_hash}")
            return self.document_hash
        except FileNotFoundError:
            print(f"❌ Файл '{document_path}' не знайдено!")
            return None
        except Exception as e:
            print(f"❌ Помилка при читанні файлу: {e}")
            return None
    
    def sign_document(self):
        """Створення цифрового підпису"""
        if self.private_key is None or self.document_hash is None:
            print("Помилка: Спочатку згенеруйте ключі та створіть документ!")
            return None
            
        self.signature = self.document_hash ^ self.private_key
        
        # Зберігаємо підпис у файл
        with open("signature.txt", "w") as f:
            f.write(str(self.signature))
        
        print(f"\n=== Цифровий підпис створено ===")
        print(f"Підпис: {self.signature}")
        print("✅ Підпис збережено у файл: signature.txt")
        return self.signature
    
    def verify_signature(self, document_path_to_verify):
        """Перевірка цифрового підпису - ЧИТАЄ ПІДПИС З ФАЙЛУ"""
        if self.public_key is None:
            print("Помилка: Спочатку згенеруйте ключі!")
            return False
        
        try:
            # Читаємо підпис з файлу (а не з пам'яті)
            with open("signature.txt", "r") as f:
                signature_from_file = int(f.read().strip())
            
            # Читаємо документ для перевірки
            with open(document_path_to_verify, 'rb') as f:
                current_content = f.read()
            
            current_hash = int(hashlib.sha256(current_content).hexdigest()[:8], 16)
            decrypted_hash = signature_from_file ^ self.private_key
            
            print(f"\n=== Перевірка підпису ===")
            print(f"Файл для перевірки: {document_path_to_verify}")
            print(f"Підпис з файлу: {signature_from_file}")
            print(f"Хеш поточного документа: {current_hash}")
            print(f"Розшифрований хеш з підпису: {decrypted_hash}")
            
            if decrypted_hash == current_hash:
                print("✅ Підпис ДІЙСНИЙ - документ не змінений")
                return True
            else:
                print("❌ Підпис ПІДРОБЛЕНО - документ змінений або пошкоджений")
                return False
                
        except FileNotFoundError:
            print(f"❌ Файл не знайдено!")
            return False
        except Exception as e:
            print(f"❌ Помилка при перевірці: {e}")
            return False

def main_menu():
    """Головне меню програми"""
    signature_system = SimplifiedDigitalSignature()
    
    while True:
        print("\n" + "="*50)
        print("      СИСТЕМА ЦИФРОВИХ ПІДПИСІВ")
        print("="*50)
        print("1. Генерація ключів")
        print("2. Створення підпису для файлу")
        print("3. Перевірка підпису файлу")
        print("4. Вихід")
        print("-"*50)
        
        choice = input("Оберіть опцію (1-4): ").strip()
        
        if choice == "1":
            print("\n--- Генерація ключів ---")
            last_name = input("Введіть прізвище: ").strip()
            birth_date = input("Введіть дату народження (ДДММРРРР): ").strip()
            secret_word = input("Введіть секретне слово: ").strip()
            
            signature_system.generate_keys(last_name, birth_date, secret_word)
            
        elif choice == "2":
            print("\n--- Створення підпису для файлу ---")
            if signature_system.private_key is None:
                print("Спочатку згенеруйте ключі! (пункт 1)")
                continue
                
            document_path = input("Введіть шлях до файлу для підпису: ").strip()
            if signature_system.create_document_hash(document_path) is not None:
                signature_system.sign_document()
            
        elif choice == "3":
            print("\n--- Перевірка підпису файлу ---")
            if signature_system.private_key is None:
                print("Спочатку згенеруйте ключі! (пункт 1)")
                continue
                
            document_path = input("Введіть шлях до файлу для перевірки: ").strip()
            signature_system.verify_signature(document_path)
            
        elif choice == "4":
            print("Вихід з програми...")
            break
            
        else:
            print("Невірний вибір! Спробуйте знову.")
        
        input("\nНатисніть Enter для продовження...")

if __name__ == "__main__":
    main_menu()