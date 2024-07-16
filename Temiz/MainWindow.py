# MainWindow.py
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QMessageBox
from Entity.MainWindow_ui import Ui_MainWindow
from Service.CariKarti_Service import CariKartiService
from Service.GirisFisi_Service import GirisFisiService
from Service.CikisFisi_Service import CikisFisiService
from Service.StokKarti_Service import StokKartiService
from Repository.CariKarti_Repository import CariKartiRepository
from Repository.GirisFisi_Repository import GirisFisiRepository
from Repository.CikisFisi_Repository import CikisFisiRepository
from Repository.StokKarti_Repository import StokKartiRepository
from Entity.CariGorWidget import CariGorWidget
from Entity.CariEkleWidget import CariEkleWidget
from Entity.CariBulWidget import CariBulWidget
from Entity.StokGorWidget import StokGorWidget
from Entity.StokEkleWidget import StokEkleWidget
from Entity.GirisFisiWidget import GirisFisiWidget
from Entity.GirisFisiGorWidget import GirisFisiGorWidget
from Entity.CikisFisiWidget import CikisFisiWidget
from Entity.YapilanCikisFisleriWidget import YapilanCikisFisleriWidget  # Yeni eklenen import

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.current_widget = None  # Mevcut widget
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DIOR\\SQLEXPRESS;DATABASE=barcode_db;UID=sa;PWD=1881'
        self.cari_karti_service = CariKartiService(CariKartiRepository(connection_string))
        self.giris_fisi_service = GirisFisiService(GirisFisiRepository(connection_string))
        self.cikis_fisi_service = CikisFisiService(CikisFisiRepository(connection_string))
        self.stok_karti_service = StokKartiService(StokKartiRepository(connection_string))

    def initUI(self):
        self.actionCariler.triggered.connect(self.cari_gor)
        self.actionCari_Ekle.triggered.connect(self.cari_ekle)
        self.actionCari_Bul.triggered.connect(self.cari_bul)
        self.actionStoklar.triggered.connect(self.stok_gor)
        self.actionStok_ekle.triggered.connect(self.stok_ekle)
        self.actionGiri_Fi_i.triggered.connect(self.giris_fisi)
        self.actionYap_lan_Giri_Fi_leri.triggered.connect(self.yapilan_giris_fisleri)
        self.action_k_Fi_i.triggered.connect(self.cikis_fisi)
        self.actionYap_lan_k_fi_leri.triggered.connect(self.yapilan_cikis_fisleri)

    def set_central_widget(self, widget):
        if self.current_widget is not None:
            if self.centralWidget().layout() is not None:
                self.centralWidget().layout().removeWidget(self.current_widget)
            self.current_widget.deleteLater()
        self.current_widget = widget
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(widget)
        self.setCentralWidget(central_widget)

    def cari_gor(self):
        try:
            cariler = self.cari_karti_service.get_all_cariler()
            widget = CariGorWidget(cariler, self.cari_karti_service)
            widget.set_service(self.cari_karti_service)  # Servis referansını set ediyoruz
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def cari_ekle(self):
        try:
            widget = CariEkleWidget(self.cari_karti_service)
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def cari_bul(self):
        try:
            widget = CariBulWidget(self.cari_karti_service)
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def stok_gor(self):
        try:
            stoklar = self.stok_karti_service.get_all_stoklar()
            widget = StokGorWidget(stoklar, self.stok_karti_service)
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def stok_ekle(self):
        try:
            widget = StokEkleWidget(self.stok_karti_service)
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def giris_fisi(self):
        try:
            widget = GirisFisiWidget(self.giris_fisi_service)
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def yapilan_giris_fisleri(self):
        try:
            giris_fisleri = self.giris_fisi_service.get_all_giris_fisleri()
            widget = GirisFisiGorWidget(giris_fisleri, self.giris_fisi_service)
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def cikis_fisi(self):
        try:
            widget = CikisFisiWidget(self.cikis_fisi_service)  # CikisFisiWidget kullanımı
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

    def yapilan_cikis_fisleri(self):
        try:
            widget = YapilanCikisFisleriWidget(self.cikis_fisi_service)  # YapilanCikisFisleriWidget kullanımı
            self.set_central_widget(widget)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
