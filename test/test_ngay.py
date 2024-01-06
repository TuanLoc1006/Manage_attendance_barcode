import datetime

# Lấy ngày hiện tại
today = datetime.date.today()

# Chuyển đổi sang ngày tháng năm
day = today.strftime("%d/%m/%Y")

# In ngày tháng năm
print(day)
