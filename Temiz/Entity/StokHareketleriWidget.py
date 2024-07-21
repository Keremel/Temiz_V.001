from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from .StokHaraketleri_ui import Ui_Form  # UI sınıfını import ediyoruz
from Temiz.Service.StokHareketleri_Service import StokHareketleriService
from datetime import datetime, date


class StokHareketleriWidget(QWidget, Ui_Form):
    def __init__(self, service: StokHareketleriService, parent=None):
        super().__init__(parent)
        self.service = service
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # Tabloya "Fiş Numarası" sütununu ekleme
        self.tableWidget.setColumnCount(9)  # Toplam sütun sayısını 9'a çıkarıyoruz
        self.tableWidget.setHorizontalHeaderLabels(
            ['Fiş Numarası', 'Tarih', 'Stok Kodu', 'Stok Adı', 'Depo Adı', 'Giren/Çıkan', 'Miktar', 'Toplam Tutar', 'Kalan Miktar'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Arama butonlarını arama metodlarına bağlama
        self.pushButton.clicked.connect(self.search_by_product)
        self.pushButton_2.clicked.connect(self.search_by_date)
        self.pushButton_3.clicked.connect(self.search_by_warehouse)
        self.radioButton.toggled.connect(self.search_by_transaction_type)
        self.radioButton_2.toggled.connect(self.search_by_transaction_type)

        # Verileri yükleme
        self.load_fis_data()

    def format_date(self, date_value):
        if isinstance(date_value, str):
            try:
                date_value = datetime.strptime(date_value, '%Y-%m-%d')
            except ValueError:
                return date_value
        elif isinstance(date_value, (datetime, date)):
            return date_value.strftime('%d/%m/%Y')
        return date_value

    def load_fis_data(self, records=None):
        try:
            if records is None:
                records = self.service.get_all_fis_details()  # Tüm kayıtları alıyoruz
            self.tableWidget.setRowCount(0)
            for record in records:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                for column, item in enumerate(record):
                    if column == 1:  # Tarih sütunu
                        item = self.format_date(item)
                    self.tableWidget.setItem(row_position, column, QTableWidgetItem(str(item)))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def search_by_product(self):
        # Ürün arama işlemi
        stok_kodu = self.lineEdit.text().strip()
        stok_adi = self.lineEdit_2.text().strip()
        try:
            records = self.service.get_all_fis_details()  # Tüm kayıtları alıyoruz
            filtered_records = [
                record for record in records
                if (not stok_kodu or record[2] == stok_kodu) and (not stok_adi or record[3] == stok_adi)
            ]
            self.load_fis_data(filtered_records)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def search_by_date(self):
        # Tarihe göre arama işlemi
        baslangic_tarihi = self.dateTimeEdit.dateTime().toString(Qt.ISODate)
        bitis_tarihi = self.dateTimeEdit_2.dateTime().toString(Qt.ISODate)
        try:
            records = self.service.get_all_fis_details()  # Tüm kayıtları alıyoruz
            baslangic_dt = datetime.fromisoformat(baslangic_tarihi)
            bitis_dt = datetime.fromisoformat(bitis_tarihi)
            filtered_records = [
                record for record in records
                if baslangic_dt.date() <= (record[1] if isinstance(record[1], date) else datetime.strptime(record[1], '%Y-%m-%d').date()) <= bitis_dt.date()
            ]
            for record in filtered_records:
                record[1] = self.format_date(record[1])
            self.load_fis_data(filtered_records)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def search_by_transaction_type(self):
        # İşleme göre arama işlemi
        if self.radioButton.isChecked():  # Giriş İşlemleri
            prefix = 'GF'
        elif self.radioButton_2.isChecked():  # Çıkış İşlemleri
            prefix = 'CF'
        else:
            return
        try:
            records = self.service.get_all_fis_details()  # Tüm kayıtları alıyoruz
            filtered_records = [
                record for record in records
                if record[0].startswith(prefix)
            ]
            self.load_fis_data(filtered_records)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def search_by_warehouse(self):
        # Depoya göre arama işlemi
        depo_adi = self.lineEdit_3.text().strip()
        try:
            records = self.service.get_all_fis_details()  # Tüm kayıtları alıyoruz
            filtered_records = [
                record for record in records
                if depo_adi in record
            ]
            self.load_fis_data(filtered_records)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
