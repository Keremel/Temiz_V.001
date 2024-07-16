from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from Temiz.Service.CikisFisi_Service import CikisFisiService

class YapilanCikisFisleriWidget(QWidget):
    def __init__(self, service: CikisFisiService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['Fiş Numarası', 'Stok Kodu', 'Stok Adı', 'Miktar', 'Birim', 'Birim Fiyatı', 'Toplam Tutar', 'Barkod', 'Tarih'])

        self.refresh_button = QPushButton('Yenile', self)
        self.refresh_button.clicked.connect(self.load_cikis_fisleri)

        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.load_cikis_fisleri()

    def load_cikis_fisleri(self):
        try:
            cikis_fisleri = self.service.get_all_cikis_fisleri()
            self.table.setRowCount(len(cikis_fisleri))
            for row, cikis_fisi in enumerate(cikis_fisleri):
                self.table.setItem(row, 0, QTableWidgetItem(str(cikis_fisi.fis_numarasi)))
                self.table.setItem(row, 1, QTableWidgetItem(str(cikis_fisi.stok_kodu)))
                self.table.setItem(row, 2, QTableWidgetItem(str(cikis_fisi.stok_adi)))
                self.table.setItem(row, 3, QTableWidgetItem(str(cikis_fisi.miktar)))
                self.table.setItem(row, 4, QTableWidgetItem(str(cikis_fisi.birim)))
                self.table.setItem(row, 5, QTableWidgetItem(str(cikis_fisi.birim_fiyati)))
                self.table.setItem(row, 6, QTableWidgetItem(str(cikis_fisi.toplam_tutar)))
                self.table.setItem(row, 7, QTableWidgetItem(str(cikis_fisi.barkod)))
                self.table.setItem(row, 8, QTableWidgetItem(str(cikis_fisi.tarih)))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Çıkış fişlerini yüklerken bir hata oluştu: {e}')
