import tkinter as tk

# Khởi tạo cửa sổ
window = tk.Tk()
window.geometry("1200x500")

# Khung chứa các ô
frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

# Danh sách các ô
cells = []

# List sử dụng
list_data = [1, 9, 17, 25, 33, 34, 35, 36, 37, 38, 39, 40, 32, 24, 16, 8, 7, 6, 5, 4, 3, 2]

# Tạo 40 ô
for i in range(40):
    cell = tk.Label(frame, borderwidth=2, font=("Arial", 12))
    cell.grid(row=i // 8, column=i % 8)  # Co giãn và bám sát các cạnh
    cells.append(cell)

# Cài đặt kích thước cột và hàng
for i in range(8):
    frame.columnconfigure(i, weight=1)
    frame.rowconfigure(i, weight=1)

# Cập nhật kích thước của frame
frame.update()

# Tính toán kích thước ô
height = frame.winfo_height()
width = frame.winfo_width()

# Duyệt và in ra chỉ số của list_data
for i, value in enumerate(list_data):
    print(f"Chỉ số: {i}, Giá trị: {value}")
    cells[value-1].configure(bg="red")
    cells[value-1].configure(text=str(i + 1))
    cells[value-1].configure(height=5, width=15)

# Chạy chương trình
window.mainloop()