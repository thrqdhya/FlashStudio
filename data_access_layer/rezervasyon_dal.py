from data_access_layer.db_connection import get_db_connection

class RezervasyonDAL:
    @staticmethod
    def rezervasyon_ekle(musteri_id, fotografci_id, paket_id, randevu_tarihi, toplam_tutar, kapora):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # 1. FORMAT TANGGAL: Mengubah huruf 'T' dari input datetime-local HTML menjadi spasi
            # agar formatnya menjadi 'YYYY-MM-DD HH:MM:00' yang valid untuk SQL Server
            if randevu_tarihi and "T" in randevu_tarihi:
                randevu_tarihi = randevu_tarihi.replace("T", " ") + ":00"
            
            # 2. PEMBERSIHAN FOREIGN KEY: Jika tidak memilih fotografer (opsional), 
            # paksa nilainya menjadi None agar masuk sebagai NULL asli di database
            if not fotografci_id or str(fotografci_id).strip() == "" or fotografci_id == "None":
                fotografci_id = None
                
            try:
                # Mengeksekusi Stored Procedure sp_RezervasyonEkle bawaan database
                cursor.execute(
                    "{CALL sp_RezervasyonEkle (?, ?, ?, ?, ?, ?)}",
                    (musteri_id, fotografci_id, paket_id, randevu_tarihi, toplam_tutar, kapora)
                )
                conn.commit()
            except Exception as e:
                conn.close()
                raise e
                
            conn.close()

    @staticmethod
    def rezervasyon_getir_hepsi():
        conn = get_db_connection()
        rezervasyonlar = []
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("{CALL sp_RezervasyonDetay}")
                
                # SAKTI: Mengambil list nama kolom langsung dari database
                columns = [column[0].lower() for column in cursor.description]
                
                rows = cursor.fetchall()
                for row in rows:
                    # Membuat dictionary dinamis antara nama kolom dan nilainya
                    row_dict = dict(zip(columns, row))
                    
                    # Kita cari kolom secara fleksibel menggunakan kata kunci nama kolomnya
                    # Solusi ini menangani jika nama kolomnya menggunakan bahasa Turki / Inggris
                    id_res = row_dict.get('rezervasyonid') or row[0]
                    
                    # Mencari nama pelanggan (Müşteri Adı Soyadı)
                    musteri_ad = row_dict.get('müşteri ad soyad') or row_dict.get('musteri_ad_soyad') or row_dict.get('musteri')
                    
                    # Mencari nama fotografer (Fotoğrafçı)
                    fotografci_ad = row_dict.get('fotoğrafçı') or row_dict.get('fotografci_ad_soyad') or row_dict.get('fotografci')
                    
                    # Mencari nama paket (Seçilen Paket)
                    paket_ad = row_dict.get('seçilen paket') or row_dict.get('paket_adi') or row_dict.get('paket')
                    
                    # Jika deteksi nama kolom gagal, kita pakai fallback indeks yang digeser manual
                    if not musteri_ad:
                        # Jika indeks bergeser, coba ambil Thoriq Dhiya di baris yang tepat
                        musteri_ad = row[2] if len(row) > 2 else 'Bilinmeyen Müşteri'
                        fotografci_ad = row[3] if len(row) > 3 else 'İsteğe Bağlı'
                        paket_ad = row[4] if len(row) > 4 else 'Paket Yok'
                    
                    # Mengambil data keuangan secara dinamis
                    toplam_tutar = float(row_dict.get('toplam fiyat') or row_dict.get('toplam_tutar') or row[6] or 0.0)
                    kapora_tutari = float(row_dict.get('ödenen kapora') or row_dict.get('kapora') or row[7] or 0.0)
                    kalan_borc = float(row_dict.get('kalan borç') or row_dict.get('kalan_borc') or row[8] or (toplam_tutar - kapora_tutari))

                    # Format tanggal
                    tarih_obj = row_dict.get('çekim tarihi') or row_dict.get('randevu_tarihi') or row[5]
                    if tarih_obj and hasattr(tarih_obj, 'strftime'):
                        tarih_str = tarih_obj.strftime('%d/%m/%Y %H:%M')
                    else:
                        tarih_str = str(tarih_obj) if tarih_obj else 'Tarih Belirtilmedi'

                    rezervasyonlar.append({
                        'id': id_res,
                        'musteri_ad': musteri_ad,
                        'fotografci_ad': fotografci_ad if fotografci_ad else 'İsteğe Bağlı',
                        'paket_ad': paket_ad,
                        'tarih': tarih_str,
                        'toplam': toplam_tutar,
                        'kapora': kapora_tutari,
                        'kalan': kalan_borc
                    })
            except Exception as e:
                print(f"DAL Tampilan Reservasi Error: {str(e)}")
            finally:
                conn.close()
        return rezervasyonlar