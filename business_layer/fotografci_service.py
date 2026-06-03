from data_access_layer.fotografci_dal import FotografciDAL

class FotografciService:
    @staticmethod
    def yeni_fotografci_kaydet(ad, soyad, uzmanlik, tel):
        if not ad or not soyad or not uzmanlik:
            return False, "Ad, Soyad ve Uzmanlık alanları boş bırakılamaz!"
        try:
            FotografciDAL.fotografci_ekle(ad, soyad, uzmanlik, tel)
            return True, "Fotoğrafçı başarıyla sisteme kaydedildi."
        except Exception as e:
            return False, f"Kayıt hatası: {str(e)}"

    @staticmethod
    def tum_fotografcilari_listele():
        return FotografciDAL.fotografci_getir_hepsi()