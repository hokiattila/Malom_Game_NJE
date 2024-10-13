from .player import Player
import ast
# HumanPlayer - emberi jatekos
# Player osztaly leszarmazottja
# Debug modban stdout-on keresztul kapja meg a userinputot,
# alapmodban GUI feluleten

# Milestone 1 - TODO (Armand)
class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color)

    def get_valid_move(self, valid_moves):
        pieces = {move[0] for move in valid_moves}  # Kiválasztott korongok egyedi készlete
        print(f"Elérhető korongok: {pieces}")

        # Kérjük be a korongot a felhasználótól
        piece_to_move = None
        while True:
            try:
                piece_to_move = int(input(f"Válassz egy korongot a következők közül: {pieces}: "))
                if piece_to_move in pieces:
                    break  # Ha a választott korong érvényes, kilépünk a ciklusból
                else:
                    print("Ez a korong nem érvényes! Kérlek, válassz egy másikat.")
            except ValueError:
                print("Hibás bemenet! Kérlek, egy számot adj meg.")

        # Kiírjuk a kiválasztott koronghoz tartozó szomszédokat
        neighbors = [move[1] for move in valid_moves if move[0] == piece_to_move]
        print(f"A(z) {piece_to_move} korong szomszédai: {neighbors}")

        # Kérjük be a szomszédot a felhasználótól
        neighbor_to_move = None
        while True:
            try:
                neighbor_to_move = int(input(f"Válassz egy szomszédos mezőt a következők közül: {neighbors}: "))
                if neighbor_to_move in neighbors:
                    return (piece_to_move, neighbor_to_move)  # Visszaadjuk az érvényes lépést
                else:
                    print(f"A(z) {neighbor_to_move} nem érvényes szomszédos mező! Kérlek, válassz egy másikat.")
            except ValueError:
                print("Hibás bemenet! Kérlek, egy számot adj meg.")

    # Milestone 1 TODO (Armand)
    def make_move(self, valid_moves):
            # Ellenőrizzük, hogy vannak-e érvényes lépések
            if not valid_moves:
                print("Nincsenek érvényes lépések!")
                return None

            while True:  # Addig ismételjük, amíg nem kapunk érvényes bemenetet
                if all(isinstance(move, tuple) for move in valid_moves):
                    return self.get_valid_move(valid_moves)
                else:
                    try:
                        # Bekérjük a játékos lépését
                        move = int(input("Add meg a lépésed (0-23 közötti szám): "))

                        # Ellenőrizzük, hogy a megadott lépés érvényes-e
                        if move in valid_moves:
                            return move  # Ha érvényes, visszatérünk vele
                        else:
                            print(f"A {move} nem érvényes lépés! Próbáld újra.")
                    except ValueError:
                        # Ha nem sikerül a bemenetet számra konvertálni, hibát dobunk
                        print("Hibás bemenet! Kérlek, egy 0-23 közötti számot adj meg.")


    # Milestone 1 TODO (Armand)
    @staticmethod
    def choose_opponent_piece_to_remove(removable_pieces):

            while True:  # Addig ismételjük, amíg nem kapunk érvényes bemenetet
                try:
                    # Bekérjük a játékos lépését
                    print("Levehető korongok: " + str(removable_pieces))

                    move = int(input("Add meg a leveendő korongot: "))

                    # Ellenőrizzük, hogy a megadott lépés érvényes-e
                    if move in removable_pieces:
                        return move  # Ha érvényes, visszatérünk vele
                    else:
                        print(f"A {move} nem levehető! Próbáld újra.")
                except ValueError:
                    # Ha nem sikerül a bemenetet számra konvertálni, hibát dobunk
                    print("Hibás bemenet!")

if __name__ == "__main__":
    print("This script cannot be run directly.")