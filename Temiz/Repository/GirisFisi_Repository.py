import pyodbc

class GirisFisiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def get_last_fis_numarasi(self):
        query = "SELECT TOP 1 FisNo FROM GirisFisi ORDER BY FisNo DESC"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Error fetching last fis numarasi: {e}")
            return None

    def save(self, giris_fisi):
        query = """
        INSERT INTO GirisFisi (FisNo, FisTarihi, Stokkod, Stokad, Birim, Miktar, BirimFiyat, ToplamTutar, KalanMiktar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (giris_fisi.fis_no, giris_fisi.fis_tarihi, giris_fisi.stokkod, giris_fisi.stokad,
                                       giris_fisi.birim, giris_fisi.miktar, giris_fisi.birim_fiyat, giris_fisi.toplam_tutar, giris_fisi.kalan_miktar))
                conn.commit()
        except Exception as e:
            print(f"Error saving giris fisi: {e}")

    def get_all(self):
        query = "SELECT * FROM GirisFisi"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all giris fisleri: {e}")
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
        query = "SELECT StokAd, Birim, AlisFiyati AS BirimFiyat, MevcutStokMiktari FROM StokKarti WHERE Stokkod = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (stokkod,))
                result = cursor.fetchone()
                if result:
                    return {
                        'StokAd': result[0],
                        'Birim': result[1],
                        'BirimFiyat': result[2],
                        'MevcutStokMiktari': result[3]
                    }
                return None
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return None

    def find_all(self):
        query = "SELECT * FROM GirisFisi"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all giris fisleri: {e}")
            return []

    def find_by_fis_no(self, fis_no):
        query = "SELECT * FROM GirisFisi WHERE FisNo = ?"
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (fis_no,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching giris fis by fis no: {e}")
            return None

    def get_all_fis_details(self):
        query = """
        SELECT FisNo, FisTarihi, Stokkod, Stokad, Birim, Miktar, BirimFiyat, ToplamTutar, KalanMiktar
        FROM GirisFisi
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all fis details: {e}")
            return []
