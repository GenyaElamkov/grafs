import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from src.settings import setting


class Window(ttk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.help_label = ttk.Label(
            text="1. Нажмите на кнопку «Выбрать файл» и найдите ваш Excel файл.\n2. Прежде чем запускать обработку, убедитесь, что в файле нет пустых строк в верхней части.\n3. Когда все готово, нажмите кнопку «Запустить».")
        self.text_label = ttk.Label(text="Выберите файл")

        self.filepath = ""
        self.open_button = ttk.Button(text="Выбрать файл", command=self.open_file)
        self.setup_button = ttk.Button(text="Запустить", command=self.setup_script)

        self.setup_grid()

    def open_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath != "":
            self.text_label.config(text=self.filepath)
            return self.filepath

    def setup_script(self):
        if self.filepath != "":
            self.text_label.config(text=self.filepath)
            setting(self.filepath)
        else:
            self.text_label.config(text="Не выбран файл")

    def setup_grid(self):
        self.help_label.grid(column=0, row=0, columnspan=2, padx=10)
        self.text_label.grid(column=0, row=1, columnspan=2, padx=10)
        self.open_button.grid(column=0, row=2, sticky=tk.NSEW, padx=10, pady=10)
        self.setup_button.grid(column=1, row=2, sticky=tk.NSEW, padx=10, pady=10)


def main() -> None:
    root = tk.Tk()
    root.title("Grafs")
    # root.geometry("600x200")
    
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 200
    root.geometry(f'600x200+{w}+{h}')
    root.resizable(width=False, height=False) 
    
    root.grid_rowconfigure(index=0, weight=1)
    root.grid_columnconfigure(index=0, weight=1)
    root.grid_columnconfigure(index=1, weight=1)

    app = Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
