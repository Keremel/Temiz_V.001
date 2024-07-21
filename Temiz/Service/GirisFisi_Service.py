from Temiz.Entity.GirisFisi import GirisFisi


class GirisFisiService:
    def __init__(self, giris_fisi_repository):
        self.giris_fisi_repository = giris_fisi_repository

    def save_giris_fisi(self, fis_no, fis_tarihi, stokkod, stokad, birim, miktar, birim_fiyat, toplam_tutar, kalan_miktar):
        giris_fisi = GirisFisi(fis_no, fis_tarihi, stokkod, stokad, birim, miktar, birim_fiyat, toplam_tutar, kalan_miktar)
        self.giris_fisi_repository.save(giris_fisi)
        self.update_stok_miktari(stokkod, miktar)

    def get_mevcut_stok(self, stokkod):
        query = "SELECT MevcutStokMiktari FROM StokKarti WHERE Stokkod = ?"
        try:
            with self.giris_fisi_repository.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (stokkod,))
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"Error fetching current stock: {e}")
            return 0

    def update_stok_miktari(self, stokkod, miktar):
        query = "UPDATE StokKarti SET MevcutStokMiktari = MevcutStokMiktari + ? WHERE Stokkod = ?"
        try:
            with self.giris_fisi_repository.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (miktar, stokkod))
                conn.commit()
        except Exception as e:
            print(f"Error updating stock quantity: {e}")

    def get_last_fis_numarasi(self):
        return self.giris_fisi_repository.get_last_fis_numarasi()

    def check_stok_kodu(self, stokkod):
        return self.giris_fisi_repository.check_stok_kodu(stokkod)

    def get_stock_info(self, stokkod):
        return self.giris_fisi_repository.get_stock_info(stokkod)

    def get_all_giris_fisleri(self):
        return self.giris_fisi_repository.find_all()

    def get_all_fis_details(self):
        return self.giris_fisi_repository.get_all_fis_details()

    def generate_new_fis_no(self):
        last_fis_no = self.get_last_fis_numarasi()
        if not last_fis_no:
            return "GF00001"

        new_fis_no = int(last_fis_no[2:]) + 1
        while self.giris_fisi_repository.find_by_fis_no(f"GF{new_fis_no:05d}") is not None:
            new_fis_no += 1
        return f"GF{new_fis_no:05d}"
