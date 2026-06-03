from data_access_layer.ekipman_dal import EkipmanDAL

class EkipmanService:
    @staticmethod
    def yeni_ekipman_kaydet(ad, kategori, fiyat, stok, birim, detay):
        if not ad or not kategori or not fiyat:
            return False, "Ekipman Adı, Kategori ve Kira Ücreti alanları boş bırakılamaz!"
        try:
            EkipmanDAL.ekipman_ekle(ad, kategori, float(fiyat), float(stok), birim, detay)
            return True, "Ekipman başarıyla veritabanına kaydedildi."
        except Exception as e:
            return False, f"Kayıt Hatası: {str(e)}"

    @staticmethod
    def tum_ekipmanlari_listele():
        return EkipmanDAL.ekipman_getir_hepsi()

    # YENİ: Silme Servisi
    @staticmethod
    def m_ekipman_sil(id):
        try:
            EkipmanDAL.ekipman_sil(id)
            return True, "Ekipman başarıyla veritabanından silindi."
        except Exception as e:
            return False, f"Silme işlemi başarısız: {str(e)}"