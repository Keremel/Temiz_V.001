# Entity/StokEkleWidget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from Temiz.Service.StokKarti_Service import StokKartiService
from Temiz.Entity.StokKarti import StokKarti
from Temiz.Entity.StokGorWidget import StokGorWidget  # Doğru şekilde import edildi


class StokEkleWidget(QWidget):
    def __init__(self, service: StokKartiService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self.stok_kod = QLineEdit(self)
        self.stok_kod.setReadOnly(True)
        self.stok_kod.setText(self.service.generate_new_stok_kod())

        self.stok_ad = QLineEdit(self)

        self.birim = QLineEdit(self)

        self.kategori = QLineEdit(self)

        self.tedarikci_bilgileri = QLineEdit(self)

        self.alis_fiyati = QLineEdit(self)

        self.satis_fiyati = QLineEdit(self)

        self.mevcut_stok_miktari = QLineEdit(self)

        self.minimum_stok_seviyesi = QLineEdit(self)

        self.maksimum_stok_seviyesi = QLineEdit(self)

        self.depo_lokasyonu = QLineEdit(self)

        self.barkod_numarasi = QLineEdit(self)

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

        self.save_button = QPushButton('Ekle', self)
        self.save_button.clicked.connect(self.save_stok_karti)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_stok_karti(self):
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
            if existing_stok:
                QMessageBox.warning(self, 'Kayıtlı Ürün İsmi', 'Aynı isimle farklı bir ürün zaten kayıtlı.')
                return

            new_stok_karti = StokKarti(stok_kod, stok_ad, birim, kategori, tedarikci_bilgileri, alis_fiyati,
                                       satis_fiyati, mevcut_stok_miktari, minimum_stok_seviyesi, maksimum_stok_seviyesi,
                                       depo_lokasyonu, barkod_numarasi)

            self.service.save_stok_karti(new_stok_karti)
            QMessageBox.information(self, 'Başarılı', 'Stok kartı başarıyla eklendi.')
            parent = self.parent()
            while parent and not hasattr(parent, 'set_central_widget'):
                parent = parent.parent()
            if parent:
                parent.set_central_widget(
                    StokGorWidget(self.service.get_all_stoklar(), self.service))  # Stoklar sayfasına dön
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
