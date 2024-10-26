import sys
import time
import tkinter as tk
import customtkinter

import customtkinter  # Győződj meg arról, hogy importálva van a customtkinter
import tkinter as tk


class GUI:
    # Változók a beállítások menü elemeihez

    def __init__(self, game_instance, event_queue):
        self.event_queue = event_queue
        self.selected_button = None
        self.app = customtkinter.CTk()
        self.app.geometry("1280x720")
        self.app.title("Malom by FreeKredit")
        self.game_mode = customtkinter.StringVar(value="pvp")  # Alapértelmezett játékmód
        self.difficulty = customtkinter.StringVar(value="easy")  # Alapértelmezett játékmód
        self.aitype = customtkinter.StringVar(value="greedy")
        self.log_game = customtkinter.BooleanVar(value=False)  # Logolás alapértelmezetten kikapcsolva
        self.game_instance = game_instance
        self.start_gui()  # GUI indítása

    def start_gui(self):
        # Alapbeállítások
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        # Főmenü megjelenítése
        self.show_main_menu()

        # Alkalmazás indítása
        self.app.mainloop()

    # Főmenü létrehozása
    def show_main_menu(self):
        # Töröljük a meglévő widgeteket
        for widget in self.app.winfo_children():
            widget.destroy()

        # Cím hozzáadása
        title_label = customtkinter.CTkLabel(self.app, text="Malom - by FreeKredit", font=("Arial", 24))
        title_label.pack(pady=20)

        # Gombok a főmenüben
        start_button = customtkinter.CTkButton(self.app, text="Start", command=self.start_game)
        start_button.pack(pady=10)

        settings_button = customtkinter.CTkButton(self.app, text="Beállítások", command=self.show_settings_menu)
        settings_button.pack(pady=10)

        exit_button = customtkinter.CTkButton(self.app, text="Kilépés", command=self.exit_app)
        exit_button.pack(pady=10)

    # Beállítások menü létrehozása
    def show_settings_menu(self):
        # Töröljük a meglévő widgeteket
        for widget in self.app.winfo_children():
            widget.destroy()

        # Cím a beállítások menüben
        settings_label = customtkinter.CTkLabel(self.app, text="Beállítások", font=("Arial", 24))
        settings_label.pack(pady=(20, 10))  # Felső margó, alsó margó

        # Játékmód kiválasztása legördülő menüvel
        mode_label = customtkinter.CTkLabel(self.app, text="Válassz játékmódot:")
        mode_label.pack(pady=(10, 5))  # Felső margó, alsó margó

        mode_dropdown = customtkinter.CTkComboBox(self.app, values=["pvp", "pvc", "cvc"], variable=self.game_mode)
        mode_dropdown.pack(pady=(0, 15))  # Felső margó, alsó margó


        # Nehézség kiválasztása legördülő menüvel
        difficulty_label = customtkinter.CTkLabel(self.app, text="Válassz nehézséget:")
        difficulty_label.pack(pady=(10, 5))  # Felső margó, alsó margó

        difficulty_dropdown = customtkinter.CTkComboBox(self.app, values=["easy", "medium", "hard"],
                                                        variable=self.difficulty)
        difficulty_dropdown.pack(pady=(0, 15))  # Felső margó, alsó margó

        # Jelölőnégyzet a logoláshoz
        log_checkbox = customtkinter.CTkCheckBox(self.app, text="Logolás engedélyezése", variable=self.log_game)
        log_checkbox.pack(pady=(10, 5))  # Felső margó, alsó margó

        # Vissza gomb a főmenübe
        back_button = customtkinter.CTkButton(self.app, text="Vissza", command=self.show_main_menu)
        back_button.pack(pady=(20, 10))  # Felső margó, alsó margó

    # Játék indítása
    def start_game(self):
        self.game_instance.start_game_gui(self.game_mode.get(), self.difficulty.get())
        self.print_board_gui()
        print(
            f"Játék elindult, játékmód: {self.game_mode.get()}, logolás: {'bekapcsolva' if self.log_game.get() else 'kikapcsolva'}")
        #self.app.quit()
    # Alkalmazás bezárása
    def exit_app(self):
        self.app.quit()
        sys.exit() # Ideiglenes, nem ajánlott ezzel kilépni, majd a main.py while-ba kellene beépíteni.

    # Játéktábla kirajzolása
    def print_board_gui(self):
        for widget in self.app.winfo_children():
            widget.destroy()

            # Bal oldali szekció a korongoknak
        self.piece_frame = tk.Frame(self.app, width=100, height=600, bg="lightgrey")
        self.piece_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Korongok frissítése
        self.update_piece_count()  # Frissítjük a korongok számát

        # Játéktábla szekció
        canvas = tk.Canvas(self.app, width=1200, height=1200, bg="grey")
        canvas.grid(row=0, column=1, padx=20, pady=10)

        mezo = -1
        #self.game_instance = actual_game_instance


        # Játéktábla szekció
        canvas = tk.Canvas(self.app, width=1200, height=1200, bg="grey")
        canvas.grid(row=0, column=1, padx=20, pady=10)

        # Tábla központi pontjainak koordinátái
        points = [
            (150, 150), (600, 150), (1050, 150),
            (300, 300), (600, 300), (900, 300),
            (450, 450), (600, 450), (750, 450),
            (150, 600), (300, 600), (450, 600),
            (750, 600), (900, 600), (1050, 600),
            (450, 750), (600, 750), (750, 750),
            (300, 900), (600, 900), (900, 900),
            (150, 1050), (600, 1050), (1050, 1050)
        ]

        # Tábla vonalainak koordinátái
        lines = [
            (150, 150, 1050, 150), (150, 150, 150, 1050),
            (1050, 150, 1050, 1050), (150, 1050, 1050, 1050),
            (300, 300, 900, 300), (300, 300, 300, 900),
            (900, 300, 900, 900), (300, 900, 900, 900),
            (450, 450, 750, 450), (450, 450, 450, 750),
            (750, 450, 750, 750), (450, 750, 750, 750),
            (150, 600, 450, 600), (750, 600, 1050, 600),
            (600, 150, 600, 450), (600, 750, 600, 1050)
        ]

        # Tábla vonalainak kirajzolása
        for x1, y1, x2, y2 in lines:
            canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

        # Gombok a tábla mezőihez
        buttons = []
        for i, (x, y) in enumerate(points):
            piece_char = self.game_instance.board[i]  # board i. eleme
            if piece_char == 'W':
                button = tk.Button(canvas, text="⚪", width=5, height=3, command=lambda i=i: self.place_disc(i),
                                   bg="white")
            elif piece_char == 'B':
                button = tk.Button(canvas, text="⚫", width=5, height=3, command=lambda i=i: self.place_disc(i),
                                   bg="black")
            else:
                button = tk.Button(canvas, text=f"{i}", width=5, height=3, command=lambda i=i: self.place_disc(i),
                                   bg="lightgrey")

            button.place(x=x - 20, y=y - 20)
            buttons.append(button)

        # Mentjük a gombokat a mezők későbbi eléréséhez
        self.buttons = buttons

        # Visszatérő gomb a főmenübe
        back_button = customtkinter.CTkButton(self.app, text="Játék befejezése", command=self.back_to_menu)
        back_button.grid(row=1, column=1, pady=20)

    def update_button(self, index):
        # A megfelelő gomb frissítése az index alapján
        piece_char = self.game_instance.board[index]  # board i. eleme
        button = self.buttons[index]  # Hozzáférés a megfelelő gombhoz

        if piece_char == 'W':
            button.config(text="⚪", bg="white")  # Fehér korong
        elif piece_char == 'B':
            button.config(text="⚫", bg="black")  # Fekete korong
        else:
            button.config(text=f"{index}", bg="lightgrey")  # Üres mező

    def update_piece_count(self):
        # Töröljük a régieket a korongok szekcióban
        for widget in self.piece_frame.winfo_children():
            widget.destroy()

        # Létrehozzuk a keretet a korongok számára
        white_frame = tk.Frame(self.piece_frame, bg="lightgrey")
        white_frame.pack(side=tk.LEFT, padx=(0, 10))  # Fehér korongok kerete

        black_frame = tk.Frame(self.piece_frame, bg="lightgrey")
        black_frame.pack(side=tk.LEFT)  # Fekete korongok kerete

        # Fehér korongok oszlopa
        white_label = tk.Label(white_frame, text="Játékos 1 korongjai", font=("Arial", 12), bg="lightgrey")
        white_label.pack(pady=5)

        for _ in range(9 - self.game_instance.pieces_placed_player1):
            white_piece = tk.Label(white_frame, text="⚪", font=("Arial", 16), bg="lightgrey")
            white_piece.pack()

        # Fekete korongok oszlopa
        black_label = tk.Label(black_frame, text="Játékos 2 korongjai", font=("Arial", 12), bg="lightgrey")
        black_label.pack(pady=5)

        for _ in range(9 - self.game_instance.pieces_placed_player2):
            black_piece = tk.Label(black_frame, text="⚫", font=("Arial", 16), bg="lightgrey")
            black_piece.pack()

    # Vissza a főmenübe
    def back_to_menu(self):
        self.show_main_menu()

    # Példa a `place_disc` függvényre, amit a gombok `command`-ként használnak
    def place_disc(self, index):
        self.selected_button = index
        self.event_queue.put(index)
        self.update_button(index)
        self.update_piece_count()  # Frissítjük a korongok számát
        for i in range(len(self.game_instance.board)):
            self.update_button(i)
