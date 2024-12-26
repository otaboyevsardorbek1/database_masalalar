import sqlite3
from main import db_file_path
DB_NAME = db_file_path('university.db')


class DatabaseManager:
    """SQLite ma'lumotlar bazasi boshqaruvi."""
    
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=None):
        """SQL so'rovini bajarish."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
        except sqlite3.OperationalError as e:
            print("Xato:", e)
            return None

    def fetch_all(self, query):
        """Ma'lumotlarni olish uchun so'rov."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def get_columns(self, table):
        """Jadvalning maydonlarini olish."""
        query = f"PRAGMA table_info({table});"
        return [column[1] for column in self.fetch_all(query)]


class UniversityApp:
    """Universitet tizimini boshqaruvchi dastur."""
    
    def __init__(self):
        self.db = DatabaseManager(DB_NAME)
        self.create_tables()

    def create_tables(self):
        """Dastlabki jadvallarni yaratish."""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password TEXT NOT NULL,
                role_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES roles (id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date DATE NOT NULL,
                phone_number TEXT,
                email TEXT UNIQUE,
                parent_contact TEXT,
                group_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups (id)
            );
            """
        ]
        for table in tables:
            self.db.execute_query(table)

    def display_menu(self):
        """Foydalanuvchi menyusi."""
        print(""" 
1. Ma'lumotlarni ko'rish
2. Ma'lumot qo'shish
3. Ma'lumotni o'zgartirish
4. Ma'lumotni o'chirish
5. Chiqish
""")

    def view_data(self):
        """Jadval ma'lumotlarini ko'rish."""
        table = input("Qaysi jadvalni ko'rmoqchisiz? (masalan: students, users): ")
        query = f"SELECT * FROM {table}"
        records = self.db.fetch_all(query)
        if records:
            for record in records:
                print(record)
        else:
            print("Jadval bo'sh yoki noto'g'ri nom kiritildi!")

    def add_data(self):
        """Jadvalga ma'lumot qo'shish."""
        table = input("Qaysi jadvalga ma'lumot qo'shmoqchisiz? (masalan: students, users): ")
        columns = self.db.get_columns(table)
        print(f"{table} jadvalidagi maydonlar: {', '.join(columns)}")
        
        # Foydalanuvchidan maydonlar va qiymatlar so'rash
        fields = input(f"Maydonlarni kiriting ({', '.join(columns)}): ").split(",")
        # Maydonlar to'g'riligi tekshiruvi
        if not all(field in columns for field in fields):
            print("Xato! Kiritilgan maydonlar noto'g'ri.")
            return
        
        values = input("Qiymatlarni kiriting (vergul bilan): ").split(",")
        if len(fields) != len(values):
            print("Xato! Qiymatlar soni maydonlar soniga mos kelmaydi.")
            return

        placeholders = ",".join(["?" for _ in values])
        query = f"INSERT INTO {table} ({','.join(fields)}) VALUES ({placeholders})"
        self.db.execute_query(query, values)
        print("Ma'lumot muvaffaqiyatli qo'shildi!")

    def update_data(self):
        """Jadvaldagi ma'lumotni o'zgartirish."""
        table = input("Qaysi jadvalda ma'lumotni o'zgartirmoqchisiz? (masalan: students, users): ")
        columns = self.db.get_columns(table)
        print(f"{table} jadvalidagi maydonlar: {', '.join(columns)}")
        
        field = input("Qaysi maydonni o'zgartirmoqchisiz? (masalan: email): ")
        if field not in columns:
            print("Xato! Maydon nomi noto'g'ri.")
            return
        
        new_value = input("Yangi qiymatni kiriting: ")
        condition = input("Qaysi shart asosida o'zgartirasiz? (masalan: id=1): ")
        query = f"UPDATE {table} SET {field} = ? WHERE {condition}"
        self.db.execute_query(query, (new_value,))
        print("Ma'lumot muvaffaqiyatli o'zgartirildi!")

    def delete_data(self):
        """Jadvaldagi ma'lumotni o'chirish."""
        table = input("Qaysi jadvalda ma'lumotni o'chirmoqchisiz? (masalan: students, users): ")
        condition = input("Qaysi shart asosida o'chirasiz? (masalan: id=1): ")
        query = f"DELETE FROM {table} WHERE {condition}"
        self.db.execute_query(query)
        print("Ma'lumot muvaffaqiyatli o'chirildi!")

    def run(self):
        """Dastur ishga tushirilishi."""
        while True:
            self.display_menu()
            choice = input("Tanlovingizni kiriting (1-5): ")
            if choice == "1":
                self.view_data()
            elif choice == "2":
                self.add_data()
            elif choice == "3":
                self.update_data()
            elif choice == "4":
                self.delete_data()
            elif choice == "5":
                print("Chiqish...")
                break
            else:
                print("Noto'g'ri tanlov, qayta urinib ko'ring!")


if __name__ == "__main__":
    app = UniversityApp()
    app.run()
