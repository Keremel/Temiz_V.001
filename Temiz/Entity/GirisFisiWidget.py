from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
from Temiz.Service.GirisFisi_Service import GirisFisiService

class GirisFisiWidget(QWidget):
    def __init__(self, service: GirisFisiService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self.fis_no = QLineEdit(self)
        self.fis_no.setReadOnly(True)
        self.fis_no.setText(self.service.generate_new_fis_no())

        self.fis_tarihi = QDateEdit(self)
        self.fis_tarihi.setDate(QDate.currentDate())

        self.stok_kodu = QLineEdit(self)

        self.stok_adi = QLineEdit(self)

        self.birim = QLineEdit(self)

        self.miktar = QLineEdit(self)
        self.miktar.textChanged.connect(self.calculate_total)

        self.birim_fiyat = QLineEdit(self)
        self.birim_fiyat.textChanged.connect(self.calculate_total)

        self.toplam_tutar = QLineEdit(self)
        self.toplam_tutar.setReadOnly(True)

        self.aciklama = QLineEdit(self)

        self.cari_kod = QLineEdit(self)

        self.form_layout.addRow('Fiş No:', self.fis_no)
        self.form_layout.addRow('Fiş Tarihi:', self.fis_tarihi)
        self.form_layout.addRow('Stok Kodu:', self.stok_kodu)
        self.form_layout.addRow('Stok Adı:', self.stok_adi)
        self.form_layout.addRow('Birim:', self.birim)
        self.form_layout.addRow('Miktar:', self.miktar)
        self.form_layout.addRow('Birim Fiyat:', self.birim_fiyat)
        self.form_layout.addRow('Toplam Tutar:', self.toplam_tutar)
        self.form_layout.addRow('Açıklama:', self.aciklama)
        self.form_layout.addRow('Cari Kod:', self.cari_kod)

        self.save_button = QPushButton('Kaydet', self)
        self.save_button.clicked.connect(self.save_giris_fisi)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def calculate_total(self):
        try:
            miktar = float(self.miktar.text())
            birim_fiyat = float(self.birim_fiyat.text())
            toplam_tutar = miktar * birim_fiyat
            self.toplam_tutar.setText(str(toplam_tutar))
        except ValueError:
            self.toplam_tutar.setText('')

    def save_giris_fisi(self):
        fis_no = self.fis_no.text()
        fis_tarihi = self.fis_tarihi.date().toString('yyyy-MM-dd')
        stok_kodu = self.stok_kodu.text()
        stok_adi = self.stok_adi.text()
        birim = self.birim.text()
        miktar = self.miktar.text()
        birim_fiyat = self.birim_fiyat.text()
        toplam_tutar = self.toplam_tutar.text()
        aciklama = self.aciklama.text()
        cari_kod = self.cari_kod.text()

        if not stok_kodu or not stok_adi or not birim or not miktar or not birim_fiyat or not toplam_tutar or not cari_kod:
            QMessageBox.warning(self, 'Eksik Bilgi', 'Lütfen gerekli alanları doldurunuz.')
            return

        try:
            self.service.save_giris_fisi(fis_no, fis_tarihi, stok_kodu, stok_adi, birim, miktar, birim_fiyat, toplam_tutar, aciklama, cari_kod)
            QMessageBox.information(self, 'Başarılı', 'Giriş fişi başarıyla kaydedildi.')
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def clear_form(self):
        self.fis_no.setText(self.service.generate_new_fis_no())
        self.fis_tarihi.setDate(QDate.currentDate())
        self.stok_kodu.clear()
        self.stok_adi.clear()
        self.birim.clear()
        self.miktar.clear()
        self.birim_fiyat.clear()
        self.toplam_tutar.clear()
        self.aciklama.clear()
        self.cari_kod.clear()
