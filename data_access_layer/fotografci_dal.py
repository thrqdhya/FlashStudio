from data_access_layer.db_connection import get_db_connection

class FotografciDAL:
    @staticmethod
    def fotografci_ekle(ad, soyad, uzmanlik, tel):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Memanggil Stored Procedure sp_FotografciEkle di MSSQL kamu
            cursor.execute("{CALL sp_FotografciEkle (?, ?, ?, ?)}", (ad, soyad, uzmanlik, tel))
            conn.commit()
            conn.close()

    @staticmethod
    def fotografci_getir_hepsi():
        conn = get_db_connection()
        fotografcilar = []
        if conn:
            cursor = conn.cursor()
            # Memanggil Stored Procedure sp_FotografciHepsi di MSSQL kamu
            cursor.execute("{CALL sp_FotografciHepsi}")
            rows = cursor.fetchall()
            for row in rows:
                fotografcilar.append({
                    'id': row[0],
                    'ad': row[1],
                    'soyad': row[2],
                    'uzmanlik': row[3],
                    'telefon': row[4]
                })
            conn.close()
        return fotografcilar