import pyodbc


class GirisFisiRepository:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_last_fis_no(self):
        query = "SELECT TOP 1 fis_no FROM GirisFisi ORDER BY fis_no DESC"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] if result else None

    def save(self, fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar, aciklama, cari_kod):
        query = """
        INSERT INTO GirisFisi (fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar, aciklama, cari_kod)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar, aciklama, cari_kod))
            conn.commit()

    def get_all(self):
        query = "SELECT * FROM GirisFisi"
        with pyodbc.connect(self.connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
