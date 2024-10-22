from typing import Any


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Színek
    GREY = '\033[38;5;248m'
    DARK_ORANGE = '\033[38;5;166m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Háttérszínek
    BACK_GREY = '\033[48;5;237m'
    BACK_BLACK = '\033[40m'
    BACK_RED = '\033[41m'
    BACK_GREEN = '\033[42m'
    BACK_YELLOW = '\033[43m'
    BACK_BLUE = '\033[44m'
    BACK_MAGENTA = '\033[45m'
    BACK_CYAN = '\033[46m'
    BACK_WHITE = '\033[47m'

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Cannot modify attribute {name}")