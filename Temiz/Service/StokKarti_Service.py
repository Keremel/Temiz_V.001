# Service/StokKarti_Service.py
from Temiz.Repository.StokKarti_Repository import StokKartiRepository

class StokKartiService:
    def __init__(self, repository: StokKartiRepository):
        self.repository = repository

    def save_stok_karti(self, stok_karti):
        self.repository.save(stok_karti)

    def update_stok_karti(self, stok_karti):
        self.repository.update(stok_karti)

    def get_all_stoklar(self):
        return self.repository.find_all()

    def generate_new_stok_kod(self):
        return self.repository.generate_new_stok_kod()

    def find_by_name(self, stok_ad):
        return self.repository.find_by_name(stok_ad)
