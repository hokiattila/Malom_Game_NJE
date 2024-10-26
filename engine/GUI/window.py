import sys
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk  # Szükséges a képek kezeléséhez


class GUI:
    def __init__(self, game_instance, event_queue):
        self.event_queue = event_queue
        self.selected_button = None
        self.app = customtkinter.CTk()
        self.app.geometry("1280x800")
        self.app.title("Malom - Továbbfejlesztett Verzió")
        self.game_mode = customtkinter.StringVar(value="pvp")
        self.difficulty = customtkinter.StringVar(value="easy")
        self.aitype = customtkinter.StringVar(value="greedy")
        self.log_game = customtkinter.BooleanVar(value=False)
        self.game_instance = game_instance
        self.load_images()
        self.start_gui()

    def load_images(self):
        # Kör alakú képek betöltése
        self.white_circle_img = ImageTk.PhotoImage(Image.open("img/white_circle.png").resize((60, 60)))
        self.black_circle_img = ImageTk.PhotoImage(Image.open("img/black_circle.png").resize((60, 60)))
        self.empty_circle_img = ImageTk.PhotoImage(Image.open("img/empty_circle.png").resize((60, 60)))
        self.transparent_bg_img = ImageTk.PhotoImage(Image.open("img/transparent_bg.png"))  # Betöltjük a háttérképet

    def start_gui(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.show_main_menu()
        self.app.mainloop()

    def show_main_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        title_label = customtkinter.CTkLabel(self.app, text="Malom - Továbbfejlesztett", font=("Helvetica", 26, "bold"))
        title_label.pack(pady=30)

        start_button = customtkinter.CTkButton(self.app, text="Játék indítása", command=self.start_game, width=200,
                                               height=40)
        start_button.pack(pady=20)

        settings_button = customtkinter.CTkButton(self.app, text="Beállítások", command=self.show_settings_menu,
                                                  width=200, height=40)
        settings_button.pack(pady=20)

        exit_button = customtkinter.CTkButton(self.app, text="Kilépés", command=self.exit_app, width=200, height=40)
        exit_button.pack(pady=20)

    def show_settings_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        settings_label = customtkinter.CTkLabel(self.app, text="Beállítások", font=("Helvetica", 24, "bold"))
        settings_label.pack(pady=30)

        mode_label = customtkinter.CTkLabel(self.app, text="Játékmód kiválasztása:")
        mode_label.pack(pady=5)
        mode_dropdown = customtkinter.CTkComboBox(self.app, values=["pvp", "pvc", "cvc"], variable=self.game_mode,
                                                  width=200)
        mode_dropdown.pack(pady=(0, 20))

        difficulty_label = customtkinter.CTkLabel(self.app, text="Nehézségi szint kiválasztása:")
        difficulty_label.pack(pady=5)
        difficulty_dropdown = customtkinter.CTkComboBox(self.app, values=["easy", "medium", "hard"],
                                                        variable=self.difficulty, width=200)
        difficulty_dropdown.pack(pady=(0, 20))

        log_checkbox = customtkinter.CTkCheckBox(self.app, text="Logolás engedélyezése", variable=self.log_game)
        log_checkbox.pack(pady=10)

        back_button = customtkinter.CTkButton(self.app, text="Vissza", command=self.show_main_menu, width=200)
        back_button.pack(pady=(30, 10))

    def start_game(self):
        self.game_instance.start_game_gui(self.game_mode.get(), self.difficulty.get())
        self.print_board_gui()

    def exit_app(self):
        self.app.quit()
        sys.exit()

    def print_board_gui(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        # Háttérszín beállítása a főkerethez
        self.piece_frame = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.piece_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.update_piece_count()

        # Játéktábla
        canvas = tk.Canvas(self.app, width=800, height=800, bg="#2B2B2B", highlightthickness=0)
        canvas.grid(row=0, column=1, padx=20, pady=20)

        points = [
            (100, 100), (400, 100), (700, 100),
            (200, 200), (400, 200), (600, 200),
            (300, 300), (400, 300), (500, 300),
            (100, 400), (200, 400), (300, 400),
            (500, 400), (600, 400), (700, 400),
            (300, 500), (400, 500), (500, 500),
            (200, 600), (400, 600), (600, 600),
            (100, 700), (400, 700), (700, 700)
        ]

        lines = [
            (100, 100, 700, 100), (100, 100, 100, 700), (700, 100, 700, 700), (100, 700, 700, 700),
            (200, 200, 600, 200), (200, 200, 200, 600), (600, 200, 600, 600), (200, 600, 600, 600),
            (300, 300, 500, 300), (300, 300, 300, 500), (500, 300, 500, 500), (300, 500, 500, 500),
            (100, 400, 300, 400), (500, 400, 700, 400), (400, 100, 400, 300), (400, 500, 400, 700)
        ]

        for x1, y1, x2, y2 in lines:
            canvas.create_line(x1, y1, x2, y2, fill="white", width=3)

        # Kör alakú gombok létrehozása
        self.buttons = []
        for i, (x, y) in enumerate(points):
            piece_char = self.game_instance.board[i]
            image = self.white_circle_img if piece_char == 'W' else self.black_circle_img if piece_char == 'B' else self.empty_circle_img

            # Gomb létrehozása háttérképpel, háttérszín beállítva
            button = tk.Button(canvas, image=self.transparent_bg_img, command=lambda i=i: self.place_disc(i),
                               borderwidth=0, highlightthickness=0, bg="#2B2B2B")  # Háttérszín beállítása

            button.place(x=x - 30, y=y - 30)  # Igazítás a kör alakú képekhez

            # Kör alakú kép beállítása
            button.image = image  # Szükséges a referencia megtartásához
            button.config(image=image, compound="center")  # Az image középre igazítása

            self.buttons.append(button)

        back_button = customtkinter.CTkButton(self.app, text="Játék befejezése", command=self.back_to_menu, width=150)
        back_button.grid(row=1, column=1, pady=30)

    def update_button(self, index):
        piece_char = self.game_instance.board[index]
        image = self.white_circle_img if piece_char == 'W' else self.black_circle_img if piece_char == 'B' else self.empty_circle_img
        self.buttons[index].config(image=image)

    def update_piece_count(self):
        for widget in self.piece_frame.winfo_children():
            widget.destroy()

        # Frissített keret háttérszíne szürkére
        self.piece_frame = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.piece_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ns")

        # Számlálók létrehozása
        white_label = tk.Label(self.piece_frame, text="Játékos 1 (Fehér)", font=("Arial", 12), bg="#3C3C3C", fg="white")
        white_label.pack(pady=5, anchor='e')  # Jobbra igazítás

        # Fehér korongok hozzáadása
        for _ in range(9 - self.game_instance.pieces_placed_player1):
            white_piece = tk.Label(self.piece_frame, text="⚪", font=("Arial", 20), bg="#3C3C3C", fg="white")
            white_piece.pack(side=tk.TOP, anchor='e', padx=(0, 10))  # Jobbra igazítás
        for _ in range(self.game_instance.pieces_placed_player1):
            white_piece = tk.Label(self.piece_frame, text=" ", font=("Arial", 20), bg="#3C3C3C", fg="white")
            white_piece.pack(side=tk.TOP, anchor='e', padx=(0, 10))  # Jobbra igazítás

        black_label = tk.Label(self.piece_frame, text="Játékos 2 (Fekete)", font=("Arial", 12), bg="#3C3C3C",
                               fg="white")
        black_label.pack(pady=5, anchor='e')  # Jobbra igazítás

        # Fekete korongok hozzáadása
        for _ in range(9 - self.game_instance.pieces_placed_player2):
            black_piece = tk.Label(self.piece_frame, text="⚫", font=("Arial", 20), bg="#3C3C3C", fg="white")
            black_piece.pack(side=tk.TOP, anchor='e', padx=(0, 10))  # Jobbra igazítás
        for _ in range(self.game_instance.pieces_placed_player2):
            black_piece = tk.Label(self.piece_frame, text=" ", font=("Arial", 20), bg="#3C3C3C", fg="white")
            black_piece.pack(side=tk.TOP, anchor='e', padx=(0, 10))  # Jobbra igazítás

    def back_to_menu(self):
        self.show_main_menu()

    def place_disc(self, index):
        self.selected_button = index
        self.event_queue.put(index)
        self.update_button(index)
        self.update_piece_count()
        for i in range(len(self.game_instance.board)):
            self.update_button(i)

