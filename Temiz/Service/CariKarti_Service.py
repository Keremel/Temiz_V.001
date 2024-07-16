# Service/CariKarti_Service.py
from Temiz.Repository.CariKarti_Repository import CariKartiRepository


class CariKartiService:
    def __init__(self, repository: CariKartiRepository):
        self.repository = repository

    def save_cari_karti(self, cari_karti):
        self.repository.save(cari_karti)

    def update_cari_karti(self, cari_karti):
        self.repository.update(cari_karti)

    def get_all_cariler(self):
        return self.repository.find_all()

    def get_cari_by_ad(self, cari_ad):
        return self.repository.find_by_ad(cari_ad)

    def get_cari_by_kod(self, cari_kod):
        return self.repository.find_by_kod(cari_kod)

    def generate_new_cari_kod(self):
        return self.repository.generate_new_cari_kod()

    def is_cari_ad_exists(self, cari_ad):
        cariler = self.repository.find_by_ad(cari_ad)
        return cariler is not None
