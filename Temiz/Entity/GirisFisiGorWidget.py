from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from Temiz.Service.GirisFisi_Service import GirisFisiService


class GirisFisiGorWidget(QWidget):
    def __init__(self, parent=None, service: GirisFisiService = None):
        super().__init__(parent)
        self.service = service
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.setLayout(self.layout)
        self.load_data()

    def load_data(self):
        giris_fisleri = self.service.get_all_giris_fisleri()
        self.table_widget.setRowCount(len(giris_fisleri))
        self.table_widget.setColumnCount(8)  # Sütun sayısı
        self.table_widget.setHorizontalHeaderLabels(
            ['FisNo', 'FisTarihi', 'Stokkod', 'Stokad', 'birim', 'miktar', 'BirimFiyat', 'ToplamTutar'])

        for row_idx, giris_fisi in enumerate(giris_fisleri):
            self.table_widget.setItem(row_idx, 0, QTableWidgetItem(str(giris_fisi.FisNo)))
            self.table_widget.setItem(row_idx, 1, QTableWidgetItem(str(giris_fisi.FisTarihi)))
            self.table_widget.setItem(row_idx, 2, QTableWidgetItem(str(giris_fisi.Stokkod)))
            self.table_widget.setItem(row_idx, 3, QTableWidgetItem(str(giris_fisi.Stokad)))
            self.table_widget.setItem(row_idx, 4, QTableWidgetItem(str(giris_fisi.birim)))
            self.table_widget.setItem(row_idx, 5, QTableWidgetItem(str(giris_fisi.miktar)))
            self.table_widget.setItem(row_idx, 6, QTableWidgetItem(str(giris_fisi.BirimFiyat)))
            self.table_widget.setItem(row_idx, 7, QTableWidgetItem(str(giris_fisi.ToplamTutar)))
