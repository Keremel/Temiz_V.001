# Entity/CariGorWidget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QLabel, \
    QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from Temiz.Entity.CariGuncelleWidget import CariGuncelleWidget


class CariGorWidget(QWidget):
    def __init__(self, cariler, service, parent=None):
        super().__init__(parent)
        self.service = service  # Service referansı
        self.initUI(cariler)

    def initUI(self, cariler):
        layout = QVBoxLayout(self)

        # Yenile Butonu ve Resim
        self.refresh_button = QPushButton(self)
        self.refresh_button.setFixedSize(32, 32)
        icon_path = r'C:\Users\kerem\Desktop\Temiz\png\yenilebutton.png'  # Tam dosya yolunu kullanın
        icon = QIcon(icon_path)
        self.refresh_button.setIcon(icon)
        self.refresh_button.setIconSize(self.refresh_button.size())
        self.refresh_button.clicked.connect(self.refresh_table)

        refresh_layout = QHBoxLayout()
        refresh_layout.addWidget(self.refresh_button)
        refresh_layout.addStretch()

        # Tablo
        self.table = QTableWidget(self)
        self.table.setRowCount(len(cariler))
        self.table.setColumnCount(18)  # 18 kolon başlığı var
        self.table.setHorizontalHeaderLabels([
            'Cari Kod', 'Cari Ad', 'Vergi Dairesi', 'Vergi No', 'T.C. Kimlik No',
            'Adres', 'Telefon', 'Faks', 'Email', 'Web Sitesi',
            'Banka Hesap Bilgileri', 'İlgili Kişi', 'Ödeme Tahsilat Koşulları', 'Para Birimi',
            'Risk Limiti', 'Sektör', 'Notlar', 'Cari Türü'
        ])

        for row, cari in enumerate(cariler):
            self.table.setItem(row, 0, QTableWidgetItem(cari.cari_kod))
            self.table.setItem(row, 1, QTableWidgetItem(cari.cari_ad))
            self.table.setItem(row, 2, QTableWidgetItem(cari.vergi_dairesi))
            self.table.setItem(row, 3, QTableWidgetItem(cari.vergi_no))
            self.table.setItem(row, 4, QTableWidgetItem(cari.tc_kimlik_no))
            self.table.setItem(row, 5, QTableWidgetItem(cari.adres))
            self.table.setItem(row, 6, QTableWidgetItem(cari.telefon))
            self.table.setItem(row, 7, QTableWidgetItem(cari.faks))
            self.table.setItem(row, 8, QTableWidgetItem(cari.email))
            self.table.setItem(row, 9, QTableWidgetItem(cari.web_sitesi))
            self.table.setItem(row, 10, QTableWidgetItem(cari.banka_hesap_bilgileri))
            self.table.setItem(row, 11, QTableWidgetItem(cari.ilgili_kisi))
            self.table.setItem(row, 12, QTableWidgetItem(cari.odeme_tahsilat_kosullari))
            self.table.setItem(row, 13, QTableWidgetItem(cari.para_birimi))
            self.table.setItem(row, 14, QTableWidgetItem(cari.risk_limiti))
            self.table.setItem(row, 15, QTableWidgetItem(cari.sektor))
            self.table.setItem(row, 16, QTableWidgetItem(cari.notlar))
            self.table.setItem(row, 17, QTableWidgetItem(cari.cari_turu))

        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)

        layout.addLayout(refresh_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def set_service(self, service):
        self.service = service

    def on_item_double_clicked(self, item):
        row = item.row()
        cari_kod = self.table.item(row, 0).text()
        try:
            cari = self.service.get_cari_by_kod(cari_kod)
            if cari:
                self.cari_guncelle_widget = CariGuncelleWidget(self.service, cari)
                self.cari_guncelle_widget.show()
            else:
                QMessageBox.warning(self, 'Bulunamadı', 'Girilen cari kodu ile eşleşen kayıt bulunamadı.')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def refresh_table(self):
        try:
            cariler = self.service.get_all_cariler()
            self.table.setRowCount(len(cariler))
            for row, cari in enumerate(cariler):
                self.table.setItem(row, 0, QTableWidgetItem(cari.cari_kod))
                self.table.setItem(row, 1, QTableWidgetItem(cari.cari_ad))
                self.table.setItem(row, 2, QTableWidgetItem(cari.vergi_dairesi))
                self.table.setItem(row, 3, QTableWidgetItem(cari.vergi_no))
                self.table.setItem(row, 4, QTableWidgetItem(cari.tc_kimlik_no))
                self.table.setItem(row, 5, QTableWidgetItem(cari.adres))
                self.table.setItem(row, 6, QTableWidgetItem(cari.telefon))
                self.table.setItem(row, 7, QTableWidgetItem(cari.faks))
                self.table.setItem(row, 8, QTableWidgetItem(cari.email))
                self.table.setItem(row, 9, QTableWidgetItem(cari.web_sitesi))
                self.table.setItem(row, 10, QTableWidgetItem(cari.banka_hesap_bilgileri))
                self.table.setItem(row, 11, QTableWidgetItem(cari.ilgili_kisi))
                self.table.setItem(row, 12, QTableWidgetItem(cari.odeme_tahsilat_kosullari))
                self.table.setItem(row, 13, QTableWidgetItem(cari.para_birimi))
                self.table.setItem(row, 14, QTableWidgetItem(cari.risk_limiti))
                self.table.setItem(row, 15, QTableWidgetItem(cari.sektor))
                self.table.setItem(row, 16, QTableWidgetItem(cari.notlar))
                self.table.setItem(row, 17, QTableWidgetItem(cari.cari_turu))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
