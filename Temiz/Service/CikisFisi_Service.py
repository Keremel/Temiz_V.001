from Temiz.Entity.CikisFisi import CikisFisi


class CikisFisiService:
    def __init__(self, cikis_fisi_repository):
        self.cikis_fisi_repository = cikis_fisi_repository

    def save_cikis_fisi(self, fis_no, fis_tarihi, stokkod, stokad, birim, miktar, satis_fiyati, toplam_tutar, kalan_miktar):
        cikis_fisi = CikisFisi(fis_no, fis_tarihi, stokkod, stokad, birim, miktar, satis_fiyati, toplam_tutar, kalan_miktar)
        self.cikis_fisi_repository.save(cikis_fisi)
        self.update_stok_miktari(stokkod, miktar)

    def get_mevcut_stok(self, stokkod):
        query = "SELECT MevcutStokMiktari FROM StokKarti WHERE Stokkod = ?"
        try:
            with self.cikis_fisi_repository.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (stokkod,))
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            print(f"Error fetching current stock: {e}")
            return 0

    def update_stok_miktari(self, stokkod, miktar):
        query = "UPDATE StokKarti SET MevcutStokMiktari = MevcutStokMiktari - ? WHERE Stokkod = ?"
        try:
            with self.cikis_fisi_repository.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (miktar, stokkod))
                conn.commit()
        except Exception as e:
            print(f"Error updating stock quantity: {e}")

    def get_last_fis_numarasi(self):
        return self.cikis_fisi_repository.get_last_fis_numarasi()

    def check_stok_kodu(self, stokkod):
        return self.cikis_fisi_repository.check_stok_kodu(stokkod)

    def get_stock_info(self, stokkod):
        return self.cikis_fisi_repository.get_stock_info(stokkod)

    def get_all_cikis_fisleri(self):
        return self.cikis_fisi_repository.find_all()

    def get_all_fis_details(self):
        return self.cikis_fisi_repository.get_all_fis_details()
