from PIL import ImageGrab, ImageEnhance
import tkinter as tk
import pytesseract
import webbrowser

def select_area():
    def on_mouse_drag(event):
        # Cập nhật tọa độ hình chữ nhật
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_mouse_release(event):
        # Lưu tọa độ vùng chọn
        global region
        region = (min(start_x, event.x), min(start_y, event.y), 
                  max(start_x, event.x), max(start_y, event.y))
        root.destroy()

    def on_mouse_press(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    # Tạo cửa sổ toàn màn hình
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)  # Làm cửa sổ trong suốt một phần
    root.bind("<Escape>", lambda e: root.destroy())  # Thoát bằng phím Esc

    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)

    # Vẽ hình chữ nhật vùng chọn
    start_x = start_y = 0
    rect = canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)

    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()

def translate_selected_area_with_tesseract(region):
    if region[0] == region[2] and region[1] == region[3]:
        full_url = f'https://translate.google.com/details?sl=auto&tl=vi&op=translate'
    else:
        # Chụp màn hình vùng được chọn
        screenshot = ImageGrab.grab(bbox=region)
        processed_image = ImageEnhance.Contrast(screenshot.convert('L')).enhance(2)

        # Nhận diện văn bản bằng Tesseract
        text = pytesseract.image_to_string(processed_image, lang='en+vie').replace(" ", "%20").replace("\n", "%20").replace("6", "G")
        print(text)

        full_url = f'https://translate.google.com/details?sl=auto&tl=vi&text={text}&op=translate'

    # Mở Google Dịch
    webbrowser.open(full_url)

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Thay tọa độ bằng vùng đã chọn
    region = None
    select_area()
    if region: translate_selected_area_with_tesseract(region)