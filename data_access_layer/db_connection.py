import pyodbc

def get_db_connection():
    try:
        # Koneksi menggunakan Windows Authentication ke SQLEXPRESS milikmu
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=FlashStudioDB;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None