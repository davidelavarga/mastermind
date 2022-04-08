from mastermind.domain.models.black_pegs import BlackPegs
from mastermind.domain.models.code import CodeBuilder


def test_black_pegs_solution():
    code = CodeBuilder("RGGB")()
    guess = CodeBuilder("RGGB")()

    black_pegs = BlackPegs(code, guess).count()
    assert black_pegs == 4


def test_black_pegs_no_pegs():
    code = CodeBuilder("RGGB")()
    guess = CodeBuilder("YYYY")()

    black_pegs = BlackPegs(code, guess).count()
    assert black_pegs == 0


def test_black_pegs_partial_solution():
    code = CodeBuilder("RGGB")()
    guess = CodeBuilder("RGYY")()

    black_pegs = BlackPegs(code, guess).count()
    assert black_pegs == 2
