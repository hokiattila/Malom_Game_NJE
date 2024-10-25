
import customtkinter


def start_gui(self: "Game"):
    # Alapbeállítások
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    # Fő alkalmazás ablak létrehozása
    app = customtkinter.CTk()
    app.geometry("720x480")
    app.title("Malom by FreeKredit")

    # Változók a beállítások menü elemeihez
    game_mode = customtkinter.StringVar(value="PvP")  # Alapértelmezett játékmód
    log_game = customtkinter.BooleanVar(value=False)  # Logolás alapértelmezetten kikapcsolva

    # Főmenü létrehozása
    def show_main_menu():
        # Töröljük a meglévő widgeteket
        for widget in app.winfo_children():
            widget.destroy()

        # Cím hozzáadása
        title_label = customtkinter.CTkLabel(app, text="Malom - Nine Men's Morris", font=("Arial", 24))
        title_label.pack(pady=20)

        # Gombok a főmenüben
        start_button = customtkinter.CTkButton(app, text="Start", command=start_game)
        start_button.pack(pady=10)

        settings_button = customtkinter.CTkButton(app, text="Beállítások", command=show_settings_menu)
        settings_button.pack(pady=10)

        exit_button = customtkinter.CTkButton(app, text="Kilépés", command=exit_app)
        exit_button.pack(pady=10)

    # Beállítások menü létrehozása
    def show_settings_menu():
        # Töröljük a meglévő widgeteket
        for widget in app.winfo_children():
            widget.destroy()

        # Cím a beállítások menüben
        settings_label = customtkinter.CTkLabel(app, text="Beállítások", font=("Arial", 24))
        settings_label.pack(pady=20)

        # Játékmód kiválasztása legördülő menüvel
        mode_label = customtkinter.CTkLabel(app, text="Válassz játékmódot:")
        mode_label.pack(pady=5)

        mode_dropdown = customtkinter.CTkComboBox(app, values=["PvP", "PvC", "CvC"], variable=game_mode)
        mode_dropdown.pack(pady=10)

        # Jelölőnégyzet a logoláshoz
        log_checkbox = customtkinter.CTkCheckBox(app, text="Logolás engedélyezése", variable=log_game)
        log_checkbox.pack(pady=10)

        # Vissza gomb a főmenübe
        back_button = customtkinter.CTkButton(app, text="Vissza", command=show_main_menu)
        back_button.pack(pady=20)

    # Funkciók a gombokhoz
    def start_game():
        # Játék elindítása (itt csak egy üzenet, de később kiegészíthető)
        print(
            f"Játék elindult, játékmód: {game_mode.get()}, logolás: {'bekapcsolva' if log_game.get() else 'kikapcsolva'}")

    def exit_app():
        app.quit()

    # Főmenü megjelenítése
    show_main_menu()

    # Alkalmazás indítása
    app.mainloop()