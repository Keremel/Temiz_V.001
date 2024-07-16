from Temiz.Entity.CikisFisi import CikisFisi


class CikisFisiService:
    def __init__(self, repository):
        self.repository = repository

    def save_cikis_fisi(self, fis_numarasi, tarih, stok_kodu, stok_adi, birim, miktar, birim_fiyati, toplam_tutar, barkod):
        if not self.repository.check_stok_kodu(stok_kodu):
            raise Exception('Sistemde kayıtlı olmayan stok kodu.')
        # Diğer kontrolleri ekleyin (eğer gerekliyse)

        cikis_fisi = CikisFisi(fis_numarasi, stok_kodu, stok_adi, miktar, birim, birim_fiyati, toplam_tutar, barkod, tarih)
        self.repository.save(cikis_fisi)

    def get_all_cikis_fisleri(self):
        return self.repository.find_all()

    def generate_new_fis_numarasi(self):
        last_fis = self.repository.get_last_fis_numarasi()
        if last_fis:
            new_fis_num = int(last_fis.replace("CF", "")) + 1
            return f"CF{new_fis_num:05d}"
        else:
            return "CF00001"
