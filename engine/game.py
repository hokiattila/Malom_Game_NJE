import os.path
from datetime import datetime
from random import getrandbits
from engine.player.random_player import RandomPlayer

class Game:
    def __init__(self, mode="cvc", debug=False, log=False):
        self.player1 = RandomPlayer("W")    # Jatekos 1 (feher korong)
        self.player2 = RandomPlayer("B")    # Jatekos 2 (fekete korong)
        self.turn_player1 = True            # Soron kovetkezo jatekos (feher kezd)
        self.pieces_placed_player1 = 0      # Jatekos 1 lerakott korongjai szama
        self.pieces_placed_player2 = 0      # Jatekos 2 lerakott korongjainak szama
        self.game_id = getrandbits(128)     # Egyedi jatekazonosito
        self.mode = mode                    # Jatekmod (pl. cvc - computer vs. computer)
        self.debug = debug                  # Debug parameter
        self.log = log                      # Logolas be- illetve kikapcsolasa
        self.time = datetime.now()          # Az aktualis ido
        self.board = [str(x) for x in range(0,24)] # A tabla reprezentacioja
        self.mills = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),(0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7), (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23)) # A lehetseges malom poziciok

    # Jatekadatok kezdeti kiirasa konzolra - Csak debug modban
    def print_initials(self):
        if self.debug:
            print("Game id:", self.game_id)
            print("Game mode:", self.mode)
            print("Time:", self.time)

    # Milestone 1 TODO (Armand)
    # Lepesek logolasa az elozetesen letrehozott {game_id}.txt fajlba - Csak --log kapcsolo eseten
    def log_move(self, move):
        pass

    # Ket karakteres mezok kiiratasat korrigaljuk
    @staticmethod
    def adjust(char):
        if len(char) == 1:
            return char + ' '
        return char


    # A tabla aktualis allapotanak kirajzolasa konzolra - Csak debug mod
    def print_board_debug(self):
        print(
            '                                   Tábla\n'
            '                     {}--------------{}---------------{}\n'
            '                     |               |                |\n'
            '                     |    {}---------{}----------{}   |\n'
            '                     |    |          |           |    |\n'
            '                     |    |    {}----{}-----{}   |    |\n'
            '                     |    |    |            |    |    |\n'
            '                     {}---{}---{}           {}---{}---{}\n'
            '                     |    |    |            |    |    |\n'
            '                     |    |    {}----{}-----{}   |    |\n'
            '                     |    |          |           |    |\n'
            '                     |    {}---------{}----------{}   |\n'
            '                     |               |                |\n'
            '                     {}--------------{}---------------{}\n'.format(self.adjust(self.board[0]), self.adjust(self.board[1]), self.adjust(self.board[2]), self.adjust(self.board[3]), self.adjust(self.board[4]), self.adjust(self.board[5]), self.adjust(self.board[6]),
                self.adjust(self.board[7]),self.adjust(self.board[8]), self.adjust(self.board[9]), self.adjust(self.board[10]), self.adjust(self.board[11]), self.adjust(self.board[12]), self.adjust(self.board[13]), self.adjust(self.board[14]),self.adjust(self.board[15]),self.adjust(self.board[16]), self.adjust(self.board[17]), self.adjust(self.board[18]), self.adjust(self.board[19]), self.adjust(self.board[20]), self.adjust(self.board[21]), self.adjust(self.board[22]),
                self.adjust(self.board[23])))
        print()

    # Az aktualis jatekos meghatarozasa
    def current_player(self):
        return self.player1 if self.turn_player1 else self.player2

    # Kor atadasa masik jatekosnak
    def switch_turns(self):
        self.turn_player1 = not self.turn_player1


    # Egy lepest regisztral a tablan
    # Ha a celpozicio (target) adott, akkor a mozgatasi fazisban vagyunk, ha nincs megadva, akkor a lerakasi fazisban.
    # Ha a lepes ervenytelen, es a debug mod aktiv, akkor figyelmezteto uzenetet ad vissza.
    # Malom eseten korong levetelre kerul sor.
    def register_move(self, move, target=None):
        if move is None:    # Ellenorizzuk, hogy a lepes ervenyes-e (nem None)
            if self.debug:
                print("Invalid move. No move was made.") # Hiba log (Debug modban)
            return
        if target is not None: # Ha kapunk target parametert akkor a mozgatasi fazisban vagyunk
            if self.board[move] == self.current_player().color and self.board[target] not in ['W', 'B']: # Ellenorizzuk, hogy a sajat korongunkat akarjuk e mozgatni es hogy a cel pozicio ures-e
                self.board[move] = str(move) # Eredeti poziciot visszaallitjuk
                self.board[target] = self.current_player().color # Uj poziciora beirjuk a korongot
                if self.mill_is_made(): # Ha malom keletkezik
                    if self.debug:
                        print(f"Mill formed by {self.current_player().color}!") # Debug log
                    self.remove_opponent_piece() # Meghivjuk a koronglevetelert felelos metodust
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
                        print(f"Mill formed by {self.current_player().color}!") # Debug log
                    self.remove_opponent_piece() # Meghivjuk a koronglevetelert felelos metodust
            else: # Foglalt a megadott pozicio (es Lerakasi fazisban vagyunk)
                if self.debug:
                    print("Invalid move, position already taken.") # Hiba log (Debug mod)


    # Ellenorzi, hogy egy adott pozicio egy malom resze-e.
    # Ha a megadott pozicio (position) a jatekos szinevel megegyezo
    # es egy malomban van, akkor True ertekkel ter vissza, egyebkent False.
    def part_of_mill(self, position, player_color):
        for mill in self.mills: # Vegigmegyunk az osszes malom kombinacion
            if position in mill and all(self.board[i] == player_color for i in mill): # Ellenorizzuk, hogy a megadott pozicio benne van-e a malomban,
                return True # es hogy a malom poziciojan ugyanaz a jatekos szine van-e
        return False    # Pozicio nem resze malomnak



    # Malom eseten a jatekos elvehet egy korongot az ellenfeltol, ezt a logikat valositja meg.
    # Eloszor azokat a korongokat keresi meg,amelyek nincsenek malomban, ha van ilyen.
    # Ha az osszes korong malomban van, akkor barmelyik korong elveheto.
    def remove_opponent_piece(self):
        current_player = self.current_player()  # Meghatarozzuk az aktualis jatekost
        opponent_color = 'B' if current_player.color == 'W' else 'W' # Meghatarozzuk az ellenfel szinet

        opponent_pieces_on_board = [i for i, piece in enumerate(self.board) if piece == opponent_color] # Osszegyujtjuk az ellenfel osszes korongjat egy listaban
        removable_pieces = [i for i in opponent_pieces_on_board if not self.part_of_mill(i, opponent_color)] # Leszurjuk azokat a korongokat amik nincsenek malomban

        if not removable_pieces: # Ha az ellenfel osszes korongja malomban van,
            removable_pieces = opponent_pieces_on_board # akkor tetszoleges elveheto

        piece_to_remove = current_player.choose_opponent_piece_to_remove(removable_pieces) # A jatekos (AI vagy Human) donti el, melyik korongot veszi le
        if self.debug:
            print(f"{current_player.color} removes opponent's piece at position {piece_to_remove}") # Game log (Debug mod)
        self.board[piece_to_remove] = str(piece_to_remove) # A valasztott korongot levesszuk a tablarol

    # Azt vizsgalja, hogy veget ert-e a jatek
    # Ha minden korongot leraktak es nincs elegendo korong valamelyik jatekosnal,
    # vagy ha nincs tobb ervenyes lepes.
    def game_over(self):
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
    # TODO ugras implementalasa (Armand)
    def generate_valid_moves(self, noprint=False):
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

        valid_moves = [] # Ures lista - ebben gyujtuk majd a lehetseges lepeseket
        for piece in player_pieces_on_board: # Vegignezzuk a jatekos letett korongjait
            for neighbor in adjacency_list[piece]:  # Vegigmegyunk a szomszedsagi konyvtarunkon
                if self.board[neighbor] not in ['W', 'B']:  # Ha koronggal szomszedos mezo ures,
                    valid_moves.append((piece, neighbor))   # akkor hozzaadjuk a listahoz egy tuple adatszerkezetben (honnan hova lehet lepni)

        if not noprint and self.debug:
            print(f"Valid moves for {self.current_player().color}: {valid_moves}") # Debug log

        return valid_moves  # Visszaadjuk a lehetseges lepesek listajat


    # Player 1 soron levo lepeset kezeli.
    # Eloszor ellenorzi, hogy a jatek lerakasi fazisban van-e (9-nel kevesebb a lerakott korongok szama),
    # vagy a mozgatasi fazisban. Ez alapjan hivja meg a megfelelo lepeseket, majd visszaadja a kort Player 2-nek.
    def player1_move(self):
        if self.debug:
            print("Player1's turn") # Debug log
        if self.pieces_placed_player1 < 9:  # Ha Player1 9nel kevesebb korongot rakott le, akkor lerakasi fazisban vagyunk
            move = self.player1.make_move(self.generate_valid_moves())  # Meghivjuk a Player1 lepesert felelos metodusat, es atadjuk neki a valid lepeseket
            self.register_move(move)    # A Player1 altal visszadott lepest regisztraljuk a tablan
            if self.debug:
                print("Player1 moves:", move) # Debug log
        else:   # Egyebkent ha lerakasi fazisban vagyunk
            move, target = self.player1.make_move(self.generate_valid_moves()) # Meghivjuk a Player1 lepesert felelos metodusat, viszont tuple-t fogunk visszakapni, ezt ki kell csomagolnunk
            self.register_move(move, target)    # Regisztraljuk a lepest a tablan
            if  self.debug:
             print("Player2 moves:", move, target)  # Debug log
        self.switch_turns() # Atadjuk a kort a Player2-nek


    # Player 2 soron levo lepeset kezeli.
    # Eloszor ellenorzi, hogy a jatek lerakasi fazisban van-e (9-nel kevesebb a lerakott korongok szama),
    # vagy a mozgatasi fazisban. Ez alapjan hivja meg a megfelelo lepeseket, majd visszaadja a kort Player 1-nek.
    def player2_move(self):
        if self.debug:
            print("Player2's turn") # Debug log
        if self.pieces_placed_player2 < 9:  # Ha Player2 9nel kevesebb korongot rakott le, akkor lerakasi fazisban vagyunk
            move = self.player2.make_move(self.generate_valid_moves())  # Meghivjuk a Player2 lepesert felelos metodusat, es atadjuk neki a valid lepeseket
            self.register_move(move)    # A Player2 altal visszadott lepest regisztraljuk a tablan
            if self.debug:
                print("Player2 moves:",move)   # Debug log
        else:    # Egyebkent ha lerakasi fazisban vagyunk
            move, target = self.player2.make_move(self.generate_valid_moves())  # Meghivjuk a Player2 lepesert felelos metodusat, viszont tuple-t fogunk visszakapni, ezt ki kell csomagolnunk
            self.register_move(move, target)    # Regisztraljuk a lepest a tablan
            if  self.debug:
                print("Player2 moves:", move, target)   # Debug log
        self.switch_turns() # Atadjuk a kort a Player1-nek


    # A jatek vegeredmenyet jeleniti meg debug modban konzolon.
    # Ha barmelyik jatekosnak 3-nal kevesebb korongja maradt, az a jatekos vesztett.
    # Ha mindket jatekosnak legalabb 3 korongja van, akkor dontetlen.
    def print_result_debug(self):
        if self.board.count('W') < 3:   # Ha Player1-nek kevesebb mint 3 korongja maradt, Player2 nyert
            if self.debug:
                print("Player 2 (Black) wins!") # Game log (Debug mod)
        elif self.board.count('B') < 3: # Ha Player2-nek kevesebb mint 3 korongja maradt, Player1 nyert
            if self.debug:
                print("Player 1 (White) wins!") # Game log (Debug mod)
        else:   # Ha egyik jatekosnak sincs 3nal kevesebb (ide mar csak akkor juthatunk el ha nincs tobb valid lepes)
            if self.debug:
                print("It's a draw.")   # Game log (Debug mod) - Dontetlen


    # A mill_is_made fuggveny ellenorzi, hogy keletkezett-e malom.
    # Egy malom akkor keletkezik, ha a jatekosnak 3 azonos szinu korongja van egy vonalban
    # (a tabla elore definialt helyzetein).
    def mill_is_made(self):
        for mill in self.mills: # Vegig megyunk az osszes malom kombinacion
            if self.board[mill[0]] == self.board[mill[1]] == self.board[mill[2]] == self.current_player().color:    # Ellenorizzuk, hogy mindharom pozicion megegyezo szin talalhato-e
                return True # Ha igen akkor keletkezett malom,
        return False    # egyebkent nem



    # A jatek alapadatait logolja egy txt fajlba (/log mappa).
    # Minden jatekhoz egy egyedi azonosito alapjan kulon log fajl keszul.
    # A log a jatek ID-jat, kezdeti idejet es jatekmodjat fogja tartalmazni a fuggveny futtatasa utan.
    def log_game(self):
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
        else:   # ha a log fajl mar letezik nem irjuk felul
            return

if __name__ == '__main__':
    print("This script cannot be run directly.")