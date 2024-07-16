# Entity/StokGorWidget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QHBoxLayout, \
    QDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from Temiz.Service.StokKarti_Service import StokKartiService
from Temiz.Entity.StokGuncelleWidget import StokGuncelleWidget
from Temiz.Entity.StokKarti import StokKarti  # StokKarti import edildi


class StokGorWidget(QWidget):
    def __init__(self, stoklar, service: StokKartiService, parent=None):
        super().__init__(parent)
        self.stoklar = stoklar
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.top_layout = QHBoxLayout()
        self.refresh_button = QPushButton('', self)
        self.refresh_button.setIcon(QIcon('C:/Users/kerem/Desktop/Temiz/png/yenilebutton.png'))
        self.refresh_button.setIconSize(QSize(32, 32))
        self.refresh_button.clicked.connect(self.refresh)
        self.top_layout.addWidget(self.refresh_button)
        self.top_layout.addStretch()

        self.table = QTableWidget(self)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(
            ['Ürün Stok Kodu', 'Ürün İsmi', 'Birim', 'Kategori', 'Tedarikçi Bilgileri', 'Alış Fiyatı', 'Satış Fiyatı',
             'Mevcut Stok Miktarı', 'Minimum Stok', 'Maksimum Stok', 'Depo Lokasyonu', 'Barkod Numarası'])
        self.table.setRowCount(len(self.stoklar))

        for row, stok in enumerate(self.stoklar):
            self.table.setItem(row, 0, QTableWidgetItem(stok.stok_kod))
            self.table.setItem(row, 1, QTableWidgetItem(stok.stok_ad))
            self.table.setItem(row, 2, QTableWidgetItem(stok.birim))
            self.table.setItem(row, 3, QTableWidgetItem(stok.kategori))
            self.table.setItem(row, 4, QTableWidgetItem(stok.tedarikci_bilgileri))
            self.table.setItem(row, 5, QTableWidgetItem(str(stok.alis_fiyati)))
            self.table.setItem(row, 6, QTableWidgetItem(str(stok.satis_fiyati)))
            self.table.setItem(row, 7, QTableWidgetItem(str(stok.mevcut_stok_miktari)))
            self.table.setItem(row, 8, QTableWidgetItem(str(stok.minimum_stok_seviyesi)))
            self.table.setItem(row, 9, QTableWidgetItem(str(stok.maksimum_stok_seviyesi)))
            self.table.setItem(row, 10, QTableWidgetItem(stok.depo_lokasyonu))
            self.table.setItem(row, 11, QTableWidgetItem(stok.barkod_numarasi))

        self.table.doubleClicked.connect(self.open_guncelle_widget)

        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def refresh(self):
        try:
            stoklar = self.service.get_all_stoklar()
            self.table.setRowCount(len(stoklar))

            for row, stok in enumerate(stoklar):
                self.table.setItem(row, 0, QTableWidgetItem(stok.stok_kod))
                self.table.setItem(row, 1, QTableWidgetItem(stok.stok_ad))
                self.table.setItem(row, 2, QTableWidgetItem(stok.birim))
                self.table.setItem(row, 3, QTableWidgetItem(stok.kategori))
                self.table.setItem(row, 4, QTableWidgetItem(stok.tedarikci_bilgileri))
                self.table.setItem(row, 5, QTableWidgetItem(str(stok.alis_fiyati)))
                self.table.setItem(row, 6, QTableWidgetItem(str(stok.satis_fiyati)))
                self.table.setItem(row, 7, QTableWidgetItem(str(stok.mevcut_stok_miktari)))
                self.table.setItem(row, 8, QTableWidgetItem(str(stok.minimum_stok_seviyesi)))
                self.table.setItem(row, 9, QTableWidgetItem(str(stok.maksimum_stok_seviyesi)))
                self.table.setItem(row, 10, QTableWidgetItem(stok.depo_lokasyonu))
                self.table.setItem(row, 11, QTableWidgetItem(stok.barkod_numarasi))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def open_guncelle_widget(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            stok_kod = self.table.item(selected_row, 0).text()
            stok_ad = self.table.item(selected_row, 1).text()
            birim = self.table.item(selected_row, 2).text()
            kategori = self.table.item(selected_row, 3).text()
            tedarikci_bilgileri = self.table.item(selected_row, 4).text()
            alis_fiyati = float(self.table.item(selected_row, 5).text())
            satis_fiyati = float(self.table.item(selected_row, 6).text())
            mevcut_stok_miktari = int(self.table.item(selected_row, 7).text())
            minimum_stok_seviyesi = int(self.table.item(selected_row, 8).text())
            maksimum_stok_seviyesi = int(self.table.item(selected_row, 9).text())
            depo_lokasyonu = self.table.item(selected_row, 10).text()
            barkod_numarasi = self.table.item(selected_row, 11).text()

            stok_karti = StokKarti(stok_kod, stok_ad, birim, kategori, tedarikci_bilgileri, alis_fiyati, satis_fiyati,
                                   mevcut_stok_miktari, minimum_stok_seviyesi, maksimum_stok_seviyesi, depo_lokasyonu,
                                   barkod_numarasi)

            guncelle_dialog = QDialog(self)
            guncelle_widget = StokGuncelleWidget(stok_karti, self.service, guncelle_dialog)
            layout = QVBoxLayout()
            layout.addWidget(guncelle_widget)
            guncelle_dialog.setLayout(layout)
            guncelle_dialog.setWindowTitle('Stok Güncelle')
            guncelle_dialog.exec_()
            self.refresh()  # Güncellemeden sonra tabloyu yenile
