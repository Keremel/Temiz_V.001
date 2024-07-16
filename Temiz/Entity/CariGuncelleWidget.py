# Entity/CariGuncelleWidget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from Temiz.Entity.CariKarti import CariKarti
from Temiz.Service.CariKarti_Service import CariKartiService


class CariGuncelleWidget(QWidget):
    def __init__(self, service: CariKartiService, cari, parent=None):
        super().__init__(parent)
        self.service = service
        self.cari = cari
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()

        self.cari_kod = QLineEdit(self)
        self.cari_kod.setReadOnly(True)
        self.cari_kod.setText(self.cari.cari_kod)

        self.cari_ad = QLineEdit(self)
        self.cari_ad.setText(self.cari.cari_ad)

        self.vergi_dairesi = QLineEdit(self)
        self.vergi_dairesi.setText(self.cari.vergi_dairesi)

        self.vergi_no = QLineEdit(self)
        self.vergi_no.setText(self.cari.vergi_no)

        self.tc_kimlik_no = QLineEdit(self)
        self.tc_kimlik_no.setMaxLength(11)
        self.tc_kimlik_no.setPlaceholderText('11 haneli T.C. Kimlik No')
        self.tc_kimlik_no.setText(self.cari.tc_kimlik_no)

        self.telefon = QLineEdit(self)
        self.telefon.setMaxLength(11)
        self.telefon.setPlaceholderText('11 haneli Telefon Numarası')
        self.telefon.setText(self.cari.telefon)

        self.faks = QLineEdit(self)
        self.faks.setText(self.cari.faks)

        self.email = QLineEdit(self)
        self.email.setText(self.cari.email)

        self.web_sitesi = QLineEdit(self)
        self.web_sitesi.setText(self.cari.web_sitesi)

        self.banka_hesap_bilgileri = QLineEdit(self)
        self.banka_hesap_bilgileri.setText(self.cari.banka_hesap_bilgileri)

        self.ilgili_kisi = QLineEdit(self)
        self.ilgili_kisi.setText(self.cari.ilgili_kisi)

        self.odeme_tahsilat_kosullari = QLineEdit(self)
        self.odeme_tahsilat_kosullari.setText(self.cari.odeme_tahsilat_kosullari)

        self.para_birimi = QLineEdit(self)
        self.para_birimi.setText(self.cari.para_birimi)

        self.risk_limiti = QLineEdit(self)
        self.risk_limiti.setText(self.cari.risk_limiti)

        self.sektor = QLineEdit(self)
        self.sektor.setText(self.cari.sektor)

        self.notlar = QLineEdit(self)
        self.notlar.setText(self.cari.notlar)

        self.cari_turu = QComboBox(self)
        self.cari_turu.addItems(['Satıcı', 'Alıcı', 'Satıcı/Alıcı'])
        self.cari_turu.setCurrentText(self.cari.cari_turu)

        self.adres = QLineEdit(self)
        self.adres.setText(self.cari.adres)

        # TC Kimlik No ve Telefon Numarası için doğrulayıcı ekleyelim
        regex = QRegExp(r'\d{11}')
        validator = QRegExpValidator(regex)
        self.tc_kimlik_no.setValidator(validator)
        self.telefon.setValidator(validator)

        self.form_layout.addRow('Cari Kod:', self.cari_kod)
        self.form_layout.addRow('Cari Adı:', self.cari_ad)
        self.form_layout.addRow('Vergi Dairesi:', self.vergi_dairesi)
        self.form_layout.addRow('Vergi No:', self.vergi_no)
        self.form_layout.addRow('T.C. Kimlik No:', self.tc_kimlik_no)
        self.form_layout.addRow('Telefon:', self.telefon)
        self.form_layout.addRow('Faks:', self.faks)
        self.form_layout.addRow('Email:', self.email)
        self.form_layout.addRow('Web Sitesi:', self.web_sitesi)
        self.form_layout.addRow('Banka Hesap Bilgileri:', self.banka_hesap_bilgileri)
        self.form_layout.addRow('İlgili Kişi:', self.ilgili_kisi)
        self.form_layout.addRow('Ödeme Tahsilat Koşulları:', self.odeme_tahsilat_kosullari)
        self.form_layout.addRow('Para Birimi:', self.para_birimi)
        self.form_layout.addRow('Risk Limiti:', self.risk_limiti)
        self.form_layout.addRow('Sektör:', self.sektor)
        self.form_layout.addRow('Notlar:', self.notlar)
        self.form_layout.addRow('Cari Türü:', self.cari_turu)
        self.form_layout.addRow('Adres:', self.adres)

        self.save_button = QPushButton('Güncelle', self)
        self.save_button.clicked.connect(self.update_cari_karti)

        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def update_cari_karti(self):
        cari_kod = self.cari_kod.text()
        cari_ad = self.cari_ad.text()
        vergi_dairesi = self.vergi_dairesi.text()
        vergi_no = self.vergi_no.text()
        tc_kimlik_no = self.tc_kimlik_no.text()
        adres = self.adres.text()
        telefon = self.telefon.text()
        faks = self.faks.text()
        email = self.email.text()
        web_sitesi = self.web_sitesi.text()
        banka_hesap_bilgileri = self.banka_hesap_bilgileri.text()
        ilgili_kisi = self.ilgili_kisi.text()
        odeme_tahsilat_kosullari = self.odeme_tahsilat_kosullari.text()
        para_birimi = self.para_birimi.text()
        risk_limiti = self.risk_limiti.text()
        sektor = self.sektor.text()
        notlar = self.notlar.text()
        cari_turu = self.cari_turu.currentText()

        if not cari_kod or not cari_ad or not tc_kimlik_no or not telefon:
            QMessageBox.warning(self, 'Eksik Bilgi', 'Lütfen gerekli alanları doldurunuz.')
            return

        if len(tc_kimlik_no) != 11:
            QMessageBox.warning(self, 'Hatalı Bilgi', 'T.C. Kimlik No 11 haneli olmalıdır.')
            return

        if len(telefon) != 11:
            QMessageBox.warning(self, 'Hatalı Bilgi', 'Telefon numarası 11 haneli olmalıdır.')
            return

        cari_karti = CariKarti(
            cari_kod=cari_kod,
            cari_ad=cari_ad,
            vergi_dairesi=vergi_dairesi,
            vergi_no=vergi_no,
            tc_kimlik_no=tc_kimlik_no,
            adres=adres,
            telefon=telefon,
            faks=faks,
            email=email,
            web_sitesi=web_sitesi,
            banka_hesap_bilgileri=banka_hesap_bilgileri,
            ilgili_kisi=ilgili_kisi,
            odeme_tahsilat_kosullari=odeme_tahsilat_kosullari,
            para_birimi=para_birimi,
            risk_limiti=risk_limiti,
            sektor=sektor,
            notlar=notlar,
            cari_turu=cari_turu
        )

        try:
            self.service.update_cari_karti(cari_karti)
            QMessageBox.information(self, 'Başarılı', 'Cari kartı başarıyla güncellendi.')
            self.close()  # Güncelleme başarılı olursa ekranı kapat
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
