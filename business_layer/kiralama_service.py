from data_access_layer.kiralama_dal import KiralamaDAL

class KiralamaService:
    @staticmethod
    def kiralama_ekle(musteri_id, baslangic_tarihi, bitis_tarihi, toplam_tutar):
        # Sesuaikan pemanggilan ke KiralamaDAL kamu
        # Contoh jika nama DAL kamu adalah KiralamaDAL:
        from data_access_layer.kiralama_dal import KiralamaDAL
        return KiralamaDAL.kiralama_ekle(musteri_id, baslangic_tarihi, bitis_tarihi, toplam_tutar)