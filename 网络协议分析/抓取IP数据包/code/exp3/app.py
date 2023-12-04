import tkinter as tk

def button_click():
    print("按钮被点击了！")

window = tk.Tk()
button = tk.Button(window, text="点击我", command=button_click)
button.pack()
window.mainloop()