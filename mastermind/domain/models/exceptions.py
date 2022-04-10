class InputException(Exception):
    pass


class ColorNotSupportedError(InputException):
    pass


class GameNotFound(InputException):
    pass


class BadGuessLength(InputException):
    pass


class GameAlreadySolvedError(InputException):
    pass
