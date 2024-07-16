# Entity/StokGuncelleWidget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDialog
from Temiz.Service.StokKarti_Service import StokKartiService
from Temiz.Entity.StokKarti import StokKarti


class StokGuncelleWidget(QWidget):
    def __init__(self, stok_karti: StokKarti, service: StokKartiService, dialog: QDialog, parent=None):
        super().__init__(parent)
        self.stok_karti = stok_karti
        self.service = service
        self.dialog = dialog
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self.stok_kod = QLineEdit(self)
        self.stok_kod.setText(self.stok_karti.stok_kod)
        self.stok_kod.setReadOnly(True)

        self.stok_ad = QLineEdit(self)
        self.stok_ad.setText(self.stok_karti.stok_ad)

        self.birim = QLineEdit(self)
        self.birim.setText(self.stok_karti.birim)

        self.kategori = QLineEdit(self)
        self.kategori.setText(self.stok_karti.kategori)

        self.tedarikci_bilgileri = QLineEdit(self)
        self.tedarikci_bilgileri.setText(self.stok_karti.tedarikci_bilgileri)

        self.alis_fiyati = QLineEdit(self)
        self.alis_fiyati.setText(str(self.stok_karti.alis_fiyati))

        self.satis_fiyati = QLineEdit(self)
        self.satis_fiyati.setText(str(self.stok_karti.satis_fiyati))

        self.mevcut_stok_miktari = QLineEdit(self)
        self.mevcut_stok_miktari.setText(str(self.stok_karti.mevcut_stok_miktari))

        self.minimum_stok_seviyesi = QLineEdit(self)
        self.minimum_stok_seviyesi.setText(str(self.stok_karti.minimum_stok_seviyesi))

        self.maksimum_stok_seviyesi = QLineEdit(self)
        self.maksimum_stok_seviyesi.setText(str(self.stok_karti.maksimum_stok_seviyesi))

        self.depo_lokasyonu = QLineEdit(self)
        self.depo_lokasyonu.setText(self.stok_karti.depo_lokasyonu)

        self.barkod_numarasi = QLineEdit(self)
        self.barkod_numarasi.setText(self.stok_karti.barkod_numarasi)

        self.form_layout.addRow('Ürün Stok Kodu:', self.stok_kod)
        self.form_layout.addRow('Ürün İsmi:', self.stok_ad)
        self.form_layout.addRow('Birim:', self.birim)
        self.form_layout.addRow('Kategori:', self.kategori)
        self.form_layout.addRow('Tedarikçi Bilgileri:', self.tedarikci_bilgileri)
        self.form_layout.addRow('Alış Fiyatı:', self.alis_fiyati)
        self.form_layout.addRow('Satış Fiyatı:', self.satis_fiyati)
        self.form_layout.addRow('Mevcut Stok Miktarı:', self.mevcut_stok_miktari)
        self.form_layout.addRow('Minimum Stok:', self.minimum_stok_seviyesi)
        self.form_layout.addRow('Maksimum Stok:', self.maksimum_stok_seviyesi)
        self.form_layout.addRow('Depo Lokasyonu:', self.depo_lokasyonu)
        self.form_layout.addRow('Barkod Numarası:', self.barkod_numarasi)

        self.save_button = QPushButton('Güncelle', self)
        self.save_button.clicked.connect(self.update_stok_karti)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def update_stok_karti(self):
        try:
            stok_kod = self.stok_kod.text()
            stok_ad = self.stok_ad.text()
            birim = self.birim.text()
            kategori = self.kategori.text()
            tedarikci_bilgileri = self.tedarikci_bilgileri.text()
            alis_fiyati = float(self.alis_fiyati.text())
            satis_fiyati = float(self.satis_fiyati.text())
            mevcut_stok_miktari = int(self.mevcut_stok_miktari.text())
            minimum_stok_seviyesi = int(self.minimum_stok_seviyesi.text())
            maksimum_stok_seviyesi = int(self.maksimum_stok_seviyesi.text())
            depo_lokasyonu = self.depo_lokasyonu.text()
            barkod_numarasi = self.barkod_numarasi.text()

            if not stok_ad or not birim or alis_fiyati <= 0 or satis_fiyati <= 0:
                QMessageBox.warning(self, 'Eksik Bilgi', 'Lütfen gerekli alanları doldurunuz.')
                return

            existing_stok = self.service.find_by_name(stok_ad)
            if existing_stok and existing_stok.stok_kod != stok_kod:
                QMessageBox.warning(self, 'Kayıtlı Ürün İsmi', 'Aynı isimle farklı bir ürün zaten kayıtlı.')
                return

            updated_stok_karti = StokKarti(stok_kod, stok_ad, birim, kategori, tedarikci_bilgileri, alis_fiyati,
                                           satis_fiyati, mevcut_stok_miktari, minimum_stok_seviyesi,
                                           maksimum_stok_seviyesi, depo_lokasyonu, barkod_numarasi)

            self.service.update_stok_karti(updated_stok_karti)
            QMessageBox.information(self, 'Başarılı', 'Stok kartı başarıyla güncellendi.')
            self.dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
