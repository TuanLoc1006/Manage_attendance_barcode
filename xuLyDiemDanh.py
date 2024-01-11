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

mydb = mysql.connector.connect(
    host='localhost',
    username='root',
    password='',
    port='3306',
    database='project_barcode'
)

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.btn_openCam.clicked.connect(self.openCameraBarCode)
        self.uic.btn_export_file.clicked.connect(self.export_to_excel)
        self.uic.btn_tim_danhSach.clicked.connect(self.layDanhSachLop)
        self.uic.btn_luu_danh_sach.clicked.connect(self.luu_danh_sach)
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
        try:
            # Kiểm tra xem mã vạch có khớp với dữ liệu nào trong cột đầu tiên không
            found = False
            for row in range(self.uic.bang_danh_sach.rowCount()):
                item = self.uic.bang_danh_sach.item(row, 0)  # Giả sử mã vạch ở cột đầu tiên
                if item is not None and item.text() == barcode_data:
                    # Cập nhật trạng thái điểm danh (cột thứ hai) để chỉ ra sự có mặt
                    status_item = QtWidgets.QTableWidgetItem("Có mặt")
                    self.uic.bang_danh_sach.setItem(row, 1, status_item)
                    found = True
                    break

            if not found:
                # Nếu mã vạch không khớp với dữ liệu nào, thêm hàng mới vào bảng
                row_count = self.uic.bang_danh_sach.rowCount()
                self.uic.bang_danh_sach.insertRow(row_count)
                # Đặt mã vạch vào cột đầu tiên
                barcode_item = QtWidgets.QTableWidgetItem(barcode_data)
                self.uic.bang_danh_sach.setItem(row_count, 0, barcode_item)
                # Đặt trạng thái mặc định vào cột thứ hai
                status_item = QtWidgets.QTableWidgetItem("Có mặt")
                self.uic.bang_danh_sach.setItem(row_count, 1, status_item)

        except Exception as e:
            message = QMessageBox()
            message.setText(f"Lỗi: {str(e)}")
            message.exec_()

    def update(self):
        self.setPhoto(self.frame_so_0)
        

    def setPhoto(self,image):
        image = cv2.resize(image,(331,251))
        img = QtGui.QImage(image,image.shape[1],image.shape[0], image.strides[0],QtGui.QImage.Format_RGB888)
        self.uic.label_frameBarCode.setPixmap(QtGui.QPixmap.fromImage(img))
       
    # def layDanhSachLop(self):

    #     # SELECT 
    #     # diem_danh.mssv, thoi_khoa_bieu.ngay, diem_danh.trang_thai,diem_danh.tuan_hoc 
    #     # FROM 
    #     # dang_ky_mon_hoc join diem_danh 
    #     # on diem_danh.mssv = dang_ky_mon_hoc.mssv 
    #     # join thoi_khoa_bieu on thoi_khoa_bieu.tuan_hoc = diem_danh.tuan_hoc
    #     # WHERE dang_ky_mon_hoc.ma_mon = 'ct111' 

    #     try:
    #         ma_hoc_phan = self.uic.input_ma_mon.text()
    #         nhom = self.uic.input_nhom.text()
    #         mycursor = mydb.cursor()
    #         mycursor.execute("SELECT `ma_so_sinh_vien` FROM `dang_ky_mon_hoc` WHERE ma_mon = %s and nhom = %s", (ma_hoc_phan, nhom))
            
    #         myresult = mycursor.fetchall()
            
    #         # Làm rỗng bảng trước khi load dữ liệu mới
    #         self.uic.bang_danh_sach.setRowCount(0)
            
    #         if not myresult:
    #             message = QMessageBox()
    #             message.setText(f"Không tìm thấy lớp học")
    #             message.exec_()

    #         for row_number, row_data in enumerate(myresult):
    #             self.uic.bang_danh_sach.insertRow(row_number)
                
    #             # Chỉ lấy cột đầu tiên (mã số sinh viên)
    #             data = row_data[0]
                
    #             self.uic.bang_danh_sach.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(data)))
    #     except Exception as e:
    #         message = QMessageBox()
    #         message.setText(f"Lỗi")
    #         message.exec_()

    
    def layDanhSachLop(self):
        try:
            ma_hoc_phan = self.uic.input_ma_mon.text()
            nhom = self.uic.input_nhom.text()
            mycursor = mydb.cursor()

            # Thực hiện truy vấn SQL
            mycursor.execute("""
                SELECT diem_danh.mssv, diem_danh.trang_thai, diem_danh.tuan_hoc
                FROM dang_ky_mon_hoc 
                JOIN diem_danh ON diem_danh.mssv = dang_ky_mon_hoc.mssv 
                WHERE diem_danh.ma_hoc_phan = %s and diem_danh.nhom = %s
            """, (ma_hoc_phan, nhom))

            myresult = mycursor.fetchall()

            # Xóa bảng trước khi tải dữ liệu mới
            self.uic.bang_danh_sach.setRowCount(0)

            if not myresult:
                message = QtWidgets.QMessageBox()
                message.setText(f"Không tìm thấy lớp học")
                message.exec_()
            else:
                # Tạo một từ điển để lưu trữ dữ liệu cho mỗi mssv và tuần
                mssv_data = {}

                for row_number, row_data in enumerate(myresult):
                    mssv, trang_thai, tuan_hoc = row_data

                    # Kiểm tra xem mssv đã tồn tại trong từ điển chưa
                    if mssv not in mssv_data:
                        mssv_data[mssv] = {'tuans': {tuan_hoc: trang_thai}}
                    else:
                        mssv_data[mssv]['tuans'][tuan_hoc] = trang_thai

                # Tạo một danh sách các tuần duy nhất và thêm tuần hiện tại vào cuối cùng
                unique_weeks = sorted(set(tuan for mssv_info in mssv_data.values() for tuan in mssv_info['tuans']))
                current_week = "tuần hiện tại"
                unique_weeks.append(current_week)

                # Thêm cột cho mỗi tuần
                self.uic.bang_danh_sach.setColumnCount(1 + len(unique_weeks))

                # Đặt tiêu đề cho cột đầu tiên
                self.uic.bang_danh_sach.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('mssv'))

                # Đặt tiêu đề cho mỗi tuần
                for col_number, week in enumerate(unique_weeks):
                    self.uic.bang_danh_sach.setHorizontalHeaderItem(1 + col_number, QtWidgets.QTableWidgetItem(f'{week}'))

                # Thêm dữ liệu vào bảng
                for row_number, (mssv, mssv_info) in enumerate(mssv_data.items()):
                    self.uic.bang_danh_sach.insertRow(row_number)

                    # Đặt mssv trong cột đầu tiên
                    self.uic.bang_danh_sach.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(mssv)))

                    # Đặt trạng thái điểm danh cho mỗi tuần
                    for col_number, week in enumerate(unique_weeks):
                        trang_thai = mssv_info['tuans'].get(week, '')
                        self.uic.bang_danh_sach.setItem(row_number, 1 + col_number, QtWidgets.QTableWidgetItem(trang_thai))

        except Exception as e:
            message = QtWidgets.QMessageBox()
            message.setText(f"Lỗi: {str(e)}")
            message.exec_()



    
    

    def luu_danh_sach(self):
        try:
            ma_hoc_phan = self.uic.input_ma_mon.text()
            nhom = self.uic.input_nhom.text()
            ngay = self.uic.input_ngay.text()
            tuan = self.uic.input_tuan.text()
            mycursor = mydb.cursor()

            # Lặp qua từng dòng trong bảng để lưu dữ liệu vào CSDL
            for row in range(self.uic.bang_danh_sach.rowCount()):
                mssv_item = self.uic.bang_danh_sach.item(row, 0)  # Cột mã số sinh viên
                trang_thai_item = self.uic.bang_danh_sach.item(row, 1)  # Cột trạng thái điểm danh


                # if mssv_item is not None and trang_thai_item is not None:
                mssv = mssv_item.text()
                trang_thai = trang_thai_item.text()
                # print(mssv, ma_hoc_phan, nhom, tuan, trang_thai)
                sql_diem_danh = "INSERT INTO `diem_danh`(`id`, `mssv`, `ma_hoc_phan`, `nhom`, `tuan_hoc`, `trang_thai`)  VALUES ('', %s, %s, %s, %s, %s)"
                val_diem_danh = (mssv, ma_hoc_phan, nhom, tuan, trang_thai)
                mycursor.execute(sql_diem_danh, val_diem_danh)

                sql_tkb = "INSERT INTO `thoi_khoa_bieu`(`id`, `tuan_hoc`, `ngay`) VALUES ('',%s,%s)"
                val_tkb = (tuan,ngay)
                mycursor.execute(sql_tkb, val_tkb)
            mydb.commit()
            # Thông báo thành công
            if mssv_item is not None and trang_thai_item is not None:
                success_message = QMessageBox()
                success_message.setText("Lưu điểm danh thành công")
                success_message.exec_()

        except Exception:
            # Thông báo lỗi nếu có
            error_message = QMessageBox()
            error_message.setText(f"Chưa điểm danh !")
            error_message.exec_()       


        
    def export_to_excel(self):
        # lay du lieu tu input
        hoten_GV = self.uic.input_hoTenGV.text()
        ma_mon = self.uic.input_ma_mon.text()
        nhom = self.uic.input_nhom.text()
        ngay = self.uic.input_ngay.text()

        # Workbook and active sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        # Set headers
        headers = ['Giảng viên', 'Mã môn','Nhóm']
        for col_num, header in enumerate(headers, start=1):
            sheet.cell(row=1, column=col_num).value = header

        # Set values
        values = [hoten_GV, ma_mon, nhom]
        for col_num, value in enumerate(values, start=1):
            sheet.cell(row=2, column=col_num).value = value

        # Lấy dữ liệu từ bảng và ghi vào file Excel
        row_count = self.uic.bang_danh_sach.rowCount()
        start_row_excel = 5  # Adjust the starting row as needed

        for row in range(start_row_excel, start_row_excel + row_count):
            for col in range(1, 4):  # 3 cột trong bảng
                item = self.uic.bang_danh_sach.item(row - start_row_excel, col - 1)
                if item is not None:
                    sheet.cell(row=row, column=col).value = item.text()

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