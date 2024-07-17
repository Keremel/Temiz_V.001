import pyodbc

class GirisFisiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_last_fis_no(self):
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 1 FisNo FROM barcode_db.dbo.GirisFisi ORDER BY FisNo DESC")
            row = cursor.fetchone()
            if row:
                return row.FisNo
            return None

    def find_all(self):
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM barcode_db.dbo.GirisFisi")
            rows = cursor.fetchall()
            return rows

    def save(self, giris_fisi):
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO barcode_db.dbo.GirisFisi (FisNo, FisTarihi, Stokkod, Stokad, birim, miktar, BirimFiyat, ToplamTutar)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, giris_fisi.fis_no, giris_fisi.fis_tarihi, giris_fisi.stok_kodu, giris_fisi.stok_adi, giris_fisi.birim, giris_fisi.miktar, giris_fisi.birim_fiyat, giris_fisi.toplam_tutar)
            conn.commit()

    def check_stok_kodu(self, stok_kodu):
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM barcode_db.dbo.StokKarti WHERE Stokkod = ?", stok_kodu)
            count = cursor.fetchone()[0]
            return count > 0

    def check_stok_adi(self, stok_adi):
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM barcode_db.dbo.StokKarti WHERE Stokad = ?", stok_adi)
            count = cursor.fetchone()[0]
            return count > 0

    def check_stok_kodu_adi(self, stok_kodu, stok_adi):
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM barcode_db.dbo.StokKarti WHERE Stokkod = ? AND Stokad = ?", stok_kodu, stok_adi)
            count = cursor.fetchone()[0]
            return count > 0

    def get_all_fis_details(self):
        # Bu metodu veritabanından giriş fişlerini almak için ekliyoruz.
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM GirisFisi")
            rows = cursor.fetchall()
        return rows