from engine.game import Game
import argparse
import sys
import customtkinter



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


    #if not args.debug:  # Jelenleg csak debug modot tamogatunk
    #    sys.exit('At the moment only debug mode is supported')  # igy ha mas modban indul a program, leallitjuk

    difficulty = getattr(args, 'diff', None)
    p1 = getattr(args, 'p1', None)
    p2 = getattr(args, 'p2', None)
    new_game = Game(mode=args.mode,debug=args.debug, log=args.log, difficulty=difficulty, p1_flag=p1, p2_flag=p2) # Letrehozunk egy uj Game peldanyt
    new_game.print_initials()   # Kiirjuk az alapadatokat konzolra (Debug mod)
    if args.debug:  # A megjelenito fuggvenyek a mode kapcsolotol fuggnek
        print_brd = new_game.print_board_debug  # Debug esetben
        print_res = new_game.print_result_debug # Debug esetben
    else:
        print_brd = lambda: print("Debug mode disabled")
        print_res = lambda: print("Debug mode disabled")
    if args.log:
        new_game.log_game() # Ha kaptunk log kapcsolot akkor letrehozzuk a log fajlt


    print_brd()
    while True: # Vegtelen ciklus
        if new_game.game_over(): # Ha a jatek veget er
            print_res() # Kiirjuk az eredmenyt
            break   # Kitorunk a ciklusbol
        new_game.player_move(new_game.player1, 1) # Egyebkent player 1 lep
        print_brd() # Megjelenitjuk a tablat
        new_game.player_move(new_game.player2, 2) # Player 2 lep
        print_brd() # Megjelenitjuk a tablat
        if args.log:
            new_game.log_game()