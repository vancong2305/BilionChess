import random
import time
import tkinter as tk
from threading import Thread

class chatGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tin nhắn")

        # Khung chat
        self.chat_frame = tk.Frame(self.window, background="#f5f5f5", padx=5, pady=5)
        self.chat_frame.grid(row=0, column=0, sticky="nsew")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # Khung hiển thị tin nhắn
        self.msg_scrollbar = tk.Scrollbar(self.chat_frame)
        self.msg_list = tk.Text(self.chat_frame, height=20, width=60,
                                yscrollcommand=self.msg_scrollbar.set, wrap=tk.WORD)
        self.msg_scrollbar.config(command=self.msg_list.yview)
        self.msg_list.grid(row=0, column=0, sticky="nsew")
        self.msg_scrollbar.grid(row=0, column=1, sticky="ns")
        self.chat_frame.rowconfigure(0, weight=1)
        self.chat_frame.columnconfigure(0, weight=1)

        # Message tags & styles
        self.msg_list.tag_configure("user_message", justify=tk.RIGHT, background="lightblue")
        self.msg_list.tag_configure("other_message", justify=tk.LEFT, background="#f0f0f0")

        # Ô nhập tin nhắn (textarea, rộng toàn màn hình)
        self.entry_frame = tk.Frame(self.window)
        self.entry_var = tk.StringVar()
        self.entry = tk.Text(self.entry_frame, height=5, width=60, wrap=tk.WORD)
        self.entry.grid(row=0, column=0, sticky="nsew")
        self.entry_frame.grid(row=1, column=0, sticky="ew", pady=5)
        self.window.columnconfigure(0, weight=1)

        # Nút gửi tin nhắn (Dòng mới)
        self.send_btn = tk.Button(self.window,height=2, text="Gửi", command=self.send_msg)
        self.send_btn.grid(row=2, column=0, sticky="ew")

        # Biến lưu trữ trạng thái kết nối
        self.connected = False

        # Khởi tạo kết nối giả lập
        self.simulate_connection()

    def simulate_connection(self):
        self.connected = True

        # Tạo thread giả lập nhận tin nhắn từ người khác
        def receive_msg():
            while self.connected:
                msg = f"Người khác: {random.choice(['Hello', 'How are you?', 'What are you doing?'])}"
                self.msg_list.insert(tk.END, f"{msg}\n", "other_message")
                self.msg_list.see(tk.END)
                time.sleep(1)
        thread = Thread(target=receive_msg)
        thread.start()

    def send_msg(self):
        msg = self.entry.get("1.0", tk.END).strip()  # Lấy nội dung từ textarea
        self.entry.delete("1.0", tk.END)

        if msg:  # Chỉ gửi tin nhắn nếu không phải rỗng
            self.msg_list.insert(tk.END, f"Bạn: {msg}\n", "user_message")
            self.msg_list.see(tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = chatGUI()
    gui.run()
