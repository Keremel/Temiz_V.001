from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from Temiz.Service.StokHareketleri_Service import StokHareketleriService

class StokHareketleriWidget(QWidget):
    def __init__(self, service: StokHareketleriService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Stok Kodu', 'Stok Adı', 'Miktar', 'Birim', 'Fiş No', 'Tarih'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.load_fis_data()

    def load_fis_data(self):
        try:
            records = self.service.get_all_fis_details()  # Burada doğru metodu çağırıyoruz
            self.table.setRowCount(0)
            for record in records:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for column, item in enumerate(record):
                    self.table.setItem(row_position, column, QTableWidgetItem(str(item)))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def load_data(self):
        stok_hareketleri = self.stok_hareketleri_service.get_all_stok_hareketleri()
        self.table.setRowCount(len(stok_hareketleri))
        for row, hareket in enumerate(stok_hareketleri):
            self.table.setItem(row, 0, QTableWidgetItem(hareket.stok_kodu))
            self.table.setItem(row, 1, QTableWidgetItem(hareket.stok_adi))
            self.table.setItem(row, 2, QTableWidgetItem(str(hareket.miktar)))
            self.table.setItem(row, 3, QTableWidgetItem(hareket.birim))
            self.table.setItem(row, 4, QTableWidgetItem(hareket.fis_no))
            self.table.setItem(row, 5, QTableWidgetItem(hareket.fis_tarihi.strftime('%Y-%m-%d')))