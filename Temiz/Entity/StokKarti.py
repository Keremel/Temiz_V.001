# Entity/StokKarti.py
class StokKarti:
    def __init__(self, stok_kod, stok_ad, birim, kategori, tedarikci_bilgileri, alis_fiyati, satis_fiyati, mevcut_stok_miktari, minimum_stok_seviyesi, maksimum_stok_seviyesi, depo_lokasyonu, barkod_numarasi):
        self.stok_kod = stok_kod
        self.stok_ad = stok_ad
        self.birim = birim
        self.kategori = kategori
        self.tedarikci_bilgileri = tedarikci_bilgileri
        self.alis_fiyati = alis_fiyati
        self.satis_fiyati = satis_fiyati
        self.mevcut_stok_miktari = mevcut_stok_miktari
        self.minimum_stok_seviyesi = minimum_stok_seviyesi
        self.maksimum_stok_seviyesi = maksimum_stok_seviyesi
        self.depo_lokasyonu = depo_lokasyonu
        self.barkod_numarasi = barkod_numarasi
