from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from Temiz.Service.GirisFisi_Service import GirisFisiService
from Temiz.Entity.GirisFisi import GirisFisi

class GirisFisiGorWidget(QWidget):
    def __init__(self, giris_fisleri, service: GirisFisiService, parent=None):
        super().__init__(parent)
        self.giris_fisleri = giris_fisleri
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(8)  # Kolon sayısını uygun şekilde ayarlayın
        self.table.setHorizontalHeaderLabels(['Fiş No', 'Fiş Tarihi', 'Stok Kodu', 'Stok Adı', 'Birim', 'Miktar', 'Birim Fiyat', 'Toplam Tutar'])

        self.load_data()

        self.refresh_button = QPushButton(self)
        self.refresh_button.setIcon(QIcon('png/refresh.png'))
        self.refresh_button.setIconSize(QtCore.QSize(32, 32))
        self.refresh_button.clicked.connect(self.refresh_data)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.refresh_button)
        self.setLayout(self.layout)

    def load_data(self):
        self.table.setRowCount(len(self.giris_fisleri))
        for row, giris_fisi in enumerate(self.giris_fisleri):
            self.table.setItem(row, 0, QTableWidgetItem(giris_fisi.fis_no))
            self.table.setItem(row, 1, QTableWidgetItem(giris_fisi.fis_tarihi.strftime('%Y-%m-%d')))
            self.table.setItem(row, 2, QTableWidgetItem(giris_fisi.stok_kodu))
            self.table.setItem(row, 3, QTableWidgetItem(giris_fisi.stok_adi))
            self.table.setItem(row, 4, QTableWidgetItem(giris_fisi.birim))
            self.table.setItem(row, 5, QTableWidgetItem(str(giris_fisi.miktar)))
            self.table.setItem(row, 6, QTableWidgetItem(str(giris_fisi.birim_fiyat)))
            self.table.setItem(row, 7, QTableWidgetItem(str(giris_fisi.toplam_tutar)))

    def refresh_data(self):
        try:
            self.giris_fisleri = self.service.get_all_giris_fisleri()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Veriler yenilenirken bir hata oluştu: {e}')
