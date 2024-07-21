class StokHareketleriService:
    def __init__(self, giris_fisi_repository, cikis_fisi_repository):
        self.giris_fisi_repository = giris_fisi_repository
        self.cikis_fisi_repository = cikis_fisi_repository

    def get_stok_hareketleri(self):
        giris_fisleri = self.giris_fisi_repository.get_all_fis_details()
        cikis_fisleri = self.cikis_fisi_repository.get_all_fis_details()

        stok_hareketleri = giris_fisleri + cikis_fisleri
        stok_hareketleri.sort(key=lambda x: x[1])  # Tarihe göre sırala

        return stok_hareketleri

    def get_all_fis_details(self):
        giris_fisleri = self.giris_fisi_repository.get_all_fis_details()
        cikis_fisleri = self.cikis_fisi_repository.get_all_fis_details()

        # Giriş ve Çıkış Fişlerini birleştir
        fis_details = giris_fisleri + cikis_fisleri
        return fis_details