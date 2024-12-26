import sqlite3
from datetime import datetime
import os
from main import db_file_path
class DatabaseManager:
    DB_NAME =db_file_path('inson_db.db')

    def __init__(self):
        """Bazaga ulanish va jadval yaratish."""
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Jadvalni yaratadi agar mavjud bo'lmasa."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inson (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                familya TEXT NOT NULL,
                ism TEXT NOT NULL,
                otasi_ismi TEXT NOT NULL,
                jinsi TEXT NOT NULL,
                millati TEXT NOT NULL,
                boyi INTEGER NOT NULL,
                tugilgan_sana TEXT NOT NULL,
                saqlangan_vaqt TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_record(self, familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana):
        """Yangi yozuv qo'shadi."""
        saqlangan_vaqt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO inson (familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana, saqlangan_vaqt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana, saqlangan_vaqt))
        self.conn.commit()

    def delete_record(self, record_id):
        """Ma'lumotni ID bo'yicha o'chiradi."""
        self.cursor.execute("DELETE FROM inson WHERE id = ?", (record_id,))
        self.conn.commit()

    def update_record(self, record_id, familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana):
        """Ma'lumotni yangilaydi."""
        self.cursor.execute('''
            UPDATE inson 
            SET familya = ?, ism = ?, otasi_ismi = ?, jinsi = ?, millati = ?, boyi = ?, tugilgan_sana = ?
            WHERE id = ?
        ''', (familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana, record_id))
        self.conn.commit()

    def read_records(self):
        """Barcha yozuvlarni o'qiydi."""
        self.cursor.execute("SELECT * FROM inson")
        return self.cursor.fetchall()
    def get_all_ids(self):
        """Barcha foydalanuvchi IDlarini olish."""
        self.cursor.execute("SELECT id FROM inson")
        rows = self.cursor.fetchall()
        # Faqat ID maydonlarini listga qo'shish
        id_list = [row[0] for row in rows]
        return id_list
    def count_records(self):
        """Yozuvlar sonini qaytaradi."""
        self.cursor.execute("SELECT COUNT(*) FROM inson")
        return self.cursor.fetchone()[0]
    def search_by_familya(self, familya):
        """Familya bo'yicha qidirish."""
        self.cursor.execute("SELECT * FROM inson WHERE familya LIKE ?", (f"%{familya}%",))
        return self.cursor.fetchall()

    def search_by_ism(self, ism):
        """Ism bo'yicha qidirish."""
        self.cursor.execute("SELECT * FROM inson WHERE ism LIKE ?", (f"%{ism}%",))
        return self.cursor.fetchall()

    def search_by_jinsi(self, jinsi):
        """Jinsi bo'yicha qidirish."""
        self.cursor.execute("SELECT * FROM inson WHERE jinsi = ?", (jinsi,))
        return self.cursor.fetchall()

    def search_by_boyi(self, boyi_min, boyi_max):
        """Bo'yi oralig'ida qidirish."""
        self.cursor.execute("SELECT * FROM inson WHERE boyi BETWEEN ? AND ?", (boyi_min, boyi_max))
        return self.cursor.fetchall()

    def search_by_tugilgan_sana(self, tugilgan_sana):
        """Tug'ilgan sana bo'yicha qidirish."""
        self.cursor.execute("SELECT * FROM inson WHERE tugilgan_sana = ?", (tugilgan_sana,))
        return self.cursor.fetchall()

    def close_connection(self):
        """Bazaga ulanishni yopadi."""
        self.conn.close()


# Menyu interfeysi
def main_menu():
    db_manager = DatabaseManager()
    try:
        while True:
            os.system('color D')
            print("\n=== Ma'lumotlar Bazasi Boshqaruvi ===")
            print("1. Yangi ma'lumot qo'shish")
            print("2. Ma'lumotni o'chirish")
            print("3. Ma'lumotni yangilash")
            print("4. Barcha ma'lumotlarni ko'rish")
            print("5. Ma'lumotlar sonini ko'rish")
            print("6. Jadvladiga ma`lumotlar ids")
            print("7. Dasturdan chiqish")
            print("8. Ma'lumotlarni qidirish")
            choice = input("Tanlovingiz: ")
            if not choice:
                continue
            if choice == '1':
                familya = str(input("Familya: "))
                if not familya:
                    continue
                ism = str(input("Ism: "))
                if not ism:
                    continue
                otasi_ismi = str(input("Otasi ismi: "))
                if not otasi_ismi:
                    continue
                jinsi = str(input("Jinsi (Erkak/Ayol): "))
                if not jinsi:
                    continue
                millati = str(input("Millati: "))
                if not millati:
                    continue
                boyi = int(input("Bo'yi (sm): "))
                if not boyi:
                    continue
                tugilgan_sana = str(input("Tug'ilgan sana (YYYY-MM-DD): "))
                if not tugilgan_sana:
                    continue
                db_manager.add_record(familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana)
                print("Ma'lumot muvaffaqiyatli qo'shildi!")

            elif choice == '2':
                record_id = int(input("O'chirish uchun ID ni kiriting: "))
                db_manager.delete_record(record_id)
                print("Ma'lumot muvaffaqiyatli o'chirildi!")

            elif choice == '3':
                record_id = int(input("Yangilash uchun ID ni kiriting: "))
                if not record_id:
                    continue
                familya = str(input("Familya: "))
                if not familya:
                    continue
                ism = str(input("Ism: "))
                if not ism:
                    continue
                otasi_ismi = str(input("Otasi ismi: "))
                if not otasi_ismi:
                    continue
                jinsi = str(input("Jinsi (Erkak/Ayol): "))
                if not jinsi:
                    continue
                millati = str(input("Millati: "))
                if not millati:
                    continue
                boyi = int(input("Bo'yi (sm): "))
                if not boyi:
                    continue
                tugilgan_sana = str(input("Tug'ilgan sana (YYYY-MM-DD): "))
                if not tugilgan_sana:
                    continue
                db_manager.update_record(record_id, familya, ism, otasi_ismi, jinsi, millati, boyi, tugilgan_sana)
                print("Ma'lumot muvaffaqiyatli yangilandi!")

            elif choice == '4':
                records = db_manager.read_records()
                print("\nJadvaldagi barcha ma'lumotlar:")
                for record in records:
                    print(record)

            elif choice == '5':
                count = db_manager.count_records()
                print(f"Jadvaldagi ma'lumotlar soni: {count}")
            elif choice =='6':
                ids= db_manager.get_all_ids()
                print(f"Jadvladagi userlarning ids: {ids}")
            elif choice == '7':
                print("Dastur toxtatildi.")
                break
            elif choice == '8':
                print("\n=== Qidiruv menyusi ===")
                print("1. Familya bo'yicha qidirish")
                print("2. Ism bo'yicha qidirish")
                print("3. Jinsi bo'yicha qidirish")
                print("4. Bo'yi oralig'ida qidirish")
                print("5. Tug'ilgan sana bo'yicha qidirish")
                search_choice = input("Qidirish uchun tanlovingiz: ")

                if search_choice == '1':
                    familya = input("Familya kiriting: ")
                    if not familya:
                        continue
                    results = db_manager.search_by_familya(familya)
                elif search_choice == '2':
                    ism = input("Ism kiriting: ")
                    if not ism:
                        continue
                    results = db_manager.search_by_ism(ism)
                elif search_choice == '3':
                    jinsi = input("Jinsi kiriting (Erkak/Ayol): ")
                    if not jinsi:
                        continue
                    results = db_manager.search_by_jinsi(jinsi)
                elif search_choice == '4':
                    boyi_min = int(input("Minimal bo'yi (sm): "))
                    if not boyi_min:
                        continue
                    boyi_max = int(input("Maksimal bo'yi (sm): "))
                    if not boyi_max:
                        continue
                    results = db_manager.search_by_boyi(boyi_min, boyi_max)
                elif search_choice == '5':
                    tugilgan_sana = input("Tug'ilgan sana (YYYY-MM-DD): ")
                    if not tugilgan_sana:
                        continue
                    results = db_manager.search_by_tugilgan_sana(tugilgan_sana)
                else:
                    print("Noto'g'ri tanlov!")
                    continue

                # Natijalarni chiqarish
                if results:
                    print("\nQidiruv natijalari:")
                    for record in results:
                        print(record)
                else:
                    print("Hech qanday ma'lumot topilmadi.")

            else:
                print("Noto'g'ri tanlov. Qayta urinib ko'ring.!")

    finally:
        db_manager.close_connection()


if __name__ == "__main__":
    main_menu()
