from main import db_file_path
import sqlite3
from datetime import datetime


class UsersDatabase:
    db_name=db_file_path("ticher_db.db")
    def __init__(self):
        """Bazaga ulanish va jadvalni yaratish."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Ticher jadvalini yaratadi."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                familya TEXT NOT NULL,
                ismi TEXT NOT NULL,
                otasining_ismi TEXT NOT NULL,
                jinsi TEXT NOT NULL,
                millati TEXT NOT NULL,
                ogirligi REAL NOT NULL,
                tugilgan_sanasi TEXT NOT NULL,
                saqlangan_vaqti TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def insert_data(self, familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sanasi):
        """Yangi ma’lumot kiritish."""
        saqlangan_vaqti = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO ticher (familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sanasi, saqlangan_vaqti)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sanasi, saqlangan_vaqti))
        self.conn.commit()

    def view_data(self):
        """Ma’lumotlarni ko’rish."""
        self.cursor.execute("SELECT * FROM ticher")
        return self.cursor.fetchall()

    def update_data(self, id, column, new_value):
        """Ma’lumotni yangilash."""
        query = f"UPDATE ticher SET {column} = ? WHERE id = ?"
        self.cursor.execute(query, (new_value, id))
        self.conn.commit()

    def delete_data(self, id):
        """Ma’lumotni o’chirish."""
        self.cursor.execute("DELETE FROM ticher WHERE id = ?", (id,))
        self.conn.commit()

    def count_data(self):
        """Jadvaldagi ma’lumotlar sonini qaytarish."""
        self.cursor.execute("SELECT COUNT(*) FROM ticher")
        return self.cursor.fetchone()[0]

    def close_connection(self):
        """Bazani ulanishini yopish."""
        self.conn.close()


def main():
    db = UsersDatabase()

    while True:
        print("\nMenyu:")
        print("1. Yangi ma’lumot qo’shish")
        print("2. Ma’lumotlarni ko’rish")
        print("3. Ma’lumotni yangilash")
        print("4. Ma’lumotni o’chirish")
        print("5. Ma’lumotlar sonini ko’rish")
        print("6. Chiqish")

        choice = input("Tanlovni kiriting: ")

        if choice == "1":
            familya = input("Familya: ")
            ismi = input("Ismi: ")
            otasining_ismi = input("Otasining ismi: ")
            jinsi = input("Jinsi (Erkak/Ayol): ")
            millati = input("Millati: ")
            ogirligi = float(input("Og’irligi (kg): "))
            tugilgan_sanasi = input("Tug’ilgan sanasi (YYYY-MM-DD): ")
            db.insert_data(familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sanasi)
            print("Ma’lumot muvaffaqiyatli qo’shildi!")

        elif choice == "2":
            data = db.view_data()
            if data:
                for row in data:
                    print(row)
            else:
                print("Jadvalda ma’lumot yo’q!")

        elif choice == "3":
            id = int(input("Yangilamoqchi bo’lgan ma’lumot ID raqamini kiriting: "))
            column = input("Yangilamoqchi bo’lgan ustun nomini kiriting (familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sanasi): ")
            new_value = input("Yangi qiymatni kiriting: ")
            db.update_data(id, column, new_value)
            print("Ma’lumot muvaffaqiyatli yangilandi!")

        elif choice == "4":
            id = int(input("O’chirmoqchi bo’lgan ma’lumot ID raqamini kiriting: "))
            db.delete_data(id)
            print("Ma’lumot muvaffaqiyatli o’chirildi!")

        elif choice == "5":
            count = db.count_data()
            print(f"Jadvaldagi umumiy ma’lumotlar soni: {count}")

        elif choice == "6":
            db.close_connection()
            print("Dasturni tugatildi.")
            break

        else:
            print("Noto’g’ri tanlov! Iltimos, qaytadan urinib ko’ring.")


if __name__ == "__main__":
    main()
