from data_access_layer.musteri_dal import MusteriDAL

class MusteriService:
    @staticmethod
    def yeni_musteri_kaydet(ad, soyad, telefon, eposta, adres):
        # Validasi dasar: Memastikan input wajib tidak kosong
        if not ad or not soyad or not telefon:
            return False, "Ad, Soyad ve Telefon alanları boş bırakılamaz!"
        
        try:
            # Di sini kita panggil fungsi musteri_ekle yang sudah sinkron dengan DAL
            MusteriDAL.musteri_ekle(ad, soyad, telefon, eposta, adres)
            return True, "Müşteri başarıyla veritabanına kaydedildi."
        except Exception as e:
            # Jika ada masalah koneksi atau query, pesan error ditangkap di sini
            return False, f"Hata oluştu: {str(e)}"

    @staticmethod
    def tum_musterileri_listele():
        try:
            return MusteriDAL.musteri_getir_hepsi()
        except Exception:
            return []

    @staticmethod
    def m_musteri_sil(id):
        try:
            MusteriDAL.musteri_sil(id)
            return True
        except Exception:
            return False