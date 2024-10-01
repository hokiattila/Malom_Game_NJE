
class Game:
    def __init__(self):
        self.board = [str(x) for x in range(0,24)]
        self.mills = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11), (12, 13, 14), (15, 16, 17), (18, 19, 20), (21, 22, 23),(0, 9, 21), (3, 10, 18), (6, 11, 15), (1, 4, 7), (16, 19, 22), (8, 12, 17), (5, 13, 20), (2, 14, 23))

    def print_board(self):
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

    @staticmethod
    def adjust(char):
        if len(char) == 1:
            return char + ' '
        return char

if __name__ == '__main__':
    print("This script cannot be run directly.")