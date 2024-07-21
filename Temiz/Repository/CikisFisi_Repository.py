import pyodbc

class CikisFisiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def get_last_fis_numarasi(self):
        query = "SELECT TOP 1 FisNo FROM CikisFisi ORDER BY FisNo DESC"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Error fetching last fis numarasi: {e}")
            return None

    def save(self, cikis_fisi):
        query = """
        INSERT INTO CikisFisi (FisNo, FisTarihi, Stokkod, Stokad, Birim, Miktar, SatisFiyati, ToplamTutar, KalanMiktar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (cikis_fisi.fis_no, cikis_fisi.fis_tarihi, cikis_fisi.stokkod, cikis_fisi.stokad,
                                       cikis_fisi.birim, cikis_fisi.miktar, cikis_fisi.satis_fiyati, cikis_fisi.toplam_tutar, cikis_fisi.kalan_miktar))
                conn.commit()
        except Exception as e:
            print(f"Error saving cikis fisi: {e}")

    def get_all(self):
        query = "SELECT * FROM CikisFisi"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all cikis fisleri: {e}")
            return []

    def check_stok_kodu(self, stokkod):
        query = "SELECT COUNT(*) FROM StokKarti WHERE Stokkod = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (stokkod,))
                result = cursor.fetchone()
                return result[0] > 0
        except Exception as e:
            print(f"Error checking stok kodu: {e}")
            return False

    def get_stock_info(self, stokkod):
        query = "SELECT StokAd, Birim, SatisFiyati, MevcutStokMiktari FROM StokKarti WHERE Stokkod = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (stokkod,))
                result = cursor.fetchone()
                if result:
                    return {
                        'StokAd': result[0],
                        'Birim': result[1],
                        'SatisFiyati': result[2],
                        'MevcutStokMiktari': result[3]
                    }
                return None
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return None

    def find_all(self):
        query = "SELECT * FROM CikisFisi"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all cikis fisleri: {e}")
            return []

    def get_all_fis_details(self):
        query = """
        SELECT FisNo, FisTarihi, Stokkod, Stokad, Birim, Miktar, SatisFiyati, ToplamTutar, KalanMiktar
        FROM CikisFisi
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all fis details: {e}")
            return []
