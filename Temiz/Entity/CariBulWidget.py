# Entity/CariBulWidget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QFormLayout, QLabel
from Temiz.Service.CariKarti_Service import CariKartiService


class CariBulWidget(QWidget):
    def __init__(self, service: CariKartiService, parent=None):
        super().__init__(parent)
        self.service = service
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self.search_input = QLineEdit(self)
        self.search_button = QPushButton('Ara', self)
        self.search_button.clicked.connect(self.search_cari)

        self.result_layout = QVBoxLayout()

        self.form_layout.addRow('Cari Ad:', self.search_input)
        self.form_layout.addRow(self.search_button)

        self.layout.addLayout(self.form_layout)
        self.layout.addLayout(self.result_layout)
        self.setLayout(self.layout)

    def search_cari(self):
        cari_ad = self.search_input.text().strip()
        if not cari_ad:
            QMessageBox.warning(self, 'Eksik Bilgi', 'Lütfen cari adını giriniz.')
            return

        try:
            cariler = self.service.get_cari_by_ad(cari_ad)
            if cariler:
                self.clear_results()
                for cari in cariler:
                    self.result_layout.addWidget(QLabel(f"Cari Kod: {cari.cari_kod}"))
                    self.result_layout.addWidget(QLabel(f"Cari Ad: {cari.cari_ad}"))
                    self.result_layout.addWidget(QLabel(f"Vergi Dairesi: {cari.vergi_dairesi}"))
                    self.result_layout.addWidget(QLabel(f"Vergi No: {cari.vergi_no}"))
                    self.result_layout.addWidget(QLabel(f"T.C. Kimlik No: {cari.tc_kimlik_no}"))
                    self.result_layout.addWidget(QLabel(f"Adres: {cari.adres}"))
                    self.result_layout.addWidget(QLabel(f"Telefon: {cari.telefon}"))
                    self.result_layout.addWidget(QLabel(f"Faks: {cari.faks}"))
                    self.result_layout.addWidget(QLabel(f"Email: {cari.email}"))
                    self.result_layout.addWidget(QLabel(f"Web Sitesi: {cari.web_sitesi}"))
                    self.result_layout.addWidget(QLabel(f"Banka Hesap Bilgileri: {cari.banka_hesap_bilgileri}"))
                    self.result_layout.addWidget(QLabel(f"İlgili Kişi: {cari.ilgili_kisi}"))
                    self.result_layout.addWidget(QLabel(f"Ödeme Tahsilat Koşulları: {cari.odeme_tahsilat_kosullari}"))
                    self.result_layout.addWidget(QLabel(f"Para Birimi: {cari.para_birimi}"))
                    self.result_layout.addWidget(QLabel(f"Risk Limiti: {cari.risk_limiti}"))
                    self.result_layout.addWidget(QLabel(f"Sektör: {cari.sektor}"))
                    self.result_layout.addWidget(QLabel(f"Notlar: {cari.notlar}"))
                    self.result_layout.addWidget(QLabel(f"Cari Türü: {cari.cari_turu}"))
                    self.result_layout.addWidget(QLabel("------------------------------"))
            else:
                QMessageBox.warning(self, 'Bulunamadı', 'Girilen cari adı ile eşleşen kayıt bulunamadı.')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def clear_results(self):
        while self.result_layout.count():
            child = self.result_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
