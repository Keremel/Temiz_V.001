from Temiz.Entity.CikisFisi import CikisFisi

class CikisFisiService:
    def __init__(self, repository):
        self.repository = repository

    def save_cikis_fisi(self, fis_numarasi, tarih, stok_kodu, stok_adi, birim, miktar, birim_fiyati, toplam_tutar):
        if not self.check_stok_kodu(stok_kodu):
            raise ValueError(f"Stok kodu '{stok_kodu}' bulunamadı.")
        if not self.check_stok_adi(stok_adi):
            raise ValueError(f"Stok adı '{stok_adi}' bulunamadı.")
        if not self.check_stok_kodu_adi(stok_kodu, stok_adi):
            raise ValueError(f"Stok kodu '{stok_kodu}' ve stok adı '{stok_adi}' aynı satırda değil.")
        # Diğer kontrolleri ekleyin (eğer gerekliyse)

        cikis_fisi = CikisFisi(fis_numarasi, stok_kodu, stok_adi, miktar, birim, birim_fiyati, toplam_tutar, tarih)
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

    def get_last_fis_numarasi(self):
        return self.repository.get_last_fis_numarasi()

    def check_stok_kodu(self, stok_kodu):
        return self.repository.check_stok_kodu(stok_kodu)

    def check_stok_adi(self, stok_adi):
        return self.repository.check_stok_adi(stok_adi)

    def check_stok_kodu_adi(self, stok_kodu, stok_adi):
        return self.repository.check_stok_kodu_adi(stok_kodu, stok_adi)
