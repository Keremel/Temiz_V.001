import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLineEdit, QFormLayout, QPushButton
from PyQt5.QtCore import QDate, pyqtSignal
from Temiz.Entity.CikisFisi import CikisFisi
from Temiz.Service.CikisFisi_Service import CikisFisiService

class CikisFisiWidget(QWidget):
    cikis_fisi_olusturuldu = pyqtSignal()

    def __init__(self, cikis_fisi_service):
        super().__init__()
        self.cikis_fisi_service = cikis_fisi_service
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Çıkış Fişi Oluştur')

        layout = QVBoxLayout()

        self.fis_no_input = QLineEdit()
        self.fis_no_input.setReadOnly(True)
        self.fis_tarihi_input = QLineEdit()
        self.fis_tarihi_input.setReadOnly(True)
        self.fis_tarihi_input.setText(QDate.currentDate().toString('yyyy-MM-dd'))  # Güncel tarihi otomatik ayarla ve değiştirilmesini engelle
        self.stokkod_input = QLineEdit()
        self.stokad_input = QLineEdit()
        self.birim_input = QLineEdit()
        self.miktar_input = QLineEdit()
        self.miktar_input.textChanged.connect(self.calculate_total)  # Miktar değiştiğinde toplamı hesapla
        self.birim_fiyat_input = QLineEdit()
        self.birim_fiyat_input.textChanged.connect(self.calculate_total)  # Birim fiyatı değiştiğinde toplamı hesapla
        self.toplam_tutar_input = QLineEdit()
        self.toplam_tutar_input.setReadOnly(True)

        form_layout = QFormLayout()
        form_layout.addRow('Fiş No:', self.fis_no_input)
        form_layout.addRow('Fiş Tarihi:', self.fis_tarihi_input)
        form_layout.addRow('Stok Kodu:', self.stokkod_input)
        form_layout.addRow('Stok Adı:', self.stokad_input)
        form_layout.addRow('Birim:', self.birim_input)
        form_layout.addRow('Miktar:', self.miktar_input)
        form_layout.addRow('Birim Fiyat:', self.birim_fiyat_input)
        form_layout.addRow('Toplam Tutar:', self.toplam_tutar_input)

        self.save_button = QPushButton('Kaydet')
        self.save_button.clicked.connect(self.save_cikis_fisi)

        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.set_auto_fis_no()

    def set_auto_fis_no(self):
        last_fis_no = self.cikis_fisi_service.get_last_fis_numarasi()
        if last_fis_no:
            new_fis_no = f'CF{int(last_fis_no[2:]) + 1:05d}'
        else:
            new_fis_no = 'CF00001'
        self.fis_no_input.setText(new_fis_no)

    def calculate_total(self):
        try:
            miktar = float(self.miktar_input.text())
            birim_fiyat = float(self.birim_fiyat_input.text())
            toplam_tutar = miktar * birim_fiyat
            self.toplam_tutar_input.setText(str(toplam_tutar))
        except ValueError:
            self.toplam_tutar_input.setText('')

    def save_cikis_fisi(self):
        try:
            fis_no = self.fis_no_input.text()
            fis_tarihi = self.fis_tarihi_input.text()
            stokkod = self.stokkod_input.text()
            stokad = self.stokad_input.text()
            birim = self.birim_input.text()
            miktar = float(self.miktar_input.text())
            birim_fiyat = float(self.birim_fiyat_input.text())
            toplam_tutar = float(self.toplam_tutar_input.text())

            if not self.cikis_fisi_service.check_stok_kodu(stokkod):
                QMessageBox.critical(self, 'Hata', 'Stok kodu sistemde kayıtlı değil.')
                return

            if not self.cikis_fisi_service.check_stok_adi(stokad):
                QMessageBox.critical(self, 'Hata', 'Stok adı sistemde kayıtlı değil.')
                return

            if not self.cikis_fisi_service.check_stok_kodu_adi(stokkod, stokad):
                QMessageBox.critical(self, 'Hata', 'Stok kodu ve stok adı eşleşmiyor.')
                return

            cikis_fisi = CikisFisi(fis_no, stokkod, stokad, miktar, birim, birim_fiyat, toplam_tutar, fis_tarihi)
            self.cikis_fisi_service.save_cikis_fisi(fis_no, fis_tarihi, stokkod, stokad, birim, miktar, birim_fiyat, toplam_tutar)  # Doğru metodu çağır
            QMessageBox.information(self, 'Başarılı', 'Çıkış fişi başarıyla kaydedildi.')
            self.cikis_fisi_olusturuldu.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
