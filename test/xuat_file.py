import openpyxl

def export_to_excel(self):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Đặt tiêu đề cột
    sheet['A1'] = 'Mã số sinh viên'
    sheet['B1'] = 'Ngày'
    sheet['C1'] = 'Trạng thái'

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