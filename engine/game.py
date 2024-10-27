import os.path
from datetime import datetime
from random import getrandbits

from engine.colors import Colors
from engine.player.astar_player import AStarPlayer
from engine.player.greedy_player import GreedyPlayer
from engine.player.ml_player import MLPlayer

from engine.player.player import Player
from engine.player.random_player import RandomPlayer
from engine.player.human_player import HumanPlayer

from typing import Union
from typing import List
from typing import Tuple

from engine.GUI import window

import tkinter as tk
import customtkinter

class Game:
    def __init__(self: "Game", event_queue = "None", mode: str = "cvc", debug: bool = False, log: bool = False, difficulty: Union[None, str] = None, p1_flag: Union[str, None] = None, p2_flag: Union[str, None] = None) -> None:
        self.turn_player1 = True            # Soron kovetkezo jatekos (feher kezd)
        self.pieces_placed_player1 = 0      # Jatekos 1 lerakott korongjai szama
        self.pieces_placed_player2 = 0      # Jatekos 2 lerakott korongjainak szama
        self.game_id = getrandbits(128)     # Egyedi jatekazonosito
        self.mode = mode                    # Jatekmod (pl. cvc - computer vs. computer)
        self.debug = debug                  # Debug parameter
        self.log = log                      # Logolas be- illetve kikapcsolasa
        self.time = datetime.now()          # Az aktualis ido
        self.board = [str(x) for x in range(0,24)] # A tabla reprezentacioja
        self.event_queue = event_queue
        self.mills = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),(0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7), (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23)) # A lehetseges malom poziciok
        self.last_move = None
        self.p1_flag = p1_flag
        self.p2_flag = p2_flag
        self.event_list = [""]
        if debug:
            self.player1, self.player2 = self.initiate_players(mode, difficulty, p1_flag, p2_flag)
        #if not debug:
        #    self.game_GUI = window.GUI(self)

    def reset_game_gui(self):
        self.turn_player1 = True  # Soron kovetkezo jatekos (feher kezd)
        self.pieces_placed_player1 = 0  # Jatekos 1 lerakott korongjai szama
        self.pieces_placed_player2 = 0  # Jatekos 2 lerakott korongjainak szama
        self.game_id = getrandbits(128)  # Egyedi jatekazonosito
        self.time = datetime.now()  # Az aktualis ido
        self.board = [str(x) for x in range(0, 24)]  # A tabla reprezentacioja
        self.last_move = None
        self.event_list = [""]
        self.kijelolt_babu = None
        self.footer_text = ""
        self.GUIRemovePhase = False

    def gui_log_steps(self, log_text):
        self.event_list.append(log_text)

    def start_game_gui(self, mode, difficulty):
        self.player1, self.player2 = self.initiate_players(mode, difficulty, self.p1_flag, self.p2_flag)


    def initiate_players(self, mode: str, difficulty: Union[None, str] = None, p1_flag: Union[str, None] = None, p2_flag: Union[str, None] = None) -> Union[Tuple[Player, Player], None]:
        if mode == "pvp":
            p1 = HumanPlayer("W", self)
            p2 = HumanPlayer("B", self)
            return p1, p2
        if mode == "pvc":
            if difficulty is None:
                raise ValueError("Difficulty cannot be None in a Player vs Computer gamemode")
            p1 = HumanPlayer("W", self)
            if difficulty == "easy":
                p2 = GreedyPlayer("B")
            elif difficulty == "medium":
                p2 = MLPlayer("B")
            else:
                p2 = AStarPlayer("B")
            return p1, p2
        if mode == "cvc":
            if p1_flag is None or p2_flag is None:
                raise ValueError("Computer vs Computer gamemode needs to have both player flags")
            match p1_flag:
                case "greedy":
                    p1 = GreedyPlayer("W")
                case "ml":
                    p1 = MLPlayer("W")
                case "astar":
                    p1 = AStarPlayer("W")
                case "random":
                    p1 = RandomPlayer("W")
                case _:
                    raise ValueError("Non Valid Value provided for p1_flag")

            match p2_flag:
                case "greedy":
                    p2 = GreedyPlayer("B")
                case "ml":
                    p2 = MLPlayer("B")
                case "astar":
                    p2 = AStarPlayer("B")
                case "random":
                    p2 = RandomPlayer("B")
                case _:
                    raise ValueError("None Valid Value provided for p2_flag")
            return p1,p2

    # Jatekadatok kezdeti kiirasa konzolra - Csak debug modban
    def print_initials(self: "Game") -> None:
        if self.debug:
            print("Game id:", self.game_id)
            print("Game mode:", self.mode)
            print(f"{self.player1.name} vs. {self.player2.name}\n")
            print("Time:", self.time)


    # A tabla aktualis allapotanak kirajzolasa konzolra - Csak debug mod
    def print_board_debug(self: "Game") -> None:
        # Színes board létrehozása
        colored_board = []
        for index, piece in enumerate(self.board):  # 'enumerate' kell, hogy az indexet is kapjuk
            if piece == 'W':
                colored_board.append(
                    f"{Colors.BACK_WHITE}{Colors.BLACK}W {Colors.ENDC}{Colors.GREEN}")  # Fehér korong + space
            elif piece == 'B':
                colored_board.append(
                    f"{Colors.BACK_GREY}{Colors.WHITE}B {Colors.ENDC}{Colors.GREEN}")  # Fekete korong + space
            else:
                # Egyjegyű számok esetén is space-t rakunk mögé
                if len(piece) == 1:
                    colored_board.append(f"{Colors.OKBLUE}{piece} {Colors.ENDC}{Colors.GREEN}")  # Kék szám + space
                else:
                    colored_board.append(f"{Colors.OKBLUE}{piece}{Colors.ENDC}{Colors.GREEN}")  # Kétjegyű szám (pl. 10, 11, stb.)

        print(f"""
                                           Table
                             {Colors.GREEN}{colored_board[0]}--------------{colored_board[1]}---------------{colored_board[2]}{Colors.ENDC}
                             {Colors.GREEN}|{" " * 15}|{" " * 16}|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }{colored_board[3]}---------{colored_board[4]}----------{colored_board[5]}{" " * 3}|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }|{" " * 10}|{" " * 11}|{" " * 4 }|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }|{" " * 4 }{colored_board[6]}----{colored_board[7]}-----{colored_board[8]}{" " * 3}|{" " * 4}|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }|{" " * 4 }|{" " * 12}|{" " * 4 }|{" " * 4 }|{Colors.ENDC}
                             {Colors.GREEN}{colored_board[9]}---{colored_board[10]}---{colored_board[11]}{" " * 11}{colored_board[12]}---{colored_board[13]}---{colored_board[14]}{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }|{" " * 4 }|{" " * 12}|{" " * 4 }|{" " * 4 }|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }|{" " * 4 }{colored_board[15]}----{colored_board[16]}-----{colored_board[17]}{" " * 3 }|{" " * 4 }|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }|{" " * 10}|{" " * 11}|{" " * 4 }|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 4 }{colored_board[18]}---------{colored_board[19]}----------{colored_board[20]}{" " * 3 }|{Colors.ENDC}
                             {Colors.GREEN}|{" " * 15}|{" " * 16}|{Colors.ENDC}
                             {Colors.GREEN}{colored_board[21]}--------------{colored_board[22]}---------------{colored_board[23]}{Colors.ENDC}
        """)

        print()

    # Az aktualis jatekos meghatarozasa
    def current_player(self: "Game") -> "Player":
        return self.player1 if self.turn_player1 else self.player2

    # Kor atadasa masik jatekosnak
    def switch_turns(self: "Game") -> None:
        self.turn_player1 = not self.turn_player1




    # Egy lepest regisztral a tablan
    # Ha a celpozicio (target) adott, akkor a mozgatasi fazisban vagyunk, ha nincs megadva, akkor a lerakasi fazisban.
    # Ha a lepes ervenytelen, es a debug mod aktiv, akkor figyelmezteto uzenetet ad vissza.
    # Malom eseten korong levetelre kerul sor.
    def register_move(self: "Game", move: int, target: Union[None, int] = None) -> None:
        if move is None:    # Ellenorizzuk, hogy a lepes ervenyes-e (nem None)
            if self.debug:
                print("Invalid move. No move was made.") # Hiba log (Debug modban)
            return
        # Elmentjük az utolsó lépés pozícióját
        self.last_move = move if target is None else target
        if target is not None: # Ha kapunk target parametert akkor a mozgatasi fazisban vagyunk
            if self.board[move] == self.current_player().color and self.board[target] not in ['W', 'B']: # Ellenorizzuk, hogy a sajat korongunkat akarjuk e mozgatni es hogy a cel pozicio ures-e
                self.board[move] = str(move) # Eredeti poziciot visszaallitjuk
                self.board[target] = self.current_player().color # Uj poziciora beirjuk a korongot
                if self.mill_is_made(): # Ha malom keletkezik
                    if self.debug:
                        self.print_board_debug()
                        print(f"Mill formed by {self.current_player().color}!") # Debug log
                    if (self.debug and self.current_player().name == "HumanPlayer"):
                        self.remove_opponent_piece()  # Meghivjuk a koronglevetelert felelos metodust
                    elif self.current_player().name != "HumanPlayer":
                        event_text = "White gets a Mill" if self.turn_player1 else "Black gets a Mill"
                        self.event_list.append(event_text)
                        self.remove_opponent_piece()  # Meghivjuk a koronglevetelert felelos metodust
                    else:
                        self.GUIRemovePhase = True
                        print("GUI Remove Phase")
                        event_text = "White gets a Mill" if self.turn_player1 else "Black gets a Mill"
                        self.event_list.append(event_text)

                elif self.debug == False and self.current_player().name == "HumanPlayer":
                    self.switch_turns()
            else: # Ervenytelen lepest kaptunk
                if self.debug:
                    print("Invalid move.") # Hiba log (Debug modban)
        else: # Lerakasi fazisban vagyunk
            if self.board[move] not in ['W', 'B']: # Ellenorizzuk, hogy a megadott mezon van-e mar korong
                self.board[move] = self.current_player().color # A kapott mezore beirjuk a jatekos korongjat
                if self.current_player() == self.player1: # Meghatarozzuk az aktualis jatekost
                    self.pieces_placed_player1 += 1     # Ha a player1 kore volt akkor a hozzatartozo korong szamlalot noveljuk
                else:
                    self.pieces_placed_player2 += 1     # Ha a player2 kore volt akkor a hozzatartozo korong szamlalot noveljuk
                if self.mill_is_made(): # Ha malom keletkezik
                    if self.debug:
                        self.print_board_debug()
                        print(f"Mill formed by {self.current_player().color}!") # Debug log
                    if (self.debug and self.current_player().name == "HumanPlayer"):
                        self.remove_opponent_piece()  # Meghivjuk a koronglevetelert felelos metodust
                    elif self.current_player().name != "HumanPlayer":
                        event_text = "White gets a Mill" if self.turn_player1 else "Black gets a Mill"
                        self.event_list.append(event_text)
                        self.remove_opponent_piece()  # Meghivjuk a koronglevetelert felelos metodust
                    else:
                        self.GUIRemovePhase = True
                        print("GUI Remove Phase")
                        event_text = "White gets a Mill" if self.turn_player1 else "Black gets a Mill"
                        self.event_list.append(event_text)



                elif self.debug == False and self.current_player().name == "HumanPlayer":
                    self.switch_turns()
            else: # Foglalt a megadott pozicio (es Lerakasi fazisban vagyunk)
                if self.debug:
                    print("Invalid move, position already taken.") # Hiba log (Debug mod)
        if not self.debug:
            self.footer_text = ""

    # Ellenorzi, hogy egy adott pozicio egy malom resze-e.
    # Ha a megadott pozicio (position) a jatekos szinevel megegyezo
    # es egy malomban van, akkor True ertekkel ter vissza, egyebkent False.
    def part_of_mill(self: "Game", position: int, player_color: str) -> bool:
        for mill in self.mills: # Vegigmegyunk az osszes malom kombinacion
            if position in mill and all(self.board[i] == player_color for i in mill): # Ellenorizzuk, hogy a megadott pozicio benne van-e a malomban,
                return True # es hogy a malom poziciojan ugyanaz a jatekos szine van-e
        return False    # Pozicio nem resze malomnak



    # Malom eseten a jatekos elvehet egy korongot az ellenfeltol, ezt a logikat valositja meg.
    # Eloszor azokat a korongokat keresi meg,amelyek nincsenek malomban, ha van ilyen.
    # Ha az osszes korong malomban van, akkor barmelyik korong elveheto.
    def remove_opponent_piece(self: "Game", piece_to_remove_GUI = None) -> None:
        current_player = self.current_player()  # Meghatarozzuk az aktualis jatekost
        opponent_color = 'B' if current_player.color == 'W' else 'W' # Meghatarozzuk az ellenfel szinet

        opponent_pieces_on_board = [i for i, piece in enumerate(self.board) if piece == opponent_color] # Osszegyujtjuk az ellenfel osszes korongjat egy listaban
        removable_pieces = [i for i in opponent_pieces_on_board if not self.part_of_mill(i, opponent_color)] # Leszurjuk azokat a korongokat amik nincsenek malomban

        if not removable_pieces: # Ha az ellenfel osszes korongja malomban van,
            removable_pieces = opponent_pieces_on_board # akkor tetszoleges elveheto

        if piece_to_remove_GUI == None:
            piece_to_remove = current_player.choose_opponent_piece_to_remove(self.board,removable_pieces) # A jatekos (AI vagy Human) donti el, melyik korongot veszi le
            if self.debug:
                print(f"{current_player.color} removes opponent's piece at position {piece_to_remove}") # Game log (Debug mod)
            self.board[piece_to_remove] = str(piece_to_remove) # A valasztott korongot levesszuk a tablarol
            self.event_list.append(f"White removes piece {piece_to_remove}" if self.turn_player1 else f"Black removes piece {piece_to_remove}")

        else:
            if piece_to_remove_GUI in removable_pieces:
                self.board[piece_to_remove_GUI] = str(piece_to_remove_GUI)
                self.GUIRemovePhase = False
                self.event_list.append(f"White removes piece {piece_to_remove_GUI}" if self.turn_player1 else f"Black removes piece {piece_to_remove_GUI}")
                self.switch_turns()
            else:
                self.footer_text = "Nem levehető korong!"


    # Azt vizsgalja, hogy veget ert-e a jatek
    # Ha minden korongot leraktak es nincs elegendo korong valamelyik jatekosnal,
    # vagy ha nincs tobb ervenyes lepes.
    def game_over(self: "Game") -> bool:
        total_pieces_placed = self.pieces_placed_player1 + self.pieces_placed_player2 # Osszesitjuk az osszes lerakott korongot
        if total_pieces_placed < 18: # Ha meg nem raktuk le az osszes korongot akkor a jatek meg biztosan tart
            return False
        player1_pieces = self.board.count('W')  # Osszesitjuk a feher korongokat (mar biztosan a mozgasi fazisban vagyunk)
        player2_pieces = self.board.count('B')  # Osszesitjuk a fekete korongokat (mar biztosan a mozgasi fazisban vagyunk)
        if player1_pieces < 3 or player2_pieces < 3:   # Ha barmely jatekosnak 3-nal kevesebb korongja van,
            return True # akkor a jatek veget ert
        if not self.generate_valid_moves(noprint=True): # Ha egy jatekos sem tud lepni (None a lehetséges lepesek listaja),
            return True # akkor is vege a jateknak
        return False # Minden egyeb esetben meg nincs vege



    # Az aktualis jatekos szamara general valid lepeseket
    # Ket fazist kezel:
    # 1. Lerakasi fazis: ha a jatekos meg nem rakta le az osszes korongjat,
    #    akkor a tabla ures helyeit adja vissza.
    # 2. Mozgatasi fazis: ha mar minden korong le lett rakva, akkor csak a jatekos
    #    korongjai melletti ures helyekre lehet lepni.
    def generate_valid_moves(self: "Game", noprint: bool = False) -> Union[List[int], List[Tuple[int, int]]]:
        current_player_pieces = 'W' if self.current_player() == self.player1 else 'B'   # Meghatarozzuk az aktualis jatekos szinet

        if self.pieces_placed_player1 < 9 or self.pieces_placed_player2 < 9:    # Ellenorizzuk, hogy lerakasi fazisban vagyunk-e
            valid_moves = [i for i in range(24) if self.board[i] not in ['W', 'B']] # Ha igen, osszegyujtjuk azokat a poziciokat amik meg uresek
            if not noprint and self.debug:
                print(f"Valid placement spots: {valid_moves}")  # Debug log
            return valid_moves  # Visszaadjuk a lepesek listajat

        if not noprint and self.debug:
            print(f"\nPlayer is in the movement phase.")    # Debug log - Ha ideaig elerunk akkor mozgasi fazisban van a jatek

        player_pieces_on_board = [i for i, x in enumerate(self.board) if x == current_player_pieces]    # Meghatarozzuk az aktualis jatekos korongjainak poziciojat

        adjacency_list = {  # Definialjuk a tabla osszes mezojere annak szomszedait
            0: [1, 9], 1: [0, 2, 4], 2: [1, 14], 3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13], 6: [7, 11], 7: [4, 6, 8],
            8: [7, 12], 9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15], 12: [8, 13, 17], 13: [5, 12, 14, 20],
            14: [2, 13, 23], 15: [11, 16], 16: [15, 17, 19], 17: [12, 16], 18: [10, 19], 19: [16, 18, 20, 22],
            20: [13, 19], 21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
        }

        if len(player_pieces_on_board) == 3: # Ha 3 babu van akkor ugras.
            valid_moves = []  # Ures lista - ebben gyujtuk majd a lehetseges lepeseket
            for piece in player_pieces_on_board:  # Vegignezzuk a jatekos letett korongjait
                for i in range(0,23):
                 if self.board[i] not in ['W', 'B']:
                     valid_moves.append((piece, i))

        else:
            valid_moves = [] # Ures lista - ebben gyujtuk majd a lehetseges lepeseket
            for piece in player_pieces_on_board: # Vegignezzuk a jatekos letett korongjait
                for neighbor in adjacency_list[piece]:  # Vegigmegyunk a szomszedsagi konyvtarunkon
                    if self.board[neighbor] not in ['W', 'B']:  # Ha koronggal szomszedos mezo ures,
                        valid_moves.append((piece, neighbor))   # akkor hozzaadjuk a listahoz egy tuple adatszerkezetben (honnan hova lehet lepni)

        if not noprint and self.debug:
             print(f"Valid moves for {self.current_player().color}: {valid_moves}") # Debug log
        return valid_moves  # Visszaadjuk a lehetseges lepesek listajat


    def player_move(self: "Game", player, player_number: int, lepes = None) -> None:
        self.footer_text = ""
        if self.GUIRemovePhase:
            self.remove_opponent_piece(lepes)

        else:
            if self.debug:
                print(f"Player{player_number}'s turn")  # Debug log


            pieces_placed = self.pieces_placed_player1 if player_number == 1 else self.pieces_placed_player2

            if self.debug or player.name != "HumanPlayer":
                if pieces_placed < 9:  # Ha kevesebb mint 9 korongot rakott le, akkor lerakási fázisban vagyunk
                    move = player.make_move(self.board ,self.generate_valid_moves())  # Meghívjuk a játékos lépését
                    esemeny = f"{'White' if player_number == 1 else 'Black'} moves to: {move}"
                    self.gui_log_steps(esemeny)
                    self.register_move(move)  # A visszaadott lépést regisztráljuk
                    if self.debug:
                        print(f"Player{player_number} moves:", move)  # Debug log

                else:  # Egyébként mozgatási fázisban vagyunk
                    move, target = player.make_move(self.board,self.generate_valid_moves())  # Tuple-t fogunk visszakapni
                    esemeny = f"{'White' if player_number == 1 else 'Black'} moves from: {move} to: {target}"
                    self.gui_log_steps(esemeny)
                    self.register_move(move, target)  # Regisztráljuk a lépést
                    if self.debug:
                        print(f"Player{player_number} moves:", move, target)  # Debug log
                        if self.log:
                            self.log_game(f"Player{player_number} moves: {move} to {target}\n")

                self.switch_turns()  # Átadjuk a kört a másik játékosnak

            else:
                if pieces_placed < 9:  # Ha kevesebb mint 9 korongot rakott le, akkor lerakási fázisban vagyunk
                    if lepes in self.generate_valid_moves():
                        move = lepes  # Meghívjuk a játékos lépését
                        self.register_move(move)  # A visszaadott lépést regisztráljuk
                        if not(self.player1.name == "HumanPlayer" and self.player2.name == "HumanPlayer"): # Csak akkor csusztatunk ha az egyik player AI
                            self.event_queue.put(-1)
                        esemeny = f"{'White' if player_number == 1 else 'Black'} moves to: {lepes}"
                        self.gui_log_steps(esemeny)
                        #self.switch_turns()  # Átadjuk a kört a másik játékosnak
                    else:
                        self.footer_text = "Helytelen lépés"
                else:  # Egyébként mozgatási fázisban vagyunk
                    if self.kijelolt_babu == None:
                        self.kijelolt_babu = lepes #Nem mozgatunk, csak megjegyezzuk
                    else:
                        self.register_move(self.kijelolt_babu, lepes)  # Regisztráljuk a lépést
                        esemeny = f"{'White' if player_number == 1 else 'Black'} moves from: {self.kijelolt_babu} to: {lepes}"
                        self.kijelolt_babu = None
                        self.gui_log_steps(esemeny)
                        self.switch_turns()  # Átadjuk a kört a másik játékosnak, de csak ha már a cél is megvan.


            if self.debug:
                print(f"Player{player_number} moves: {lepes}")  # Debug log



    # A jatek vegeredmenyet jeleniti meg debug modban konzolon.
    # Ha barmelyik jatekosnak 3-nal kevesebb korongja maradt, az a jatekos vesztett.
    # Ha mindket jatekosnak legalabb 3 korongja van, akkor dontetlen.
    def print_result_debug(self: "Game") -> None:
        if self.board.count('W') < 3:   # Ha Player1-nek kevesebb mint 3 korongja maradt, Player2 nyert
            if self.debug:
                print(f"Player 2 {self.player2} wins!") # Game log (Debug mod)
        elif self.board.count('B') < 3: # Ha Player2-nek kevesebb mint 3 korongja maradt, Player1 nyert
            if self.debug:
                print(f"Player 1 {self.player1} wins!") # Game log (Debug mod)
        else:   # Ha egyik jatekosnak sincs 3nal kevesebb (ide mar csak akkor juthatunk el ha nincs tobb valid lepes)
            if self.debug:
                print("It's a draw.")   # Game log (Debug mod) - Dontetlen


    # A mill_is_made fuggveny ellenorzi, hogy keletkezett-e malom.
    # Egy malom akkor keletkezik, ha a jatekosnak 3 azonos szinu korongja van egy vonalban
    # (a tabla elore definialt helyzetein).
    def mill_is_made(self: "Game") -> bool:
        # Az utolsó lépés pozíciójához kapcsolódó malmokat vizsgáljuk
        for mill in self.mills:
            if self.last_move in mill:  # Csak azokat a malmokat nézzük, amelyek tartalmazzák az utolsó lépést
                if self.board[mill[0]] == self.board[mill[1]] == self.board[mill[2]] == self.current_player().color:
                    return True
        return False



    # A jatek alapadatait logolja egy txt fajlba (/log mappa).
    # Minden jatekhoz egy egyedi azonosito alapjan kulon log fajl keszul.
    # A log a jatek ID-jat, kezdeti idejet es jatekmodjat fogja tartalmazni a fuggveny futtatasa utan.
    def log_game(self: "Game", logtext: str = "") -> None:
        project_root = os.path.dirname(os.path.abspath(__file__)) # Taroljuk a projekt gyokerkonyvtarat
        log_dir = os.path.join(project_root, "log") # Beallitjuk az eleresi utvonalat
        if not os.path.exists(log_dir): # Ha nincs ilyen konyvtar,
            os.makedirs(log_dir)    # letrehozzuk
        log_file_path = os.path.join(log_dir, f"{self.game_id}.txt") # Osszefuzzuk a (csak az eleresi utat) a gamid-val
        if not os.path.exists(log_file_path):   # Ha log fajl nem letezik letrehozzuk,
            with open(log_file_path, mode="w") as f:    # es logoljuk az alapveto informaciokat
                f.write(f"Game ID: {self.game_id}\n")   # game_id log
                f.write(f"Time: {self.time}\n")         # current time log
                f.write(f"Mode: {self.mode}\n")         # mode log
                f.write(f"{self.player1.name} vs. {self.player2.name}\n")
        elif logtext != "":   # ha a log fajl mar letezik nem irjuk felul
            with open(log_file_path, mode="a") as f: #append a log fájl végére
                f.write(logtext)
        return

if __name__ == '__main__':
    print("This script cannot be run directly.")