import pytest

from mastermind.domain.models.code import CodeBuilder


def test_from_code_string_to_data_structure():
    code = "GBBR"
    code_builder = CodeBuilder(code)
    code = code_builder()
    assert code.pegs["G"] == {0}
    assert code.pegs["B"] == {1, 2}
    assert code.pegs["R"] == {3}
