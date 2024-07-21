import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QApplication
from PyQt5.QtCore import QDate, pyqtSignal
from Temiz.Entity.GirisFisi import GirisFisi
from Temiz.Repository.GirisFisi_Repository import GirisFisiRepository
from Temiz.Service.GirisFisi_Service import GirisFisiService
from .GirisFisi_ui import Ui_Form

class GirisFisiWidget(QWidget, Ui_Form):
    giris_fisi_olusturuldu = pyqtSignal()

    def __init__(self, giris_fisi_service):
        super().__init__()
        self.giris_fisi_service = giris_fisi_service
        self.setupUi(self)
        self.init_ui()
        self.current_stock_info = None

    def init_ui(self):
        self.setWindowTitle('Giriş Fişi Oluştur')

        # Set current date and make it readonly
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setReadOnly(True)

        # Set signals
        self.pushButton_urunekle.clicked.connect(self.add_product)
        self.pushButton_hepsinikaydet.clicked.connect(self.save_giris_fisi)
        self.pushButton_Ara.clicked.connect(self.search_stock_code)

        # Set auto-generated fis no
        self.set_auto_fis_no()

        # Tabloları yeniden yapılandırma
        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setHorizontalHeaderLabels(
            ['Stok Kodu', 'Stok Adı', 'Birim', 'Birim Fiyat', 'Aktif Miktar', 'Toplam Tutar'])

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Stok Kodu', 'Stok Adı', 'Birim', 'Birim Fiyat', 'Girecek Miktar', 'Toplam Tutar', 'Kalan Miktar'])

    def set_auto_fis_no(self):
        self.lineEdit_fisno.setText(self.giris_fisi_service.generate_new_fis_no())

    def search_stock_code(self):
        try:
            stokkod = self.lineEdit_stokkodu.text()
            if not self.giris_fisi_service.check_stok_kodu(stokkod):
                QMessageBox.critical(self, 'Hata', 'Stok kodu sistemde kayıtlı değil.')
                return

            self.current_stock_info = self.giris_fisi_service.get_stock_info(stokkod)
            if self.current_stock_info:
                stokad = self.current_stock_info['StokAd']
                birim = self.current_stock_info['Birim']
                birimfiyat = float(self.current_stock_info['BirimFiyat'])
                aktifmiktar = float(self.current_stock_info['MevcutStokMiktari'])

                # Tablodaki mevcut bilgileri temizleyelim
                self.tableWidget_2.setRowCount(0)

                # Ürün bilgilerini tabloya ekleyelim
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)
                self.tableWidget_2.setItem(row_position, 0, QTableWidgetItem(stokkod))
                self.tableWidget_2.setItem(row_position, 1, QTableWidgetItem(stokad))
                self.tableWidget_2.setItem(row_position, 2, QTableWidgetItem(birim))
                self.tableWidget_2.setItem(row_position, 3, QTableWidgetItem(str(birimfiyat)))
                self.tableWidget_2.setItem(row_position, 4, QTableWidgetItem(str(aktifmiktar)))
                self.tableWidget_2.setItem(row_position, 5, QTableWidgetItem(str(birimfiyat * aktifmiktar)))

                # Ürün bilgilerini güncelle
                self.current_stock_info['StokAd'] = stokad
                self.current_stock_info['Birim'] = birim
                self.current_stock_info['BirimFiyat'] = birimfiyat
                self.current_stock_info['MevcutStokMiktari'] = aktifmiktar

            else:
                QMessageBox.critical(self, 'Hata', 'Stok bilgileri alınamadı.')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Stok bilgilerini alırken bir hata oluştu: {e}')
            print(f"Exception: {e}")

    def add_product(self):
        try:
            if self.current_stock_info is None:
                QMessageBox.critical(self, 'Hata', 'Önce stok kodunu arayınız.')
                return

            stokkod = self.lineEdit_stokkodu.text()
            stokad = self.current_stock_info['StokAd']
            birim = self.current_stock_info['Birim']
            birimfiyat = float(self.current_stock_info['BirimFiyat'])
            aktifmiktar = float(self.current_stock_info['MevcutStokMiktari'])
            miktar = float(self.lineEdit_miktar.text())

            toplam_tutar = miktar * birimfiyat
            kalan_miktar = aktifmiktar + miktar

            # Ürün detaylarını alt tabloya ekleyelim
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(stokkod))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(stokad))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(birim))
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(birimfiyat)))
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(miktar)))
            self.tableWidget.setItem(row_position, 5, QTableWidgetItem(str(toplam_tutar)))
            self.tableWidget.setItem(row_position, 6, QTableWidgetItem(str(kalan_miktar)))

            # Güncellenen aktif miktarı yukarıdaki tabloya da ekleyelim
            self.tableWidget_2.setItem(0, 4, QTableWidgetItem(str(kalan_miktar)))
            self.tableWidget_2.setItem(0, 5, QTableWidgetItem(str(birimfiyat * kalan_miktar)))

            # MevcutStokMiktari'yi güncelle
            self.current_stock_info['MevcutStokMiktari'] = kalan_miktar

        except ValueError as e:
            QMessageBox.critical(self, 'Hata', f'Geçersiz değer hatası: {e}')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bilinmeyen bir hata oluştu: {e}')
            print(f"Exception: {e}")

    def save_giris_fisi(self):
        try:
            fis_no = self.lineEdit_fisno.text()
            fis_tarihi = self.dateEdit.date().toString("yyyy-MM-dd")

            row_count = self.tableWidget.rowCount()
            for row in range(row_count):
                stokkod_item = self.tableWidget.item(row, 0)
                stokad_item = self.tableWidget.item(row, 1)
                birim_item = self.tableWidget.item(row, 2)
                miktar_item = self.tableWidget.item(row, 4)
                birimfiyat_item = self.tableWidget.item(row, 3)
                toplam_tutar_item = self.tableWidget.item(row, 5)
                kalan_miktar_item = self.tableWidget.item(row, 6)

                if None in (stokkod_item, stokad_item, birim_item, miktar_item, birimfiyat_item, toplam_tutar_item,
                            kalan_miktar_item):
                    QMessageBox.critical(self, 'Hata', 'Tabloda eksik bilgi var.')
                    return

                stokkod = stokkod_item.text() if stokkod_item else ''
                stokad = stokad_item.text() if stokad_item else ''
                birim = birim_item.text() if birim_item else ''
                miktar = float(miktar_item.text()) if miktar_item else 0.0
                birim_fiyat = float(birimfiyat_item.text()) if birimfiyat_item else 0.0
                toplam_tutar = float(toplam_tutar_item.text()) if toplam_tutar_item else 0.0
                kalan_miktar = float(kalan_miktar_item.text()) if kalan_miktar_item else 0.0

                giris_fisi = GirisFisi(fis_no, fis_tarihi, stokkod, stokad, birim, miktar, birim_fiyat, toplam_tutar,
                                       kalan_miktar)
                self.giris_fisi_service.save_giris_fisi(fis_no, fis_tarihi, stokkod, stokad, birim, miktar, birim_fiyat,
                                                        toplam_tutar, kalan_miktar)

            QMessageBox.information(self, 'Başarılı', 'Giriş fişi başarıyla kaydedildi.')
            self.set_auto_fis_no()
            self.giris_fisi_olusturuldu.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')
            print(f"Exception: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DIOR\\SQLEXPRESS;DATABASE=barcode_db;UID=sa;PWD=1881'
    repository = GirisFisiRepository(connection_string)
    service = GirisFisiService(repository)
    widget = GirisFisiWidget(service)
    widget.show()
    sys.exit(app.exec_())
