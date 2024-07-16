import pyodbc
from Temiz.Entity.CikisFisi import CikisFisi

class CikisFisiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def connect(self):
        return pyodbc.connect(self.connection_string)

    def save(self, cikis_fisi):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO CikisFisi (FisNumarasi, StokKodu, StokAdi, Miktar, Birim, BirimFiyati, ToplamTutar, Barkod, Tarih)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cikis_fisi.fis_numarasi, cikis_fisi.stok_kodu, cikis_fisi.stok_adi, cikis_fisi.miktar, cikis_fisi.birim,
                cikis_fisi.birim_fiyati, cikis_fisi.toplam_tutar, cikis_fisi.barkod, cikis_fisi.tarih
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
            cursor.execute('SELECT * FROM CikisFisi')
            rows = cursor.fetchall()
            return [CikisFisi(*row) for row in rows]
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def get_last_fis_numarasi(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT TOP 1 FisNumarasi FROM CikisFisi ORDER BY FisNumarasi DESC')
            row = cursor.fetchone()
            return row[0] if row else None
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    def check_stok_kodu(self, stok_kodu):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM StokKarti WHERE StokKod = ?', (stok_kodu,))
            return cursor.fetchone()[0] > 0
        except pyodbc.Error as e:
            raise Exception(f'Bir hata oluştu: {e}')
        finally:
            conn.close()

    # Diğer check metotlarını buraya ekleyin (eğer gerekliyse)
