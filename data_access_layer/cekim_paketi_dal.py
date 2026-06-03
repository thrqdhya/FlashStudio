from data_access_layer.db_connection import get_db_connection

class CekimPaketiDAL:
    @staticmethod
    def paket_getir_hepsi():
        conn = get_db_connection()
        paketler = []
        if conn:
            cursor = conn.cursor()
            try:
                # Memanggil stored procedure bawaan database kamu
                cursor.execute("{CALL sp_CekimPaketiHepsi}")
                rows = cursor.fetchall()
                for row in rows:
                    paketler.append({
                        'id': row[0],
                        'ad': row[1] if len(row) > 1 else '',
                        'fiyat': row[2] if len(row) > 2 else 0
                    })
            except Exception:
                pass
            conn.close()
        return paketler