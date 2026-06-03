from data_access_layer.db_connection import get_db_connection

class MusteriDAL:
    @staticmethod
    def musteri_ekle(ad, soyad, telefon, eposta, adres):
        # Membuka koneksi ke MS SQL Server kamu
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Mengeksekusi Stored Procedure sp_MusteriEkle sesuai dengan database-mu
            cursor.execute(
                "{CALL sp_MusteriEkle (?, ?, ?, ?, ?)}", 
                (ad, soyad, telefon, eposta, adres)
            )
            conn.commit()
            conn.close()

    @staticmethod
    def musteri_getir_hepsi():
        conn = get_db_connection()
        musteriler = []
        if conn:
            cursor = conn.cursor()
            # Memanggil Stored Procedure untuk melihat daftar pelanggan
            cursor.execute("{CALL sp_MusteriHepsi}")
            rows = cursor.fetchall()
            for row in rows:
                musteriler.append({
                    'id': row[0],
                    'ad': row[1],
                    'soyad': row[2],
                    'telefon': row[3],
                    'eposta': row[4],
                    'adres': row[5]
                })
            conn.close()
        return musteriler

    @staticmethod
    def musteri_sil(id):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("{CALL sp_MusteriSil (?)}", (id,))
            conn.commit()
            conn.close()