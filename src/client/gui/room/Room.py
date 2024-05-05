import tkinter as tk
from tkinter import messagebox

# Hàm xử lý sự kiện khi người dùng nhấp vào nút
def show_selected_item(index):
    item = list_items[index]
    messagebox.showinfo(item["title"], item["content"])

# Hàm xử lý sự kiện cuộn danh sách
def on_canvas_configure(event):
    list_canvas.config(scrollregion=list_canvas.bbox(tk.ALL))

# Hàm xử lý sự kiện khi người dùng nhấp vào nút "Tạo phòng"
def create_room():
    messagebox.showinfo("Thông báo", "Phòng đã được tạo!")

# Tạo cửa sổ
window = tk.Tk()
window.title("Danh sách phòng")

# Lấy kích thước màn hình
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Tính toán vị trí hiển thị để căn giữa cửa sổ
window_width = 500
window_height = 350
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Thiết lập kích thước và vị trí
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(False, False)  # Ngăn cửa sổ khỏi việc thay đổi kích thước

# Tạo label "xyz"
xyz_label = tk.Label(window, text="Xin chào: xyz", font=("Arial", 30))
xyz_label.pack()

# Tạo label "Đánh online"
create_room_button = tk.Button(window, text="Tạo phòng", font=("Arial", 14, "bold"), width=20)
create_room_button.pack()

# Tạo label "Đánh online"
create_room_button = tk.Button(window, text="Đấu với máy", font=("Arial", 14, "bold"), width=20)
create_room_button.pack()

# Tạo label "Đánh online"
create_room_button = tk.Button(window, text="Trở về", font=("Arial", 14, "bold"), width=20)
create_room_button.pack()

# Tạo label "Đánh online"
online_title_label = tk.Label(window, text="Danh sách phòng", font=("Arial", 14, "bold"))
online_title_label.pack()


# Tạo khung chứa danh sách
list_frame = tk.Frame(window)
list_frame.pack(fill=tk.BOTH, expand=True)

# Tạo thanh cuộn
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Tạo khung chứa danh sách bên trong frame
list_canvas = tk.Canvas(list_frame, yscrollcommand=scrollbar.set, width=400)
list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Kết nối thanh cuộn với canvas
scrollbar.config(command=list_canvas.yview)

# Tạo khung chứa danh sách
items_frame = tk.Frame(list_canvas)
list_canvas.create_window((0, 0), window=items_frame, anchor=tk.NW)

# Danh sách các mục
list_items = [
    {
        "title": "Phòng số 1",
        "content": "Số người: 1/2"
    },
    {
        "title": "Phòng số 2",
        "content": "Số người: 1/2"
    },
    {
        "title": "Phòng số 3",
        "content": "Số người: 1/2"
    }
]

# Hiển thị danh sách và nút
for index, item in enumerate(list_items):
    # Tạo khung gom nhóm
    item_frame = tk.Frame(items_frame, borderwidth=1, relief=tk.SOLID)
    item_frame.pack(pady=5)

    # Hiển thị Phòng số và nội dung
    title_label = tk.Label(item_frame, text=item["title"], font=("Arial", 12, "bold"), width=40, anchor=tk.W)
    title_label.grid(row=0, column=0, sticky=tk.W)

    content_label = tk.Label(item_frame, text=item["content"], width=40, anchor=tk.W)
    content_label.grid(row=1, column=0, sticky=tk.W)

    # Tạo nút bấm
    button = tk.Button(item_frame, text="Vào", command=lambda idx=index: show_selected_item(idx), width=5, anchor=tk.CENTER, bg="black", fg="white")
    button.grid(row=0, column=1, rowspan=2, padx=10, pady=10)  # Điều chỉnh khoảng cách giữa cột và hàng

# Thiết lập kích thước của khung danh sách
items_frame.update_idletasks()
list_canvas.config(scrollregion=list_canvas.bbox(tk.ALL))


# Thiết lập sự kiện khi cuộn danh sách
list_canvas.bind("<Configure>", on_canvas_configure)

# Chạy ứng dụng
window.mainloop()