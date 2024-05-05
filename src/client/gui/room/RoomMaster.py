import tkinter as tk
from tkinter import messagebox

def kick_player():
    if player_role.get() == "Chủ phòng":
        messagebox.showinfo("Thông báo", "Người chơi đã bị đá!")
    else:
        messagebox.showinfo("Thông báo", "Bạn không có quyền đá người chơi!")

window = tk.Tk()
window.title("Room Detail")

player_name = "Người chơi"
player_role = "Chủ phòng"

canvas_width = 400
canvas_height = 350

canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
canvas.pack()

square_size = 200
square1_x = (canvas_width - square_size) // 2
square1_y = (canvas_height - square_size) // 2

square2_x = (canvas_width - square_size) // 2
square2_y = (canvas_height + square_size + 50) // 2

canvas.create_rectangle(square1_x, square1_y, square1_x + square_size, square1_y + square_size, fill="blue")
canvas.create_rectangle(square2_x, square2_y, square2_x + square_size, square2_y + square_size, fill="green")

player_name_label = tk.Label(window, text=player_name, font=("Arial", 20, "bold"))
player_name_label.place(relx=0.5, rely=0.5 - square_size / canvas_height, anchor=tk.CENTER)

player_role_label = tk.Label(window, text=player_role, font=("Arial", 14))
player_role_label.place(relx=0.5, rely=0.5 + square_size / canvas_height, anchor=tk.CENTER)

kick_button = tk.Button(window, text="Kick Player", command=kick_player)
kick_button.place(relx=0.5, rely=0.5 + (2 * square_size + 50) / canvas_height, anchor=tk.CENTER)

window.mainloop()