import pyodbc

class CikisFisiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_last_fis_numarasi(self):
        query = "SELECT TOP 1 FisNo FROM CikisFisi ORDER BY FisNo DESC"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None

    def save(self, cikis_fisi):
        query = """
        INSERT INTO CikisFisi (FisNo, FisTarihi, Stokkod, Stokad, birim, miktar, BirimFiyat, ToplamTutar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (cikis_fisi.fis_no, cikis_fisi.fis_tarihi, cikis_fisi.stokkod, cikis_fisi.stokad,
                                   cikis_fisi.birim, cikis_fisi.miktar, cikis_fisi.birim_fiyat, cikis_fisi.toplam_tutar))
            conn.commit()

    def get_all(self):
        query = "SELECT * FROM CikisFisi"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def check_stok_kodu(self, stokkod):
        query = "SELECT COUNT(*) FROM StokKarti WHERE Stokkod = ?"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (stokkod,))
            result = cursor.fetchone()
            return result[0] > 0

    def check_stok_adi(self, stokad):
        query = "SELECT COUNT(*) FROM StokKarti WHERE Stokad = ?"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (stokad,))
            result = cursor.fetchone()
            return result[0] > 0

    def check_stok_kodu_adi(self, stokkod, stokad):
        query = "SELECT COUNT(*) FROM StokKarti WHERE Stokkod = ? AND Stokad = ?"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (stokkod, stokad))
            result = cursor.fetchone()
            return result[0] > 0

    def get_fis_details(self, fis_no):
        query = """
        SELECT Stokkod, Stokad, miktar, birim, FisNo, FisTarihi
        FROM CikisFisi
        WHERE FisNo = ?
        """
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (fis_no,))
            return cursor.fetchall()

    def get_all_fis_details(self):
        query = """
        SELECT Stokkod, Stokad, miktar, birim, FisNo, FisTarihi
        FROM CikisFisi
        """
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def find_all(self):
        query = "SELECT * FROM CikisFisi"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cikis_fisleri = []
            for row in rows:
                cikis_fisleri.append({
                    'fis_no': row.FisNo,
                    'fis_tarihi': row.FisTarihi,
                    'stokkod': row.Stokkod,
                    'stokad': row.Stokad,
                    'birim': row.birim,
                    'miktar': row.miktar,
                    'birim_fiyat': row.BirimFiyat,
                    'toplam_tutar': row.ToplamTutar
                })
            return cikis_fisleri

    def get_all_fis_details(self):
        # Bu metodu veritabanından çıkış fişlerini almak için ekliyoruz.
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CikisFisi")
            rows = cursor.fetchall()
        return rows