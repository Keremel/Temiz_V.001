from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class CikisFisiGorWidget(QWidget):
    def __init__(self, cikis_fisleri, cikis_fisi_service):
        super().__init__()
        self.cikis_fisleri = cikis_fisleri
        self.cikis_fisi_service = cikis_fisi_service
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['FisNo', 'FisTarihi', 'Stokkod', 'Stokad', 'Birim', 'Miktar', 'SatisFiyati', 'ToplamTutar'])
        self.load_data()

    def load_data(self):
        self.tableWidget.setRowCount(0)
        for row_data in self.cikis_fisleri:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(row_data.FisNo))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(row_data.FisTarihi.strftime('%Y-%m-%d')))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(row_data.Stokkod))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(row_data.Stokad))
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(row_data.Birim))
            self.tableWidget.setItem(row_position, 5, QTableWidgetItem(str(row_data.Miktar)))
            self.tableWidget.setItem(row_position, 6, QTableWidgetItem(str(row_data.SatisFiyati)))
            self.tableWidget.setItem(row_position, 7, QTableWidgetItem(str(row_data.ToplamTutar)))
