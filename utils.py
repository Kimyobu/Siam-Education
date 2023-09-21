import os
import subprocess
import argparse
from datetime import datetime
from PIL import Image

parser = argparse.ArgumentParser(description="")
parser.add_argument("venv", type=str)

args = parser.parse_args()

venv = args.venv

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

def run(cmd: str):
    return subprocess.run(f"source {venv}; {cmd}", shell=True)

def is_installed(name: str, pkg_version: str or None = None, operator: str = '=='):
    out = False
    try:
        package = importlib.util.find_spec(name)
        if package is not None:
            out = True
            if pkg_version is not None:
                ver = version(package.name)
                if operator == '==':
                    out = (ver == pkg_version)
                elif operator == '>=':
                    out = (ver >= pkg_version)
                elif operator == '<=':
                    out = (ver <= pkg_version)
                elif operator == '<':
                    out = (ver < pkg_version)
                elif operator == '>':
                    out = (ver > pkg_version)
                elif operator == '!=':
                    out = (ver != pkg_version)
                elif operator == '~=':
                    out = (pkg_version in package.requires)
    except ModuleNotFoundError:
        pass
    return out

def run_pip(install_syntax: str):
    operators = ['<', '>', '==', '>=', '<=' , '!=']
    found = []

    for op in operators:
        if op in install_syntax:
            found.append(op)

    operator = found[-1] if len(found) > 0 else '=='

    if operator is not None:
        package_info = install_syntax.split(operator)
        name = package_info[0].strip()
        version = package_info[1].strip() if len(package_info) > 1 else None

        if is_installed(name, version, operator) is False and name != '':
            print(f'Install {install_syntax}')
            run(f"pip install --no-cache-dir -q {install_syntax}")
            
def install_req(file):
    op = open(file, 'r')
    r = op.read()
    op.close()
    for x in r.split('\n'):
        run_pip(x)