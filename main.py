import time
import threading
import queue

from engine.GUI.window import GUI
from engine.game import Game
import argparse
import sys
import customtkinter
from engine.GUI import window
import tkinter as tk

def close_all_threads():
    # Kilistázzuk az összes futó szálat
    for thread in threading.enumerate():
        # Megvizsgáljuk, hogy a szál nem a fő szál-e és még aktív
        if thread is not threading.main_thread() and thread.is_alive():
            print(f"Leállítás: {thread.name}")
            thread.join(timeout=1)  # Kísérlet a szál leállítására

    print("Minden nem fő szál leállt.")
def gui_thread(event_queue):
    # Inicializáljuk a GUI-t

    window = GUI(new_game, event_queue)
    # A GUI futtatása
    #root.mainloop()

def listen_for_events(event_queue):
    while True:
        # Várakozás az eseményekre (pl. gombnyomások)
        event = event_queue.get()
        if(event == "closeApp"):
            close_all_threads()
            print("Az alkalmazás leáll.")
            sys.exit()  # Az alkalmazás kilép
        if (event == "nextPlayer"):
            if new_game.turn_player1:
                new_game.player_move(new_game.player1, 1, lepes)  # Egyebkent player 1 lep
            else:
                new_game.player_move(new_game.player2, 2, lepes)  # Egyebkent player 2 lep
        return event

if __name__ == '__main__':  # Ha kozvetlenul futtajuk a fajlt
    parser = argparse.ArgumentParser(description='Malom Game NJE')  # Beallitjuk a kapcsolokat
    parser.add_argument('--debug', action='store_true', default=False, help='debug mode')   # Regisztraljuk a debug kapcsolot -> boolean, alapesetben false, konzolos megjelenitest biztosit
    parser.add_argument('--log', action='store_true', default=False, help='log gameplay')   # Regisztraljuk a log kapcsolot -> boolean, alapesetben false, log fajlok letrehozasat kezeli
    # Regisztraljuk a mode parametert, ami string tipus es pvp/pvc/cvc ertekeket vehet fel
    parser.add_argument('--mode', type=str, default='cvc', choices=['pvp','pvc','cvc'], help='Set the game mode (pvp = Player vs Player, pvc = Player vs Computer, cvc = Computer vs Computer')

    args, remaining_args = parser.parse_known_args()

    # Ha a --mode tartalmaz 'c'-t, akkor hozzáadjuk a --diff kapcsolót
    if args.mode == "pvc":
        parser.add_argument('--diff', type=str, default='easy', choices=['easy', 'medium', 'hard'], help='Set the difficulty level (easy, medium, hard)')
    elif args.mode == "cvc":
        parser.add_argument('--p1', type=str, default='greedy', choices=['greedy', 'ml', 'astar', 'random'], help='Set the computer player1')
        parser.add_argument('--p2', type=str, default='greedy', choices=['greedy', 'ml', 'astar', 'random'], help='Set the computer player2')


    # Az új parserrel feldolgozzuk a fennmaradó argumentumokat, és egyesítjük a kettőt
    args = parser.parse_args(remaining_args, namespace=args)


    difficulty = getattr(args, 'diff', None)
    p1 = getattr(args, 'p1', None)
    p2 = getattr(args, 'p2', None)

    if args.debug:  # A megjelenito fuggvenyek a mode kapcsolotol fuggnek
        new_game = Game(mode=args.mode, debug=args.debug, log=args.log, difficulty=difficulty, p1_flag=p1, p2_flag=p2)  # Letrehozunk egy uj Game peldanyt
        new_game.print_initials()  # Kiirjuk az alapadatokat konzolra (Debug mod)
        print_brd = new_game.print_board_debug  # Debug esetben
        print_res = new_game.print_result_debug # Debug esetben
        new_game = Game(mode=args.mode, debug=args.debug, log=args.log, difficulty=difficulty, p1_flag=p1,  p2_flag=p2)  # Letrehozunk egy uj Game peldanyt
        new_game.print_initials()  # Kiirjuk az alapadatokat konzolra (Debug mod)
        print_brd()  # Megjelenitjuk a tablat
    else:
        event_queue = queue.Queue()
        print_brd = lambda: print("Debug mode disabled")
        print_res = lambda: print("Debug mode disabled")
        new_game = Game(event_queue, mode=args.mode, debug=args.debug, log=args.log, difficulty=difficulty, p1_flag=p1,p2_flag=p2)  # Letrehozunk egy uj Game peldanyt
        new_game.print_initials()  # Kiirjuk az alapadatokat konzolra (Debug mod)
        #new_game.game_GUI = window.GUI(new_game, event_queue)
        # Elindítjuk a GUI szálat
        threading.Thread(target=gui_thread, args=(event_queue,), daemon=True).start()

    if args.log:
        new_game.log_game() # Ha kaptunk log kapcsolot akkor letrehozzuk a log fajlt




    #print_brd()
    while True: # Vegtelen ciklus
        if new_game.game_over(): # Ha a jatek veget er
            if args.debug:
                print_res() # Kiirjuk az eredmenyt
                break   # Kitorunk a ciklusbol
        if args.debug:
            if new_game.turn_player1:
                new_game.player_move(new_game.player1, 1)  # Egyebkent player 1 lep
            else:
                new_game.player_move(new_game.player2, 2)  # Egyebkent player 1 lep
        if not args.debug:
            lepes = listen_for_events(event_queue)
            if lepes == "closeApp":
                break
            if new_game.turn_player1:
                new_game.player_move(new_game.player1, 1, lepes)  # Egyebkent player 1 lep
            else:
                new_game.player_move(new_game.player2, 2, lepes)  # Egyebkent player 2 lep
        if args.log:
            new_game.log_game()