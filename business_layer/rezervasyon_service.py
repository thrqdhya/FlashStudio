from data_access_layer.rezervasyon_dal import RezervasyonDAL

class RezervasyonService:
    @staticmethod
    def yeni_rezervasyon_kaydet(musteri_id, fotografci_id, paket_id, randevu_tarihi, toplam_tutar, kapora):
        if not musteri_id or not paket_id or not randevu_tarihi:
            return False, "Müşteri, Paket ve Randevu Tarihi alanları zorunludur!"
            
        # PEMBERSIHAN TOTAL: Jika fotografci_id berisi string kosong, "None", 
        # atau teks petunjuk bawaan select, kita paksa menjadi None (NULL)
        if not fotografci_id or str(fotografci_id).strip() == "" or fotografci_id == "None" or "isteğe" in str(fotografci_id).lower():
            fotografci_id = None

        try:
            RezervasyonDAL.rezervasyon_ekle(musteri_id, fotografci_id, paket_id, randevu_tarihi, toplam_tutar, kapora)
            return True, "Rezervasyon başarıyla veritabanına kaydedildi."
        except Exception as e:
            return False, f"Rezervasyon eklenirken hata oluştu: {str(e)}"

    @staticmethod
    def tum_rezervasyonlari_getir():
        try:
            return RezervasyonDAL.rezervasyon_getir_hepsi()
        except Exception:
            return []