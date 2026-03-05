import tkinter as tk
from tkinter import messagebox

def on_click(button_text):
    current_text = entry.get()
    if button_text == "=":
        try:
            result = eval(current_text) # Evaluates the math string
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception:
            messagebox.showerror("Error", "Invalid Input")
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)

# Initialize Window
root = tk.Tk()
root.title("Simple Calc")

# Entry Display
entry = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=5, relief="flat", justify='right')
entry.grid(row=0, column=0, columnspan=4)

# Button Layout
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row_val = 1
col_val = 0

for button in buttons:
    action = lambda x=button: on_click(x)
    tk.Button(root, text=button, width=5, height=2, font=('Arial', 14),
              command=action).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

root.mainloop()