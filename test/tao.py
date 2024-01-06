from barcode import Code128
from io import BytesIO
from barcode.writer import ImageWriter

rv = BytesIO()
barCodeMssv = "b2013421"

# Tạo một thể hiện của lớp ImageWriter và thiết lập kích thước
writer = ImageWriter()
writer.set_options({'module_width': 0.3, 'module_height': 10})  # Điều chỉnh kích thước module

# Tạo và lưu mã vạch với kích thước được thiết lập
Code128(barCodeMssv, writer=writer).write(rv)
with open(barCodeMssv + ".png", "wb") as f:
    Code128(barCodeMssv, writer=writer).write(f)
