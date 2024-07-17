class StokHareketleriService:
    def __init__(self, giris_fisi_repository, cikis_fisi_repository):
        self.giris_fisi_repository = giris_fisi_repository  # Bu satırı düzelttik
        self.cikis_fisi_repository = cikis_fisi_repository

    def get_all_fis_details(self):
        giris_fisleri = self.giris_fisi_repository.get_all_fis_details()
        cikis_fisleri = self.cikis_fisi_repository.get_all_fis_details()
        return giris_fisleri + cikis_fisleri

    def get_all_stok_hareketleri(self):
        # Eğer başka bir metod eklemek isterseniz, buraya ekleyebilirsiniz.
        pass
