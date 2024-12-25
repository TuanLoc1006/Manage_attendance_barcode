import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog,QMessageBox 
from dangKyMa import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui,QtWidgets

from barcode import Code128
from io import BytesIO
from barcode.writer import ImageWriter
rv = BytesIO()

import importlib
#ket noi voi xampp
import mysql.connector
# import regex
import re
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
        self.uic.btn_imgUser.clicked.connect(self.linkToUser)
        self.uic.btn_luuThongTin.clicked.connect(self.createBarcode)
        self.uic.btn_clear_input.clicked.connect(self.clear_input)
        self.uic.btn_dangKyHocPhan.clicked.connect(self.dangKyHocPhan)
        self.uic.btn_page_quanly.clicked.connect(self.pageQuanLy)

    def linkToUser(self):
        global link_name_user_pic
        #tim duong dan         
        link_name_user_pic = QFileDialog.getOpenFileName(filter='*.jpg *.png')
        #mo hinh anh len
        self.uic.label_user.setPixmap(QPixmap(link_name_user_pic[0]))

    # def pageQuanLy(self):
    #     self.main_win = xuLyDiemDanh.MainWindow()
    #     self.main_win.show()

    def pageQuanLy(self):
        if hasattr(self, 'main_win'):
            # Đóng cửa sổ hiện tại trước khi chuyển sang cửa sổ mới
            self.main_win.close()

        # Import lại module
        import xuLyDiemDanh
        importlib.reload(xuLyDiemDanh)

        # Tạo một thể hiện mới của lớp MainWindow
        self.main_win = xuLyDiemDanh.MainWindow()
        self.main_win.show()
            
    def createBarcode(self):
        try:
            if self.check_information() == 4:
                createQR = 1
                name = self.uic.input_hoTen.text()
                maSo = self.uic.input_maSo.text()
                soDienThoai = self.uic.input_phone.text()
                email = self.uic.input_email.text()
                gioiTinh =  self.uic.input_gioiTinh.currentText()
  
                anh_user = ""
                try:    
                    anh_user = link_name_user_pic[0]
                    print('======> anh dang ky:',anh_user)
                  
                except NameError:
                    pass
                    
                if not anh_user:
                    msg = QMessageBox()
                    msg.setText("Bạn chưa chọn ảnh đăng ký!!!")
                    msg.exec_()
                    createQR = 0
                mycursor = mydb.cursor()
                sql = " SELECT ma_so_sinh_vien FROM sinh_vien WHERE ma_so_sinh_vien = %s"
                adr = (maSo,)
                mycursor.execute(sql, adr)
                existing_record = mycursor.fetchall()
                if existing_record:
                    msg = QMessageBox()
                    msg.setText("Mã số sinh viên đã tồn tại trong cơ sở dữ liệu!")
                    msg.exec_()
                    createQR = 0
               
                # print(name,maSo,soDienThoai,email,gioiTinh,thoiHan)
                if createQR == 1 :
                    barCodeMssv = self.uic.input_maSo.text()
                    Code128(barCodeMssv, writer=ImageWriter()).write(rv)
                    with open("E:\\CTU\\HK2_nam_4_2023-2024\\NLMMT_full\\Users\\"+barCodeMssv+".png", "wb") as f:
                        Code128(barCodeMssv, writer=ImageWriter()).write(f)
                    # hien thi ma vach
                    self.uic.label_barCode.setPixmap(QPixmap("E:\\CTU\\HK2_nam_4_2023-2024\\NLMMT_full\\Users\\"+barCodeMssv+".png"))
                    
                    mycursor = mydb.cursor()
                    sql_sinh_vien = "INSERT INTO `sinh_vien`(`ma_so_sinh_vien`, `ho_ten`, `email`, `gioi_tinh`, `so_dien_thoai`, `anh_sinh_vien`) VALUES (%s,%s,%s,%s,%s,%s)"
                    val_sinh_vien = (maSo, name, email, gioiTinh, soDienThoai, anh_user  )
                    mycursor.execute(sql_sinh_vien, val_sinh_vien)
                    mydb.commit()
                    # print(mycursor.rowcount, "record inserted.")

        except Exception as e:
            print(f"Lỗi tao QR: {str(e)}")
            message = QtWidgets.QMessageBox()
            message.setText(f"Bạn chưa chọn ảnh đăng ký!!!")
            message.exec_()

    def dangKyHocPhan(self):
        try:
            mssv_dkhp = self.uic.input_mssv_dkhp.text()
            ma_hocPhan = self.uic.input_ma_hocPhan.text()
            nhom = self.uic.input_nhom_hocPhan.text()

            mycursor = mydb.cursor()
            sql = "SELECT  mssv, ma_mon FROM dang_ky_mon_hoc WHERE mssv=%s and ma_mon=%s"
            adr = (mssv_dkhp,ma_hocPhan)
            mycursor.execute(sql, adr)
            existing_record = mycursor.fetchall()
            if  existing_record:
                msg = QMessageBox()
                msg.setText("Mã số sinh viên đã đăng ký học phần này!")
                msg.exec_()
                return
            
            mycursor = mydb.cursor()
            sql_nhom = "SELECT stt_nhom FROM nhom WHERE ma_mon=%s AND stt_nhom=%s"
            val_nhom = (ma_hocPhan, nhom)
            mycursor.execute(sql_nhom, val_nhom)
            existing_record = mycursor.fetchall()
            if not existing_record:
                msg = QMessageBox()
                msg.setText("Nhóm không tồn tại!")
                msg.exec_()
                return
            mycursor = mydb.cursor()
            sql_DK_mon_hoc = "INSERT INTO `dang_ky_mon_hoc`(`mssv`, `ma_mon`, `nhom`) VALUES (%s,%s,%s)"
            val_DK_mon_hoc = (mssv_dkhp, ma_hocPhan, nhom)
            mycursor.execute(sql_DK_mon_hoc, val_DK_mon_hoc)
            mydb.commit()
           
            msg = QMessageBox()
            msg.setText("Đăng ký thành công")
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setText("Đăng ký thất bại")
            msg.exec_()

    def clear_input(self):  
        self.uic.label_user.setPixmap(QPixmap("E:\\CTU\\HK2_nam_4_2023-2024\\NLMMT_full\\img\\pic_user.png"))
        global link_name_user_pic
        link_name_user_pic = None
        self.uic.label_barCode.setPixmap(QPixmap(""))
        self.uic.input_hoTen.setText('') 
        self.uic.input_maSo.setText('') 
        self.uic.input_phone.setText('') 
        self.uic.input_email.setText('') 
        self.uic.label_barCode.setText('Mã vạch')

    
    regex_email = re.compile(r"^[A-Za-z0-9\.\+\_-]+@[A-Za-z0-9\._-]+\.[A-Za-z]+$")
    def validate_email(self,email):
        # Sử dụng phương thức fullmatch để so khớp với chuỗi
        if self.regex_email.fullmatch(email):
            return True
        else:
            return False
        
    regex_name = re.compile(r"^[A-Za-z\s'-]+$")
    def validate_name(self,name):
        if self.regex_name.fullmatch(name) and not self.uic.input_hoTen.text().isspace():
            return True
        else:
            self.uic.input_hoTen.setFocus()
            return False
        
    def check_information(self):
        count = 0
        message = ""
        if self.validate_name(self.uic.input_hoTen.text()):
            count+=1
        else:
            message+= ('Họ tên không hợp lệ\n')

        if len(str(self.uic.input_maSo.text()))!=8 :
            message+=('Mã số sinh viên không hợp lệ\n')
        else: 
            count+=1
            
        if len(str(self.uic.input_phone.text()))<12:
            message+=('Số điện thoại không hợp lệ\n')
        else: 
            count+=1
       
        if self.validate_email(self.uic.input_email.text()):
            count+=1
        else:
            message+= ('Email không hợp lệ\n') 
       
        if(count<4):
            msg = QMessageBox()
            message+=('Vui lòng kiểm tra thông tin!\n')
            msg.setText(message)
            msg.exec_()
        
        return count    

    def show(self):
        self.main_win.show()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     main_win.show()
#     sys.exit(app.exec())
        

                   