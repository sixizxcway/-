#библиотеки для интерфейса
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор анимации")
        self.root.geometry("650x450")
        self.root.config(bg="#fc9afd")

        self.photo_path = None
        self.audio_path = None

        # Главный контейнер
        main_frame = tk.Frame(root, bg="#fc9afd")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Левая колонка (Фотография) ---
        left_frame = tk.Frame(main_frame, bg="#fc9afd")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Область предпросмотра фото
        self.photo_box = tk.Label(
            left_frame,
            text="*Выбранная фотография*",
            bg="#fcb8fd",
            fg="#666666",
            font=("Arial", 11),
            relief="flat"
        )
        self.photo_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Кнопка выбора файла фото
        btn_choose_photo = tk.Button(
            left_frame,
            text="*Выбор файла*",
            bg="#db1adb",
            fg="#333333",
            font=("Arial", 10),
            relief="flat",
            cursor="hand2",
            command=self.choose_photo
        )
        btn_choose_photo.pack(fill=tk.X, ipady=8)

        # --- Правая колонка (Текст и аудио) ---
        right_frame = tk.Frame(main_frame, bg="#fc9afd")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Верхняя панель справа: две кнопки (Самостоятельный ввод / Выбрать аудиофайл)
        top_right_panel = tk.Frame(right_frame, bg="#fc9afd")
        top_right_panel.pack(fill=tk.X, pady=(0, 10))

        btn_manual_input = tk.Button(
            top_right_panel,
            text="Самостоятельный\nввод",
            bg="#db1adb",
            fg="#333333",
            font=("Arial", 9),
            relief="flat"
        )
        btn_manual_input.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5), ipady=4)

        btn_choose_audio = tk.Button(
            top_right_panel,
            text="Выбор\nаудиофайл",
            bg="#db1adb",
            fg="#333333",
            font=("Arial", 9),
            relief="flat",
            command=self.choose_audio
        )
        btn_choose_audio.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0), ipady=4)

        # Поле для ввода текста
        self.text_input = tk.Text(
            right_frame,
            bg="#fcb8fd",
            fg="#666666",
            font=("Arial", 11),
            relief="flat",
            height=8,
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.text_input.insert("1.0", "Введите текст")
        # Удаляем плейсхолдер при клике
        self.text_input.bind("<FocusIn>", self.clear_placeholder)

        # Кнопка «Создать»
        btn_create = tk.Button(
            right_frame,
            text="Генерация",
            bg="#db1adb",
            fg="#333333",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.create_process
        )
        btn_create.pack(fill=tk.X, ipady=8)

    def choose_photo(self):
        file_path = filedialog.askopenfilename(
            title="Выберите фотографию",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.photo_path = file_path
            try:
                img=Image.open(file_path)
                self.photo_box.update_idletasks()
                box_width = self.photo_box.winfo_width() or 250
                box_height=self.photo_box.winfo_height() or 300
                img.thumbnail((box_width -20, box_height-20))
                self.img_tk=ImageTk.PhotoImage(img)
                self.photo_box.config(image=self.img_tk,text="")
            except Exception as e:
                messagebox.showerror("Ошибка")
           # self.photo_box.config(text=f"Файл выбран:\n{file_path.split('/')[-1]}", fg="black")

    def choose_audio(self):
        file_path = filedialog.askopenfilename(
            title="Выберите аудиофайл",
            filetypes=[("Audio files", "*.mp3 *.wav *.aac *.ogg")]
        )
        if file_path:
            self.audio_path = file_path
            messagebox.showinfo("Аудио", f"Выбран аудиофайл:\n{file_path.split('/')[-1]}")

    def clear_placeholder(self, event):
        if self.text_input.get("1.0", tk.END).strip() == "Введите текст":
            self.text_input.delete("1.0", tk.END)
            self.text_input.config(fg="black")

    def create_process(self):
        text_content = self.text_input.get("1.0", tk.END).strip()
        if text_content == "Введите текст":
            text_content = ""

        # Здесь можно прописать логику обработки данных
        messagebox.showinfo(
            "Готово",
            f"Фото: {'Выбрано' if self.photo_path else 'Не выбрано'}\n"
            f"Аудио: {'Выбрано' if self.audio_path else 'Не выбрано'}\n"
            f"Текст: {text_content if text_content else 'Пусто'}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()