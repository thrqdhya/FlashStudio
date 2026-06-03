from data_access_layer.db_connection import get_db_connection

class EkipmanDAL:
    @staticmethod
    def ekipman_ekle(ad, kategori, fiyat, stok, birim, detay):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            durum_default = "Mevcut"
            
            # SESUAI SP SSMS:
            # ? ke-1: @marka  -> ad
            # ? ke-2: @model  -> kategori
            # ? ke-3: @tur    -> birim (Input dari form Birimi (Tür))
            # ? ke-4: @kira   -> fiyat (Input dari form Kira Ücreti)
            # ? ke-5: @durum  -> durum_default ("Mevcut")
            
            cursor.execute(
                "{CALL sp_EkipmanEkle (?, ?, ?, ?, ?)}", 
                (ad, kategori, birim, fiyat, durum_default)
            )
            
            conn.commit()
            conn.close()

    @staticmethod
    def ekipman_getir_hepsi():
        conn = get_db_connection()
        ekipmanlar = []
        if conn:
            cursor = conn.cursor()
            try:
                # Memanggil sp_EkipmanHepsi yang mengembalikan kolom sesuai struktur tabel database
                cursor.execute("{CALL sp_EkipmanHepsi}")
                rows = cursor.fetchall()
                for row in rows:
                    ekipmanlar.append({
                        'id': row[0],        # Primary Key (ID) untuk tombol Sil
                        'ad': row[1],        # @marka -> Nama Alat
                        'kategori': row[2],  # @model -> Kategori
                        'birim': row[3],     # @tur   -> Menampilkan Tür di kolom yang pas
                        'fiyat': row[4],     # @kira  -> Menampilkan Kira Ücreti asli (1000 TL)
                        'stok': row[5] if len(row) > 5 else 'Mevcut', # @durum -> Status ketersediaan
                        'detay': 'Aktif'
                    })
            except Exception:
                pass
            conn.close()
        return ekipmanlar

    @staticmethod
    def ekipman_sil(id):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Memanggil sp_EkipmanSil menggunakan ID komponen asli (row[0])
            cursor.execute("{CALL sp_EkipmanSil (?)}", (id,))
            conn.commit()
            conn.close()