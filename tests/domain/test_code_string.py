import pytest

from mastermind.domain.models.code import CodeBuilder
from mastermind.domain.models.exceptions import ColorNotSupportedError


def test_from_code_string_to_data_structure():
    code = "GBBR"
    code_builder = CodeBuilder(code)
    code = code_builder()
    assert code.pegs["G"] == {0}
    assert code.pegs["B"] == {1, 2}
    assert code.pegs["R"] == {3}


def test_support_lowercase_colors():
    code = "gbbr"
    code_builder = CodeBuilder(code)
    code = code_builder()
    assert str(code) == "GBBR"


def test_color_not_supported_in_builder():
    code = "X"
    with pytest.raises(ColorNotSupportedError):
        CodeBuilder(code)
