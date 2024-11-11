import sys
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk  # Szükséges a képek kezeléséhez
from customtkinter import CTkImage



class GUI:
    def __init__(self, game_instance, event_queue):


        self.game_instance = game_instance

        self.event_queue = event_queue
        self.selected_button = None
        self.app = customtkinter.CTk()
        self.app.geometry("1280x800")
        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.big_button_width = int(self.screen_width * 0.3)  # 30%-os szélesség
        self.big_button_height = int(self.screen_height * 0.1)  # 10%-os magasság
        self.app.bind("<Configure>", self.resize_button())  # Az ablak méretének változásakor újraméretezi a gombot
        self.app.title("Malom - Továbbfejlesztett Verzió")
        self.game_mode = customtkinter.StringVar(value="pvp")
        self.difficulty = customtkinter.StringVar(value="easy")
        self.aitype = customtkinter.StringVar(value="greedy")
        self.log_game = customtkinter.BooleanVar(value=False)

        # Beállítások
        self.theme_var = tk.StringVar(value="Alapértelmezett")
        self.appearance_mode = tk.StringVar(value="dark")


        # color paletta:

        self.primary_color = "#635985"
        self.secondary_color = "#443C68"
        self.harmadlagos_color = "#393053"
        self.negyedleges_color = "#18122B"

        #Indítás
        self.load_images()
        self.start_gui()



    def load_images(self):
        # Kör alakú képek betöltése
        self.white_circle_img = ImageTk.PhotoImage(Image.open("img/white_circle.png").resize((60, 60)))
        self.black_circle_img = ImageTk.PhotoImage(Image.open("img/black_circle.png").resize((60, 60)))
        self.empty_circle_img = ImageTk.PhotoImage(Image.open("img/empty_circle.png").resize((60, 60)))
        self.transparent_bg_img = ImageTk.PhotoImage(Image.open("img/transparent_bg.png"))  # Betöltjük a háttérképet
        self.logo_img = CTkImage(light_image=Image.open("img/malom.png"), size=(200, 200))

    def start_gui(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.show_main_menu()
        self.app.mainloop()

    def resize_button(self):
        # Gomb mérete az ablakhoz viszonyítva (szélesség és magasság százalékban)
        self.big_button_width = int(self.screen_width * 0.2)  # 30%-os szélesség
        self.big_button_height = int(self.screen_height * 0.07)  # 10%-os magasság


    def show_main_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        title_label = customtkinter.CTkLabel(self.app, text="Malom - by FreeKredit", font=("Helvetica", int(self.screen_width/30), "bold"))
        title_label.pack(pady=30)
        # Kép megjelenítése a főablakban
        logo_label = customtkinter.CTkLabel(self.app, image=self.logo_img,
                                            text="")  # text="" eltünteti a szöveget, ha nincs szükség rá
        logo_label.pack(pady=20)

        start_button = customtkinter.CTkButton(self.app, text="Játék indítása", command=self.show_game_settings_menu, width=self.big_button_width,
                                               height=self.big_button_height, corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        start_button.pack(pady=20)

        settings_button = customtkinter.CTkButton(self.app, text="Beállítások", command=self.show_settings_menu, width=self.big_button_width, height=self.big_button_height,
                                                  corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        settings_button.pack(pady=20)

        exit_button = customtkinter.CTkButton(self.app, text="Kilépés", command=lambda: self.sendEvent("exitApp"), width=self.big_button_width, height=self.big_button_height,
                                              corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        exit_button.pack(pady=20)

    def show_settings_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.menu_fix_header()

        settings_label = customtkinter.CTkLabel(self.app, text="Beállítások", font=("Helvetica", int(self.screen_width/55), "bold"))
        settings_label.pack(pady=30)

        # Dark/Light mód beállítása
        mode_label = customtkinter.CTkLabel(self.app, text="Megjelenés mód:")
        mode_label.pack(pady=10)

        # Változó létrehozása a megjelenés mód tárolásához


        # Dark mód rádiógomb
        dark_mode_radio = customtkinter.CTkRadioButton(self.app, text="Dark mód", variable=self.appearance_mode,
                                                       value="dark", command=self.update_appearance)
        dark_mode_radio.pack(pady=5)

        # Light mód rádiógomb
        light_mode_radio = customtkinter.CTkRadioButton(self.app, text="Light mód", variable=self.appearance_mode,
                                                        value="light", command=self.update_appearance)
        light_mode_radio.pack(pady=5)

        # Téma beállítása
        theme_label = customtkinter.CTkLabel(self.app, text="Játék téma:")
        theme_label.pack(pady=10)

        # Téma legördülő menü

        theme_dropdown = customtkinter.CTkComboBox(
            self.app,
            values=["Alapértelmezett", "Klasszikus", "Naplemente", "Tenger"],
            variable=self.theme_var,
            command=lambda _: self.update_theme()  # itt egy név nélküli "_" változóval fogadjuk az extra argumentumot
        )
        theme_dropdown.pack(pady=5)

        # Vissza gomb a főmenübe való visszatéréshez
        back_button = customtkinter.CTkButton(self.app, text="Vissza", command=self.show_main_menu, width=200, corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        back_button.pack(pady=(30, 10))
    
    def menu_fix_header(self):
        ###
        title_label = customtkinter.CTkLabel(self.app, text="Malom - by FreeKredit", font=("Helvetica", int(self.screen_width/30), "bold"))
        title_label.pack(pady=30)
        # Kép megjelenítése a főablakban
        logo_label = customtkinter.CTkLabel(self.app, image=self.logo_img,
                                            text="")  # text="" eltünteti a szöveget, ha nincs szükség rá
        logo_label.pack(pady=20)
        ###
    def update_appearance(self):
        # Az aktuális megjelenés mód beállítása a kiválasztott érték alapján
        mode = self.appearance_mode.get()
        customtkinter.set_appearance_mode(mode)  # "dark" vagy "light"

    def update_theme(self):
        # A kiválasztott téma alapján módosítja a színeket
        selected_theme = self.theme_var.get()

        if selected_theme == "Alapértelmezett":  # Alapértelmezett
            self.primary_color = "#635985"
            self.secondary_color = "#443C68"
            self.harmadlagos_color = "#393053"
            self.negyedleges_color = "#18122B"
        elif selected_theme == "Klasszikus":
            self.primary_color = "#352F44"
            self.secondary_color = "#5C5470"
            self.harmadlagos_color = "#B9B4C7"
            self.negyedleges_color = "#FAF0E6"
        elif selected_theme == "Naplemente":
            self.primary_color = "#FF204E"
            self.secondary_color = "#A0153E"
            self.harmadlagos_color = "#5D0E41"
            self.negyedleges_color = "#00224D"
        elif selected_theme == "Tenger":
            self.primary_color = "#27374D"
            self.secondary_color = "#526D82"
            self.harmadlagos_color = "#9DB2BF"
            self.negyedleges_color = "#DDE6ED"


        # Az új színeket alkalmazzuk a felületen, ha szükséges

    def show_game_settings_menu(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        #self.menu_fix_header()
        settings_label = customtkinter.CTkLabel(self.app, text="Új játék", font=("Helvetica", int(self.screen_width/55), "bold"))
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

        back_button = customtkinter.CTkButton(self.app, text="Vissza", command=self.show_main_menu, width=200, corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        back_button.pack(pady=(30, 10))

        start_button = customtkinter.CTkButton(self.app, text="Játék indítása", command=self.start_game, width=200,
                                               height=40, corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        start_button.pack(pady=20)

    def start_game(self):
        self.game_instance.reset_game_gui()
        self.game_instance.start_game_gui(self.game_mode.get(), self.difficulty.get())
        self.print_board_gui()

    def exit_app(self):
        self.app.quit()
        sys.exit()

    def print_board_gui(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        # Megnövelt háttérszín a főkerethez és középre igazítjuk a darabokat
        self.piece_frame = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.piece_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        self.update_piece_count()

        self.step_list = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.step_list.grid(row=0, column=2, padx=(20, 0), pady=10, sticky="ns")
        self.update_step_list()

        self.footer = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.footer.grid(row=1, column=0, padx=(20, 0), pady=10, sticky="ns")
        self.update_footer()
        # Játéktábla nagyobb méretben és középre igazítva
        canvas_size = self.screen_width-300  # Növeljük a vászon méretét
        canvas = tk.Canvas(self.app, width=canvas_size, height=canvas_size, bg="#2B2B2B", highlightthickness=0)
        canvas.grid(row=0, column=1, padx=20, pady=20, rowspan=2, sticky="n")  # Középre helyezve a grid beállításaival

        # Új koordináták a nagyobb vászonhoz, hogy középre igazítsuk a darabokat
        points = [
            (150, 150), (canvas_size // 2, 150), (canvas_size - 150, 150),
            (250, 250), (canvas_size // 2, 250), (canvas_size - 250, 250),
            (350, 350), (canvas_size // 2, 350), (canvas_size - 350, 350),
            (150, canvas_size // 2), (250, canvas_size // 2), (350, canvas_size // 2),
            (canvas_size - 350, canvas_size // 2), (canvas_size - 250, canvas_size // 2),
            (canvas_size - 150, canvas_size // 2),
            (350, canvas_size - 350), (canvas_size // 2, canvas_size - 350), (canvas_size - 350, canvas_size - 350),
            (250, canvas_size - 250), (canvas_size // 2, canvas_size - 250), (canvas_size - 250, canvas_size - 250),
            (150, canvas_size - 150), (canvas_size // 2, canvas_size - 150), (canvas_size - 150, canvas_size - 150)
        ]

        # Növelt méretű vonalak a középre helyezett játékmezőhöz
        lines = [
            (150, 150, canvas_size - 150, 150), (150, 150, 150, canvas_size - 150),
            (canvas_size - 150, 150, canvas_size - 150, canvas_size - 150),
            (150, canvas_size - 150, canvas_size - 150, canvas_size - 150),
            (250, 250, canvas_size - 250, 250), (250, 250, 250, canvas_size - 250),
            (canvas_size - 250, 250, canvas_size - 250, canvas_size - 250),
            (250, canvas_size - 250, canvas_size - 250, canvas_size - 250),
            (350, 350, canvas_size - 350, 350), (350, 350, 350, canvas_size - 350),
            (canvas_size - 350, 350, canvas_size - 350, canvas_size - 350),
            (350, canvas_size - 350, canvas_size - 350, canvas_size - 350),
            (150, canvas_size // 2, 350, canvas_size // 2),
            (canvas_size - 350, canvas_size // 2, canvas_size - 150, canvas_size // 2),
            (canvas_size // 2, 150, canvas_size // 2, 350),
            (canvas_size // 2, canvas_size - 350, canvas_size // 2, canvas_size - 150)
        ]

        for x1, y1, x2, y2 in lines:
            canvas.create_line(x1, y1, x2, y2, fill="white", width=4)

        # Kör alakú gombok nagyobb vászonra igazítva
        self.buttons = []
        for i, (x, y) in enumerate(points):
            piece_char = self.game_instance.board[i]
            image = self.white_circle_img if piece_char == 'W' else self.black_circle_img if piece_char == 'B' else self.empty_circle_img

            button = tk.Button(canvas, image=self.transparent_bg_img, command=lambda i=i: self.place_disc(i),
                               borderwidth=0, highlightthickness=0, bg="#2B2B2B")
            button.place(x=x - 30, y=y - 30)  # Igazítás a kör alakú képekhez
            button.image = image  # Referencia megtartása
            button.config(image=image, compound="center")

            self.buttons.append(button)


        # Gomb a főmenübe való visszatéréshez, középre igazítva
        back_button = customtkinter.CTkButton(self.app, text="Játék befejezése", command=self.back_to_menu, width=250,  corner_radius=20, fg_color=self.primary_color, hover_color=self.secondary_color)
        back_button.grid(row=2, column=1, pady=30, sticky="n")

    def update_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()
        self.footer = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.footer.grid(row=1, column=1, padx=(20, 0), pady=20, sticky="ns")

        label = tk.Label(self.footer,
                         text=self.game_instance.footer_text,
                         font=("Helvetica", int(self.screen_width/45)), bg="#2B2B2B", fg=self.PlayerNameColor1)
        label.pack(pady=5, anchor='w')  # Balra igazítás

    def update_button(self, index):
        piece_char = self.game_instance.board[index]
        image = self.white_circle_img if piece_char == 'W' else self.black_circle_img if piece_char == 'B' else self.empty_circle_img
        self.buttons[index].config(image=image)

    def update_step_list(self):
        for widget in self.step_list.winfo_children():
            widget.destroy()

        self.step_list = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.step_list.grid(row=0, column=2, padx=(20, 0), pady=10, sticky="ns")

        label = tk.Label(self.step_list,
                         text="Legutóbbi lépések",
                         font=("Helvetica", int(self.screen_width/40)),
                         bg=self.primary_color,
                         fg="white")
        label.pack(pady=5, anchor='w')  # Balra igazítás
        # Kiválasztjuk a step_list utolsó 10 elemét
        last_steps = self.game_instance.event_list[-15:]

        # Iterálunk a kiválasztott elemek felett, és minden elemet kiírunk egy új Label widgetre
        for step in last_steps:
            label = tk.Label(self.step_list,
                             text=step,
                             font=("Helvetica", int(self.screen_width/45)),
                             bg=self.negyedleges_color,
                             fg="white")
            label.pack(pady=5, anchor='w')  # Balra igazítás

    def update_piece_count(self):
        for widget in self.piece_frame.winfo_children():
            widget.destroy()

        # Frissített keret háttérszíne szürkére
        self.piece_frame = tk.Frame(self.app, bg="#3C3C3C")  # Keret háttere szürke
        self.piece_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="ns")

        if self.game_instance.turn_player1:
            self.player1_prefix = ""
            self.player2_prefix = ""
            self.PlayerNameColor1 = "white"
            self.PlayerNameColor2 = self.negyedleges_color
        else:
            self.player1_prefix = ""
            self.player2_prefix = ""
            self.PlayerNameColor1 = self.negyedleges_color
            self.PlayerNameColor2 = "white"


        # Számlálók létrehozása
        white_label = tk.Label(self.piece_frame, text=self.player1_prefix + self.game_instance.player1.name + " - fehér", font=("Helvetica", int(self.screen_width/40)), bg="#3C3C3C", fg=self.PlayerNameColor1)
        white_label.pack(pady=5, anchor='w')  # Jobbra igazítás

        # Fehér korongok hozzáadása
        white_piece = tk.Label(self.piece_frame, text="⚫" * (9 - self.game_instance.pieces_placed_player1), font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
        white_piece.pack(side=tk.TOP, anchor='w', padx=(0, 10))  # Jobbra igazítás
        white_piece = tk.Label(self.piece_frame, text=" "* (self.game_instance.pieces_placed_player1), font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
        white_piece.pack(side=tk.TOP, anchor='w', padx=(0, 10))  # Jobbra igazítás
        #for _ in range(9 - self.game_instance.pieces_placed_player1):
        #    white_piece = tk.Label(self.piece_frame, text="⚫", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
        #    white_piece.pack(side=tk.TOP, anchor='c', padx=(0, 10))  # Jobbra igazítás
        #for _ in range(self.game_instance.pieces_placed_player1):
        #    white_piece = tk.Label(self.piece_frame, text=" ", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
        #    white_piece.pack(side=tk.TOP, anchor='c', padx=(0, 10))  # Jobbra igazítás

        for _ in range(2):
            space = tk.Label(self.piece_frame, text=" ", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
            space.pack(side=tk.TOP, anchor='w', padx=(0, 10))  # Jobbra igazítás
        # Vonal létrehozása a canvas segítségével
        canvas = tk.Canvas(self.piece_frame, width=300, height=5, bg="#3C3C3C", highlightthickness=0)
        canvas.pack(pady=10)

        # Vízszintes vonal rajzolása
        canvas.create_line(0, 2, 300, 2, fill="white", width=3)  # A vonal a canvas magasságának 2 pixeljével van eltolva
        for _ in range(2):
            space = tk.Label(self.piece_frame, text=" ", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
            space.pack(side=tk.TOP, anchor='w', padx=(0, 10))  # Jobbra igazítás
        black_label = tk.Label(self.piece_frame, text=self.player2_prefix + self.game_instance.player2.name + " - fekete", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C",
                               fg=self.PlayerNameColor2)
        black_label.pack(pady=5, anchor='w')  # Jobbra igazítás


        black_piece = tk.Label(self.piece_frame, text="⚪" * (9 - self.game_instance.pieces_placed_player2), font=("Helvetica", int(self.screen_width / 45)),
                               bg="#3C3C3C", fg="white")
        black_piece.pack(side=tk.TOP, anchor='w', padx=(0, 10))  # Jobbra igazítás
        black_piece = tk.Label(self.piece_frame, text=" " * (self.game_instance.pieces_placed_player2), font=("Helvetica", int(self.screen_width / 45)),
                                bg="#3C3C3C", fg="white")
        black_piece.pack(side=tk.TOP, anchor='w', padx=(0, 10))  # Jobbra igazítás
        # Fekete korongok hozzáadása
        '''
        for _ in range(9 - self.game_instance.pieces_placed_player2):
            black_piece = tk.Label(self.piece_frame, text="⚪", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
            black_piece.pack(side=tk.TOP, anchor='c', padx=(0, 10))  # Jobbra igazítás
        for _ in range(self.game_instance.pieces_placed_player2):
            black_piece = tk.Label(self.piece_frame, text=" ", font=("Helvetica", int(self.screen_width/45)), bg="#3C3C3C", fg="white")
            black_piece.pack(side=tk.TOP, anchor='c', padx=(0, 10))  # Jobbra igazítás
        '''

    def back_to_menu(self):
        self.show_main_menu()

    def place_disc(self, index):
        self.selected_button = index
        self.event_queue.put(index)
        self.update_button(index)
        self.update_piece_count()
        for i in range(len(self.game_instance.board)):
            self.update_button(i)
        self.update_step_list()
        self.update_footer()

    def sendEvent(self, event):
        self.event_queue.put(event)