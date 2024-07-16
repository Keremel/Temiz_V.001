from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
from Temiz.Service.CikisFisi_Service import CikisFisiService

class CikisFisiWidget(QWidget):
    def __init__(self, service: CikisFisiService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.fis_numarasi = QLineEdit(self)
        self.fis_numarasi.setReadOnly(True)
        self.fis_numarasi.setText(self.service.generate_new_fis_numarasi())

        self.tarih = QDateEdit(self)
        self.tarih.setDate(QDate.currentDate())

        self.stok_kodu = QLineEdit(self)
        self.stok_adi = QLineEdit(self)
        self.birim = QLineEdit(self)
        self.miktar = QLineEdit(self)
        self.miktar.textChanged.connect(self.calculate_total)

        self.birim_fiyati = QLineEdit(self)
        self.birim_fiyati.textChanged.connect(self.calculate_total)

        self.toplam_tutar = QLineEdit(self)
        self.toplam_tutar.setReadOnly(True)

        self.barkod = QLineEdit(self)

        self.form_layout.addRow('Fiş Numarası:', self.fis_numarasi)
        self.form_layout.addRow('Tarih:', self.tarih)
        self.form_layout.addRow('Stok Kodu:', self.stok_kodu)
        self.form_layout.addRow('Stok Adı:', self.stok_adi)
        self.form_layout.addRow('Birim:', self.birim)
        self.form_layout.addRow('Miktar:', self.miktar)
        self.form_layout.addRow('Birim Fiyatı:', self.birim_fiyati)
        self.form_layout.addRow('Toplam Tutar:', self.toplam_tutar)
        self.form_layout.addRow('Barkod:', self.barkod)

        self.save_button = QPushButton('Kaydet', self)
        self.save_button.clicked.connect(self.save_cikis_fisi)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def calculate_total(self):
        try:
            miktar = float(self.miktar.text())
            birim_fiyati = float(self.birim_fiyati.text())
            toplam_tutar = miktar * birim_fiyati
            self.toplam_tutar.setText(str(toplam_tutar))
        except ValueError:
            self.toplam_tutar.setText('')

    def save_cikis_fisi(self):
        fis_numarasi = self.fis_numarasi.text()
        tarih = self.tarih.date().toString('yyyy-MM-dd')
        stok_kodu = self.stok_kodu.text()
        stok_adi = self.stok_adi.text()
        birim = self.birim.text()
        miktar = self.miktar.text()
        birim_fiyati = self.birim_fiyati.text()
        toplam_tutar = self.toplam_tutar.text()
        barkod = self.barkod.text()

        if not stok_kodu or not stok_adi or not birim or not miktar or not birim_fiyati or not toplam_tutar or not barkod:
            QMessageBox.warning(self, 'Eksik Bilgi', 'Lütfen gerekli alanları doldurunuz.')
            return

        try:
            self.service.save_cikis_fisi(fis_numarasi, tarih, stok_kodu, stok_adi, birim, miktar, birim_fiyati, toplam_tutar, barkod)
            QMessageBox.information(self, 'Başarılı', 'Çıkış fişi başarıyla kaydedildi.')
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def clear_form(self):
        self.fis_numarasi.setText(self.service.generate_new_fis_numarasi())
        self.tarih.setDate(QDate.currentDate())
        self.stok_kodu.clear()
        self.stok_adi.clear()
        self.birim.clear()
        self.miktar.clear()
        self.birim_fiyati.clear()
        self.toplam_tutar.clear()
        self.barkod.clear()
