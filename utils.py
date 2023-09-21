import os
from datetime import datetime
from PIL import Image

def save_img(image, folder_path):
    # รับวันที่ปัจจุบัน
    current_date = datetime.now().strftime('%d%m%y')

    # กำหนดโฟลเดอร์ที่คุณต้องการบันทึกภาพ
    folder_name = os.path.join(folder_path, current_date)

    # ตรวจสอบว่าโฟลเดอร์มีอยู่หรือไม่ หากไม่มีให้สร้างโฟลเดอร์
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # นับจำนวนไฟล์ที่มีในโฟลเดอร์แล้วเพื่อตัดรหัสรูปภาพให้ถูกต้อง
    existing_files = os.listdir(folder_name)
    image_count = len(existing_files) + 1

    # สร้างชื่อไฟล์รูปภาพ
    image_name = f"{image_count:05d}.jpg"  # ใช้รหัสลำดับ 5 หลัก (00001, 00002, ...)

    # บันทึกรูปภาพ
    image.save(os.path.join(folder_name, image_name))

# ตัวอย่างการใช้งาน
# สร้าง PIL Image จากไฟล์ภาพหรือข้อมูลภาพของคุณ
# image = Image.open("your_image.jpg")
# ส่งรูปภาพและโฟลเดอร์ปลายทางไปยังฟังก์ชัน
# save_image_with_date_and_sequence(image, "/path/to/your/folder")
