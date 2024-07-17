from Temiz.Entity.GirisFisi import GirisFisi

class GirisFisiService:
    def __init__(self, repository):
        self.repository = repository

    def save_giris_fisi(self, fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar):
        if not self.repository.check_stok_kodu(stok_kodu):
            raise ValueError(f"Stok kodu '{stok_kodu}' bulunamadı.")
        if not self.repository.check_stok_adi(stok_adi):
            raise ValueError(f"Stok adı '{stok_adi}' bulunamadı.")
        if not self.repository.check_stok_kodu_adi(stok_kodu, stok_adi):
            raise ValueError(f"Stok kodu '{stok_kodu}' ve stok adı '{stok_adi}' aynı satırda değil.")
        # Diğer kontrolleri ekleyin (eğer gerekliyse)

        giris_fisi = GirisFisi(fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar)
        self.repository.save(giris_fisi)

    def get_all_giris_fisleri(self):
        return self.repository.find_all()

    def generate_new_fis_no(self):
        last_fis = self.repository.get_last_fis_no()
        if last_fis:
            new_fis_num = int(last_fis.replace("GF", "")) + 1
            return f"GF{new_fis_num:05d}"
        else:
            return "GF00001"
