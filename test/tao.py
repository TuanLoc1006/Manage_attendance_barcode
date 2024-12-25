from barcode import Code128 , Code39
from io import BytesIO
from barcode.writer import ImageWriter

rv = BytesIO()

barCodeMssv = "B2013421"
numeric_part = ''.join(filter(str.isdigit, barCodeMssv))  # Lọc ra chỉ các chữ số
first_8_digits = numeric_part[:8] 
# Tạo một thể hiện của lớp ImageWriter và thiết lập kích thước
writer = ImageWriter()
writer.set_options({'module_width': 0.3, 'module_height': 10})  # Điều chỉnh kích thước module

# Tạo và lưu mã vạch với kích thước được thiết lập
Code39(barCodeMssv, writer=writer).write(rv)
with open("E:\\CTU\\HK2_nam_4_2023-2024\\NLMMT\\test\\"+barCodeMssv + ".png", "wb") as f:
    Code39(barCodeMssv, writer=writer).write(f)
