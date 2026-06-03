from data_access_layer.cekim_paketi_dal import CekimPaketiDAL

class CekimPaketiService:
    @staticmethod
    def tum_cekim_paketlerini_listele():
        return CekimPaketiDAL.paket_getir_hepsi()