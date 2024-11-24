import unittest
from unittest.mock import MagicMock
import tkinter as tk

import customtkinter
from PIL import Image, ImageTk
from customtkinter import CTkImage
from engine.GUI.window import GUI

class TestGUI(unittest.TestCase):

    def setUp(self):
        # Mocking the game instance and event queue
        self.mock_game_instance = MagicMock()
        self.mock_event_queue = MagicMock()

        # Creating a GUI instance with mocked dependencies
        self.gui = GUI(self.mock_game_instance, self.mock_event_queue)

    def test_initial_values(self):
        # Teszteljük, hogy az inicializáláskor a helyes alapértékek vannak beállítva
        self.assertEqual(self.gui.game_mode.get(), "pvp")
        self.assertEqual(self.gui.difficulty.get(), "easy")
        self.assertEqual(self.gui.aitype.get(), "greedy")
        self.assertFalse(self.gui.log_game.get())

    def test_load_images(self):
        # Teszteljük, hogy a képek betöltődnek
        self.gui.load_images()
        self.assertIsInstance(self.gui.white_circle_img, ImageTk.PhotoImage)
        self.assertIsInstance(self.gui.black_circle_img, ImageTk.PhotoImage)
        self.assertIsInstance(self.gui.empty_circle_img, ImageTk.PhotoImage)
        self.assertIsInstance(self.gui.transparent_bg_img, ImageTk.PhotoImage)
        self.assertIsInstance(self.gui.logo_img, CTkImage)

    def test_start_gui(self):
        # Teszteljük, hogy a GUI indítása elindítja a megfelelő ablakot
        # A Tkinter alkalmazás nem jelenik meg a tesztelés során, de az app inicializálás megtörténik
        self.gui.start_gui()
        self.assertIsInstance(self.gui.app, customtkinter.CTk)

    def test_update_appearance(self):
        # Teszteljük, hogy a megjelenési mód változása helyesen működik
        self.gui.update_appearance()
        customtkinter.set_appearance_mode.assert_called_with(self.gui.appearance_mode.get())

    def test_update_theme(self):
        # Teszteljük, hogy a téma frissítése működik a választott téma alapján
        self.gui.update_theme()
        self.assertEqual(self.gui.primary_color, "#635985")

    def test_show_game_settings_menu(self):
        # Teszteljük, hogy a játékmenü megjelenítésekor a widgetek megfelelően betöltődnek
        self.gui.show_game_settings_menu()
        self.assertTrue(self.gui.app.winfo_children())  # Ellenőrizzük, hogy a widgetek megjelentek

    def test_exit_app(self):
        # Teszteljük, hogy az exit_app metódus bezárja az alkalmazást
        with self.assertRaises(SystemExit):
            self.gui.exit_app()

if __name__ == "__main__":
    unittest.main()