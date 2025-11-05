

#Fallow me on:
#https://T.me/AiHoma
#https://github.com/Aihoma
#https://medium.com/@AiHoma

import sys
import subprocess
import importlib

packages = ["qrcode", "Pillow", "arabic_reshaper", "python-bidi"]

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        install_package(pkg)

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import os
import platform
import arabic_reshaper
from bidi.algorithm import get_display

class QRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code ساز حرفه‌ای")
        self.root.geometry("520x650")
        self.root.resizable(False, False)
        self.language = "FA"
        self.texts = self.get_texts()
        self.data_var = tk.StringVar()
        self.brand_var = tk.StringVar()
        self.fill_color = "#000000"
        self.logo_path = ""
        self.font_path = self.get_default_farsi_font()
        self.font_size = 70
        self.create_widgets()

    def get_default_farsi_font(self):
        if platform.system() == "Windows":
            for path in [r"C:\Windows\Fonts\tahoma.ttf", r"C:\Windows\Fonts\arial.ttf"]:
                if os.path.isfile(path):
                    return path
        return None

    def get_texts(self):
        if self.language == "FA":
            return {
                "link": "لینک یا متن QR:",
                "brand": "نام برند:",
                "color": "انتخاب رنگ QR",
                "logo": "آپلود لوگو",
                "build": "ساخت QR Code",
                "select_lang": "انتخاب زبان",
                "success": "QR Code ساخته شد و ذخیره گردید.",
                "error": "هیچ داده‌ای وارد نشده است."
            }
        else:
            return {
                "link": "QR Link/Text:",
                "brand": "Brand Name:",
                "color": "Choose QR Color",
                "logo": "Upload Logo",
                "build": "Build QR Code",
                "select_lang": "Select Language",
                "success": "QR Code has been created and saved.",
                "error": "No QR data entered."
            }

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        self.label_lang = tk.Label(frame, text=self.texts["select_lang"], font=("Tahoma", 14, "bold"))
        self.label_lang.pack(pady=5)
        lang_frame = tk.Frame(frame)
        lang_frame.pack(pady=5)
        tk.Button(lang_frame, text="فارسی", font=("Tahoma", 12, "bold"), command=lambda: self.change_language("FA")).pack(side="left", padx=5)
        tk.Button(lang_frame, text="English", font=("Tahoma", 12, "bold"), command=lambda: self.change_language("EN")).pack(side="left", padx=5)
        self.label_link = tk.Label(frame, text=self.texts["link"], font=("Tahoma", 12, "bold"))
        self.label_link.pack(pady=5)
        self.entry_link = tk.Entry(frame, textvariable=self.data_var, width=40, font=("Tahoma", 12), justify="left")
        self.entry_link.pack(pady=5)
        self.label_brand = tk.Label(frame, text=self.texts["brand"], font=("Tahoma", 12, "bold"))
        self.label_brand.pack(pady=5)
        self.entry_brand = tk.Entry(frame, textvariable=self.brand_var, width=40, font=("Tahoma", 12))
        self.entry_brand.pack(pady=5)
        self.button_color = tk.Button(frame, text=self.texts["color"], font=("Tahoma", 12, "bold"), command=self.choose_color, width=20)
        self.button_color.pack(pady=5)
        self.button_logo = tk.Button(frame, text=self.texts["logo"], font=("Tahoma", 12, "bold"), command=self.choose_logo, width=20)
        self.button_logo.pack(pady=5)
        self.button_build = tk.Button(frame, text=self.texts["build"], font=("Tahoma", 14, "bold"), command=self.build_qr, width=25, bg="#4CAF50", fg="white")
        self.button_build.pack(pady=10)
        self.canvas = tk.Canvas(frame, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

    def change_language(self, lang):
        self.language = lang
        self.texts = self.get_texts()
        self.update_texts()

    def update_texts(self):
        self.label_lang.config(text=self.texts["select_lang"])
        self.label_link.config(text=self.texts["link"])
        self.label_brand.config(text=self.texts["brand"])
        self.button_color.config(text=self.texts["color"])
        self.button_logo.config(text=self.texts["logo"])
        self.button_build.config(text=self.texts["build"])

    def choose_color(self):
        color = colorchooser.askcolor(title=self.texts["color"])[1]
        if color:
            self.fill_color = color

    def choose_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.logo_path = path

    def build_qr(self):
        data = self.data_var.get()
        brand_name = self.brand_var.get()
        if not data:
            messagebox.showerror("Error", self.texts["error"])
            return
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=30,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fill_color, back_color="white").convert('RGB')
        img = img.resize((1000, 1000), Image.LANCZOS)
        img_w, img_h = img.size
        if self.logo_path:
            try:
                logo = Image.open(self.logo_path)
                logo.thumbnail((150, 150))
                logo_w, logo_h = logo.size
                pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)
                img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
            except Exception as e:
                print("⚠️ مشکل در بارگذاری لوگو:", e)
        if brand_name:
            reshaped_text = arabic_reshaper.reshape(brand_name)
            bidi_text = get_display(reshaped_text)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(self.font_path, self.font_size)
            except:
                font = ImageFont.load_default()
            text_bbox = draw.textbbox((0,0), bidi_text, font=font)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]
            margin = 5
            new_img = Image.new("RGB", (img_w, img_h + text_h + margin), "white")
            new_img.paste(img, (0, 0))
            draw = ImageDraw.Draw(new_img)
            text_y = img_h + (margin // 2)
            draw.text(((img_w - text_w) // 2, text_y), bidi_text, fill=self.fill_color, font=font)
            img = new_img
        preview_img = img.copy()
        preview_img.thumbnail((300, 300))
        self.qr_img = img
        self.tk_img = ImageTk.PhotoImage(preview_img)
        self.canvas.create_image(150, 150, image=self.tk_img)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(current_dir, "my_qr.png")
        img.save(save_path)
        messagebox.showinfo("Success", self.texts["success"] + f"\n{save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRApp(root)
    root.mainloop()
