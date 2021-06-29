import tkinter as tk

def popupmsg(msg):
    LARGE_FONT= ("Verdana", 12)
    NORM_FONT = ("Helvetica", 10)
    SMALL_FONT = ("Helvetica", 8)
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=LARGE_FONT, width=60,height=10)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()