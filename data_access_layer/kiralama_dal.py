from data_access_layer.db_connection import get_db_connection

class KiralamaDAL:
    @staticmethod
    def kiralama_ekle(musteri_id, baslangic_tarihi, bitis_tarihi, toplam_kira):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Memanggil sp_KiralamaEkle
            cursor.execute("{CALL sp_KiralamaEkle (?, ?, ?, ?)}", (musteri_id, baslangic_tarihi, bitis_tarihi, toplam_kira))
            conn.commit()
            conn.close()