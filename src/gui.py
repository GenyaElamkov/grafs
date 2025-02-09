import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from src.settings import setting


class Window(ttk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.help_label = ttk.Label(
            text="1. Нажмите кноку «Выбрать файл» — выберите файл — exel\n2. Нажмите кноку «Запустить»\n"
        )
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
        self.help_label.grid(column=0, row=0, padx=10)
        self.text_label.grid(column=0, row=1, padx=10)
        self.open_button.grid(column=0, row=2, sticky=tk.NSEW, padx=10)
        self.setup_button.grid(column=1, row=2, sticky=tk.NSEW, padx=10)


def main() -> None:
    root = tk.Tk()
    root.title("Grafs")
    root.geometry("600x200")
    root.grid_rowconfigure(index=0, weight=1)
    root.grid_columnconfigure(index=0, weight=1)
    root.grid_columnconfigure(index=1, weight=1)

    app = Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
