class GirisFisiService:
    def __init__(self, repository):
        self.repository = repository

    def generate_new_fis_no(self):
        # En son fiş numarasını al
        last_fis_no = self.repository.get_last_fis_no()
        if last_fis_no is None:
            return 'GF00001'

        # GF00001 formatındaki fiş numarasını artır
        last_number = int(last_fis_no[2:])
        new_fis_no_int = last_number + 1
        new_fis_no = f'GF{new_fis_no_int:05d}'
        return new_fis_no

    def save_giris_fisi(self, fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar, aciklama, cari_kod):
        self.repository.save(fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar, aciklama, cari_kod)

    def get_all_giris_fisleri(self):
        return self.repository.get_all()
