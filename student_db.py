from main import db_file_path
from datetime import datetime
import sqlite3
from tabulate import tabulate

class StudentDatabase:
    db_name = db_file_path("student_db.db")

    def __init__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            familya TEXT,
            ismi TEXT,
            otasining_ismi TEXT,
            jinsi TEXT,
            millati TEXT,
            ogirligi REAL,
            tugilgan_sana DATE,
            oliy_oquv_yurti TEXT,
            fakultet TEXT,
            kurs INTEGER,
            ortacha_bal REAL,
            saqlangan_vaqt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def add_student(self, familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sana, oliy_oquv_yurti, fakultet, kurs, ortacha_bal):
        try:
            tugilgan_sana = datetime.strptime(tugilgan_sana, "%Y-%m-%d").date()
            query = """
            INSERT INTO student (familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sana, oliy_oquv_yurti, fakultet, kurs, ortacha_bal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sana, oliy_oquv_yurti, fakultet, kurs, ortacha_bal))
            self.connection.commit()
        except ValueError:
            print("Xatolik: Tug'ilgan sana noto'g'ri formatda (to'g'ri format: YYYY-MM-DD).")

    def view_students(self):
        query = "SELECT * FROM student"
        self.cursor.execute(query)
        students = self.cursor.fetchall()
        headers = ["ID", "Familya", "Ismi", "Otasining_ismi", "Jinsi", "Millati", "Og'irligi", "Tug'ilgan_sana", 
                   "Oliy_o'quv_yurti", "Fakultet", "Kurs", "O'rtacha_bal", "Saqlangan vaqt"]
        print(tabulate(students, headers=headers, tablefmt="grid"))

    def update_student(self, student_id, updates):
        update_clauses = ", ".join([f"{key} = ?" for key in updates.keys()])
        query = f"UPDATE student SET {update_clauses}, saqlangan_vaqt = CURRENT_TIMESTAMP WHERE id = ?"
        self.cursor.execute(query, (*updates.values(), student_id))
        self.connection.commit()

    def delete_student(self, student_id):
        query = "DELETE FROM student WHERE id = ?"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()

    def delete_all_students(self):
        query = "DELETE FROM student"
        self.cursor.execute(query)
        self.connection.commit()
        print("Barcha talaba ma'lumotlari o'chirildi!")

    def count_students(self):
        query = "SELECT COUNT(*) FROM student"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_last_saved_time(self, student_id):
        query = "SELECT saqlangan_vaqt FROM student WHERE id = ?"
        self.cursor.execute(query, (student_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close_connection(self):
        self.connection.close()


def main_menu():
    db = StudentDatabase()

    while True:
        print("\n--- Talaba Bazasi Menyusi ---")
        print("1. Yangi talaba qo'shish")
        print("2. Barcha talabalarning ma'lumotlarini ko'rish")
        print("3. Talaba ma'lumotlarini yangilash")
        print("4. Talaba ma'lumotlarini o'chirish")
        print("5. Barcha talabalarni o'chirish")
        print("6. Bazadagi talabalar sonini ko'rish")
        print("7. Talabaning oxirgi saqlangan vaqtini ko'rish")
        print("8. Dasturni yopish")

        choice = input("Tanlovingizni kiriting (1-8): ")

        if choice == "1":
            print("\nTalaba ma'lumotlarini kiriting:")
            familya = input("Familya: ")
            ismi = input("Ismi: ")
            otasining_ismi = input("Otasining ismi: ")
            jinsi = input("Jinsi: ")
            millati = input("Millati: ")
            ogirligi = float(input("Og'irligi (kg): "))
            tugilgan_sana = input("Tug'ilgan sanasi (YYYY-MM-DD): ")
            oliy_oquv_yurti = input("Oliy o'quv yurtining nomi: ")
            fakultet = input("Fakultet: ")
            kurs = int(input("Kurs: "))
            ortacha_bal = float(input("O'rtacha bal: "))
            db.add_student(familya, ismi, otasining_ismi, jinsi, millati, ogirligi, tugilgan_sana, oliy_oquv_yurti, fakultet, kurs, ortacha_bal)
            print("Talaba muvaffaqiyatli qo'shildi!")

        elif choice == "2":
            print("\nBarcha talabalar ma'lumotlari:")
            db.view_students()

        elif choice == "3":
            student_id = int(input("\nYangilanishi kerak bo'lgan talabaning ID raqamini kiriting: "))
            updates = {}
            print("Yangilanishlarni kiriting (masalan: familya=Yangi):")
            while True:
                key = input("Maydon nomi (yoki 'stop' tugatish uchun): ")
                if key.lower() == "stop":
                    break
                value = input("Yangi qiymat: ")
                updates[key] = value
            db.update_student(student_id, updates)
            print("Talaba ma'lumotlari yangilandi!")

        elif choice == "4":
            student_id = int(input("\nO'chirilishi kerak bo'lgan talabaning ID raqamini kiriting: "))
            db.delete_student(student_id)
            print("Talaba muvaffaqiyatli o'chirildi!")

        elif choice == "5":
            confirm = input("Barcha talabalarni o'chirishni xohlaysizmi? (ha/yo'q): ").lower()
            if confirm == "ha":
                db.delete_all_students()

        elif choice == "6":
            count = db.count_students()
            print(f"\nBazadagi talabalar soni: {count}")

        elif choice == "7":
            student_id = int(input("\nOxirgi saqlangan vaqtini ko'rmoqchi bo'lgan talabaning ID raqamini kiriting: "))
            saved_time = db.get_last_saved_time(student_id)
            if saved_time:
                print(f"Talaba oxirgi saqlangan vaqt: {saved_time}")
            else:
                print("Bunday ID raqamli talaba topilmadi!")

        elif choice == "8":
            db.close_connection()
            print("Dastur yopildi. Xayr!")
            break

        else:
            print("Noto'g'ri tanlov! Iltimos, qayta urinib ko'ring.")


if __name__ == "__main__":
    main_menu()
