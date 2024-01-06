import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog,QMessageBox 
from quanLyDiemDanh import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui,QtWidgets
from barcode import Code128
from io import BytesIO
from barcode.writer import ImageWriter
rv = BytesIO()

# mo webcam
import cv2
from pyzbar.pyzbar import decode
import numpy as np 

# xuat du lieu ra file
import openpyxl
# tao am thanh
import winsound
frequency = 2000  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second
# import ham time
import time
#ket noi voi xampp
import mysql.connector
# import ngay gio
import datetime

# mydb = mysql.connector.connect(
#     host='localhost',
#     username='root',
#     password='',
#     port='3306',
#     database='project_barcode'
# )

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.btn_openCam.clicked.connect(self.openCameraBarCode)
        self.uic.btn_export_file.clicked.connect(self.export_to_excel)
        # Lấy ngày hiện tại
        today = datetime.date.today()
        # Chuyển đổi sang ngày tháng năm
        day = today.strftime("%d/%m/%Y")
        self.uic.input_ngay.setText(day)
    def openCameraBarCode(self):
        self.cam_0 = cv2.VideoCapture(0)  
       

        while True:
            try:
                _, self.frame_so_0 = self.cam_0.read()
               
                # xu ly nhan dien ma vach
                for code in decode(self.frame_so_0):
                    pts = np.array([code.polygon], np.int32)
                    pts = pts.reshape(((-1,1,2)))
                    cv2.polylines(self.frame_so_0, [pts], True, (0,0,255), 3)
                    data = code.data.decode('utf-8')
                    winsound.Beep(frequency, duration)
                    time.sleep(1)
                    print(data)
                    self.handle_barcode_scanned(data)


                # hien len man hinh fram
                self.frame_so_0 = cv2.cvtColor(self.frame_so_0, cv2.COLOR_BGR2RGB)
                self.update()
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.cam_0.release()
                    self.cam_1.release()
                    self.cam_2.release()
                    cv2.destroyAllWindows()
                    break
            except IndexError:
                self.clearData()
                msg = QMessageBox()
                msg.setText('Ma QR khong dung, xin vui long quet lai!')
                msg.exec_()
                
            except TypeError:
                break


    def handle_barcode_scanned(self, barcode_data):
        # Thêm hàng mới vào bảng
        row_count = self.uic.bang_danh_sach.rowCount()
        self.uic.bang_danh_sach.insertRow(row_count)

        # Đặt mã số vào cột đầu tiên
        item = QtWidgets.QTableWidgetItem(barcode_data)
        self.uic.bang_danh_sach.setItem(row_count, 0, item)

        # Đặt trạng thái điểm danh vào cột thứ hai
        item = QtWidgets.QTableWidgetItem("Có mặt")  # Hoặc trạng thái khác tùy theo nhu cầu
        self.uic.bang_danh_sach.setItem(row_count, 1, item)

    def update(self):
        self.setPhoto(self.frame_so_0)
        

    def setPhoto(self,image):
        image = cv2.resize(image,(331,251))
        img = QtGui.QImage(image,image.shape[1],image.shape[0], image.strides[0],QtGui.QImage.Format_RGB888)
        self.uic.label_frameBarCode.setPixmap(QtGui.QPixmap.fromImage(img))
       
        
    def export_to_excel(self):
        # lay du lieu tu input
        hoten_GV = self.uic.input_hoTenGV.text()
        ma_mon = self.uic.input_ma_mon.text()
        nhom = self.uic.input_nhom.text()
        ngay = self.uic.input_ngay.text()
        # self.uic
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Đặt tiêu đề cột
        sheet['A1'] = 'Mã số sinh viên'
        sheet['B1'] = 'Trạng thái'
        sheet['C1'] = 'Giảng viên'
        sheet['D1'] = 'Mã môn'
        sheet['E1'] = 'Nhóm'
        sheet['F1'] = 'Ngày'

        sheet['C2'].value = hoten_GV
        sheet['D2'].value = ma_mon
        sheet['E2'].value = nhom
        sheet['F2'].value = ngay
        # Lấy dữ liệu từ bảng và ghi vào file Excel
        row_count = self.uic.bang_danh_sach.rowCount()
        for row in range(1, row_count + 1):
            for col in range(3):  # 3 cột trong bảng
                item = self.uic.bang_danh_sach.item(row - 1, col)
                if item is not None:
                    sheet.cell(row=row + 1, column=col + 1).value = item.text()

        # Lưu file Excel
        file_name = 'danh_sach_diem_danh.xlsx'  # Tên file tùy chỉnh
        try:
            workbook.save(file_name)
            message = QMessageBox()
            message.setText("Xuất file Excel thành công!")
            message.exec_()
        except Exception as e:
            message = QMessageBox()
            message.setText(f"Lỗi khi xuất file Excel: {e}")
            message.exec_()

            
    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())