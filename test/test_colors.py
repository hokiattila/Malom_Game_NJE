import unittest
from colors import Colors

class TestColors(unittest.TestCase):

    def test_attributes_exist(self):
        # Ellenőrizzük, hogy az összes szín attribútum létezik
        color_attributes = [
            'HEADER', 'OKBLUE', 'OKCYAN', 'OKGREEN', 'WARNING', 'FAIL', 
            'ENDC', 'BOLD', 'UNDERLINE', 'GREY', 'DARK_ORANGE', 
            'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 
            'CYAN', 'WHITE', 'BACK_GREY', 'BACK_BLACK', 'BACK_RED', 
            'BACK_GREEN', 'BACK_YELLOW', 'BACK_BLUE', 'BACK_MAGENTA', 
            'BACK_CYAN', 'BACK_WHITE'
        ]
        
        for attr in color_attributes:
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(Colors, attr))

    def test_attribute_modification(self):
        # Ellenőrizzük, hogy az attribútumok nem módosíthatók
        color = Colors()
        
        with self.assertRaises(AttributeError):
            color.HEADER = '\033[90m'  # Próbálkozás a HEADER attribútum módosításával

if __name__ == '__main__':
    unittest.main()
