from mastermind.domain.models.code import CodeBuilder
from mastermind.domain.models.white_pegs import WhitePegs


def test_white_pegs_solution():
    code = CodeBuilder("RGGB")()
    guess = CodeBuilder("RGGB")()

    white_pegs = WhitePegs(code, guess).count()
    assert white_pegs == 0


def test_white_pegs_one_black_peg():
    code = CodeBuilder("RGGG")()
    guess = CodeBuilder("RYYY")()

    white_pegs = WhitePegs(code, guess).count()
    assert white_pegs == 0


def test_white_pegs_more_candidates_than_max():
    code = CodeBuilder("RRGG")()
    guess = CodeBuilder("YYRY")()

    white_pegs = WhitePegs(code, guess).count()
    assert white_pegs == 1


def test_white_pegs_max_greater_than_candidates():
    code = CodeBuilder("RGGG")()
    guess = CodeBuilder("YRRR")()

    white_pegs = WhitePegs(code, guess).count()
    assert white_pegs == 1


def test_white_pegs_one_black_one_white():
    code = CodeBuilder("RGRG")()
    guess = CodeBuilder("RRYY")()

    white_pegs = WhitePegs(code, guess).count()
    assert white_pegs == 1


def test_white_pegs_different_colors():
    code = CodeBuilder("RGGG")()
    guess = CodeBuilder("GRYY")()

    white_pegs = WhitePegs(code, guess).count()
    assert white_pegs == 2
