import os
import torch
import torchvision.transforms as T
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

def display_images_sorted(folder_path, num_cols=4, image_width=4):
    # อ่านรายชื่อไฟล์รูปภาพและเรียงลำดับตามวันที่และเวลา
    image_filenames = sorted([f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))], 
                             key=lambda x: os.path.getctime(os.path.join(folder_path, x)), reverse=True)

    num_images = len(image_filenames)
    num_rows = (num_images + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(image_width * num_cols, image_width * num_rows))
    axes = axes.flatten()

    for i, filename in enumerate(image_filenames):
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path)
        
        # แสดงรูปภาพในกริด
        axes[i].imshow(img)
        axes[i].set_title(filename)
        axes[i].axis('off')

    # ปรับลำดับของกริดและเฉพาะบรรทัดสุดท้ายหากไม่เต็มแถว
    for i in range(num_images, num_rows * num_cols):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()

def display_images_in_grid(image_list, num_cols=4, image_width=4):
    num_images = len(image_list)
    num_rows = (num_images + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(image_width * num_cols, image_width * num_rows))
    axes = axes.flatten()

    for i, img in enumerate(image_list):
        axes[i].imshow(img)
        axes[i].axis('off')

    for i in range(num_images, num_rows * num_cols):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()

def tensor_to_image(tensor):
    # ใช้ transform ใน torchvision เพื่อแปลง tensor เป็นรูปภาพ
    transform = T.ToPILImage()

    # ถ้า tensor มี batch dimension (batch_size > 1) ให้ใช้ลูปเพื่อแปลงและแสดงรูปภาพแต่ละรายการใน batch
    if len(tensor.shape) == 4:
        images = [transform(t) for t in tensor]
    # ถ้า tensor ไม่มี batch dimension (batch_size=1) ให้แปลงและคืนเป็นรูปภาพเดียวในรูปแบบของ list ที่มีรายการเดียว
    else:
        images = [transform(tensor.squeeze(0))]
    
    return images