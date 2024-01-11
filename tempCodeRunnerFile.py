
    def layDanhSachLop(self):
        try:
            ma_hoc_phan = self.uic.input_ma_mon.text()
            nhom = self.uic.input_nhom.text()
            mycursor = mydb.cursor()
            
            # Execute the SQL query
            mycursor.execute("""
                SELECT diem_danh.mssv, thoi_khoa_bieu.ngay, diem_danh.trang_thai, diem_danh.tuan_hoc
                FROM dang_ky_mon_hoc 
                JOIN diem_danh ON diem_danh.mssv = dang_ky_mon_hoc.mssv 
                JOIN thoi_khoa_bieu ON thoi_khoa_bieu.tuan_hoc = diem_danh.tuan_hoc
                WHERE dang_ky_mon_hoc.ma_mon = %s AND dang_ky_mon_hoc.nhom = %s
            """, (ma_hoc_phan, nhom))
            
            myresult = mycursor.fetchall()
            
            # Clear the table before loading new data
            self.uic.bang_danh_sach.setRowCount(0)
            
            if not myresult:
                message = QtWidgets.QMessageBox()
                message.setText(f"Không tìm thấy lớp học")
                message.exec_()
            else:
                week_data = {}  # Dictionary to store data for each week
                
                for row_number, row_data in enumerate(myresult):
                    mssv, ngay, trang_thai, tuan_hoc = row_data
                    
                    # Check if the week is already in the dictionary
                    if tuan_hoc not in week_data:
                        week_data[tuan_hoc] = {'ngay': [ngay], 'trang_thai': [trang_thai]}
                    else:
                        week_data[tuan_hoc]['ngay'].append(ngay)
                        week_data[tuan_hoc]['trang_thai'].append(trang_thai)
                
                # Add columns for each week
                self.uic.bang_danh_sach.setColumnCount(len(week_data))
                
                # Set column headers with week numbers
                for col_number, week_number in enumerate(sorted(week_data.keys())):
                    self.uic.bang_danh_sach.setHorizontalHeaderItem(col_number, QtWidgets.QTableWidgetItem(f'Tuần {week_number}'))
                    
                    # Add data to the table
                    for row_number in range(len(myresult)):
                        ngay_data = week_data[week_number]['ngay']
                        trang_thai_data = week_data[week_number]['trang_thai']
                        
                        # If row number is within the range of the ngay_data list
                        if row_number < len(ngay_data):
                            ngay_item = QtWidgets.QTableWidgetItem(str(ngay_data[row_number]))
                            trang_thai_item = QtWidgets.QTableWidgetItem(str(trang_thai_data[row_number]))
                            self.uic.bang_danh_sach.setItem(row_number, col_number * 2, ngay_item)
                            self.uic.bang_danh_sach.setItem(row_number, col_number * 2 + 1, trang_thai_item)
        
        except Exception as e:
            message = QtWidgets.QMessageBox()
            message.setText(f"Lỗi: {str(e)}")
            message.exec_()

 