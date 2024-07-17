from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal
from Temiz.Service.CikisFisi_Service import CikisFisiService

class CikisFisiGorWidget(QWidget):
    cikis_fisi_guncelle = pyqtSignal()

    def __init__(self, cikis_fisleri, cikis_fisi_service):
        super().__init__()
        self.cikis_fisleri = cikis_fisleri
        self.cikis_fisi_service = cikis_fisi_service
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Yapılan Çıkış Fişleri')

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(
            ['Fiş No', 'Fiş Tarihi', 'Stok Kodu', 'Stok Adı', 'Birim', 'Miktar', 'Birim Fiyat', 'Toplam Tutar'])
        self.table_widget.setRowCount(len(self.cikis_fisleri))

        for row, cikis_fisi in enumerate(self.cikis_fisleri):
            self.table_widget.setItem(row, 0, QTableWidgetItem(cikis_fisi['fis_no']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(cikis_fisi['fis_tarihi'].strftime("%Y-%m-%d")))
            self.table_widget.setItem(row, 2, QTableWidgetItem(cikis_fisi['stokkod']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(cikis_fisi['stokad']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(cikis_fisi['birim']))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(cikis_fisi['miktar'])))
            self.table_widget.setItem(row, 6, QTableWidgetItem(str(cikis_fisi['birim_fiyat'])))
            self.table_widget.setItem(row, 7, QTableWidgetItem(str(cikis_fisi['toplam_tutar'])))

        self.refresh_button = QPushButton('Yenile')
        self.refresh_button.clicked.connect(self.refresh_cikis_fisleri)

        layout.addWidget(self.table_widget)
        layout.addWidget(self.refresh_button)

        self.setLayout(layout)

    def refresh_cikis_fisleri(self):
        self.cikis_fisleri = self.cikis_fisi_service.get_all_cikis_fisleri()
        self.table_widget.setRowCount(len(self.cikis_fisleri))

        for row, cikis_fisi in enumerate(self.cikis_fisleri):
            self.table_widget.setItem(row, 0, QTableWidgetItem(cikis_fisi['fis_no']))
            self.table_widget.setItem(row, 1, QTableWidgetItem(cikis_fisi['fis_tarihi'].strftime("%Y-%m-%d")))
            self.table_widget.setItem(row, 2, QTableWidgetItem(cikis_fisi['stokkod']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(cikis_fisi['stokad']))
            self.table_widget.setItem(row, 4, QTableWidgetItem(cikis_fisi['birim']))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(cikis_fisi['miktar'])))
            self.table_widget.setItem(row, 6, QTableWidgetItem(str(cikis_fisi['birim_fiyat'])))
            self.table_widget.setItem(row, 7, QTableWidgetItem(str(cikis_fisi['toplam_tutar'])))

        self.cikis_fisi_guncelle.emit()
