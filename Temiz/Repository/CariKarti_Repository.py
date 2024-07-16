# Repository/CariKarti_Repository.py
import pyodbc
from Temiz.Entity.CariKarti import CariKarti

class CariKartiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        return pyodbc.connect(self.connection_string)

    def save(self, cari_karti):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO CariKarti (CariKod, CariAd, VergiDairesi, VergiNo, TCKimlikNo, Adres, Telefon, Faks, Email, WebSitesi, BankaHesapBilgileri, IlgiliKisi, OdemeTahsilatKosullari, ParaBirimi, RiskLimiti, Sektor, Notlar, CariTuru)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cari_karti.cari_kod, cari_karti.cari_ad, cari_karti.vergi_dairesi, cari_karti.vergi_no,
                cari_karti.tc_kimlik_no, cari_karti.adres, cari_karti.telefon, cari_karti.faks, cari_karti.email,
                cari_karti.web_sitesi, cari_karti.banka_hesap_bilgileri, cari_karti.ilgili_kisi,
                cari_karti.odeme_tahsilat_kosullari, cari_karti.para_birimi, cari_karti.risk_limiti,
                cari_karti.sektor, cari_karti.notlar, cari_karti.cari_turu
            ))
            conn.commit()
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def update(self, cari_karti):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE CariKarti SET 
                    CariAd = ?, 
                    VergiDairesi = ?, 
                    VergiNo = ?, 
                    TCKimlikNo = ?, 
                    Adres = ?, 
                    Telefon = ?, 
                    Faks = ?, 
                    Email = ?, 
                    WebSitesi = ?, 
                    BankaHesapBilgileri = ?, 
                    IlgiliKisi = ?, 
                    OdemeTahsilatKosullari = ?, 
                    ParaBirimi = ?, 
                    RiskLimiti = ?, 
                    Sektor = ?, 
                    Notlar = ?, 
                    CariTuru = ?
                WHERE CariKod = ?
            ''', (
                cari_karti.cari_ad, cari_karti.vergi_dairesi, cari_karti.vergi_no, cari_karti.tc_kimlik_no,
                cari_karti.adres, cari_karti.telefon, cari_karti.faks, cari_karti.email, cari_karti.web_sitesi,
                cari_karti.banka_hesap_bilgileri, cari_karti.ilgili_kisi, cari_karti.odeme_tahsilat_kosullari,
                cari_karti.para_birimi, cari_karti.risk_limiti, cari_karti.sektor, cari_karti.notlar,
                cari_karti.cari_turu, cari_karti.cari_kod
            ))
            conn.commit()
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def generate_new_cari_kod(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT MAX(CariKod) FROM CariKarti')
            max_cari_kod = cursor.fetchone()[0]
            if max_cari_kod:
                new_cari_kod = 'C' + str(int(max_cari_kod[1:]) + 1).zfill(3)
            else:
                new_cari_kod = 'C001'
            return new_cari_kod
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def find_all(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CariKarti')
            rows = cursor.fetchall()
            return [CariKarti(*row) for row in rows]
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def find_by_ad(self, cari_ad):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CariKarti WHERE CariAd = ?', (cari_ad,))
            rows = cursor.fetchall()
            if rows:
                return [CariKarti(*row) for row in rows]
            return None
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def find_by_kod(self, cari_kod):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CariKarti WHERE CariKod = ?', (cari_kod,))
            row = cursor.fetchone()
            if row:
                return CariKarti(*row)
            return None
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()
