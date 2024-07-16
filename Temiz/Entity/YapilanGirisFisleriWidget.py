from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from Temiz.Service.GirisFisi_Service import GirisFisiService

class YapilanGirisFisleriWidget(QWidget):
    def __init__(self, service: GirisFisiService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['Fiş Numarası', 'Fiş Tarihi', 'Stok Kodu', 'Stok Adı', 'Birim', 'Miktar', 'Birim Fiyatı', 'Toplam Tutar', 'Barkod'])

        self.refresh_button = QPushButton('Yenile', self)
        self.refresh_button.clicked.connect(self.load_cikis_fisleri)

        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.load_cikis_fisleri()


    def load_giris_fisleri(self):
        try:
            giris_fisleri = self.service.get_all_giris_fisleri()
            self.table.setRowCount(len(giris_fisleri))
            for row, giris_fisi in enumerate(giris_fisleri):
                self.table.setItem(row, 0, QTableWidgetItem(str(giris_fisi.fis_numarasi)))
                self.table.setItem(row, 1, QTableWidgetItem(str(giris_fisi.fis_tarihi)))
                self.table.setItem(row, 2, QTableWidgetItem(str(giris_fisi.stok_kodu)))
                self.table.setItem(row, 3, QTableWidgetItem(str(giris_fisi.stok_adi)))
                self.table.setItem(row, 4, QTableWidgetItem(str(giris_fisi.birim)))
                self.table.setItem(row, 5, QTableWidgetItem(str(giris_fisi.miktar)))
                self.table.setItem(row, 6, QTableWidgetItem(str(giris_fisi.birim_fiyati)))
                self.table.setItem(row, 7, QTableWidgetItem(str(giris_fisi.toplam_tutar)))
                self.table.setItem(row, 8, QTableWidgetItem(str(giris_fisi.barkod)))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Giriş fişlerini yüklerken bir hata oluştu: {e}')
