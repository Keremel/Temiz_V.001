# Repository/StokKarti_Repository.py
import pyodbc
from Temiz.Entity.StokKarti import StokKarti

class StokKartiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        return pyodbc.connect(self.connection_string)

    def save(self, stok_karti):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO StokKarti (StokKod, StokAd, Birim, Kategori, TedarikciBilgileri, AlisFiyati, SatisFiyati, MevcutStokMiktari, MinimumStokSeviyesi, MaksimumStokSeviyesi, DepoLokasyonu, BarkodNumarasi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                stok_karti.stok_kod, stok_karti.stok_ad, stok_karti.birim, stok_karti.kategori, stok_karti.tedarikci_bilgileri,
                stok_karti.alis_fiyati, stok_karti.satis_fiyati, stok_karti.mevcut_stok_miktari, stok_karti.minimum_stok_seviyesi,
                stok_karti.maksimum_stok_seviyesi, stok_karti.depo_lokasyonu, stok_karti.barkod_numarasi
            ))
            conn.commit()
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def update(self, stok_karti):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE StokKarti
                SET StokAd = ?, Birim = ?, Kategori = ?, TedarikciBilgileri = ?, AlisFiyati = ?, SatisFiyati = ?, MevcutStokMiktari = ?, MinimumStokSeviyesi = ?, MaksimumStokSeviyesi = ?, DepoLokasyonu = ?, BarkodNumarasi = ?
                WHERE StokKod = ?
            ''', (
                stok_karti.stok_ad, stok_karti.birim, stok_karti.kategori, stok_karti.tedarikci_bilgileri, stok_karti.alis_fiyati, stok_karti.satis_fiyati,
                stok_karti.mevcut_stok_miktari, stok_karti.minimum_stok_seviyesi, stok_karti.maksimum_stok_seviyesi, stok_karti.depo_lokasyonu, stok_karti.barkod_numarasi,
                stok_karti.stok_kod
            ))
            conn.commit()
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def find_all(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT StokKod, StokAd, Birim, Kategori, TedarikciBilgileri, AlisFiyati, SatisFiyati, MevcutStokMiktari, MinimumStokSeviyesi, MaksimumStokSeviyesi, DepoLokasyonu, BarkodNumarasi FROM StokKarti')
            rows = cursor.fetchall()
            return [StokKarti(*row) for row in rows]
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def generate_new_stok_kod(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT StokKod FROM StokKarti ORDER BY StokKod DESC')
            last_kod = cursor.fetchone()
            if last_kod:
                max_kod = last_kod[0]
                new_kod = f'S{int(max_kod[1:]) + 1:05d}'
            else:
                new_kod = 'S00001'
            return new_kod
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def find_by_name(self, stok_ad):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT StokKod, StokAd, Birim, Kategori, TedarikciBilgileri, AlisFiyati, SatisFiyati, MevcutStokMiktari, MinimumStokSeviyesi, MaksimumStokSeviyesi, DepoLokasyonu, BarkodNumarasi FROM StokKarti WHERE StokAd = ?', (stok_ad,))
            row = cursor.fetchone()
            if row:
                return StokKarti(*row)
            return None
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()
