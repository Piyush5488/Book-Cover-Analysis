import pytest

from main import start


def test_invalid_format():
    val = start('2', 'images/Book-Cover1.jpeg')
    assert val == "Invalid Format Selected"
    return


def test_incorrect_file_path():
    val = start('0', 'images/he-he')
    assert val == "Incorrect File Path Provided"
    return


def test_incorrect_directory_path():
    val = start('1', 'image')
    assert val == "Incorrect Directory Path Provided"
    return


def test_single_file():
    val = start('0', 'images/Book-Cover5.jpeg')
    assert val[0] == "CHRISTMAS CAROL"
    assert val[1] == "CHARLES DICKENS"
    assert val[2] == "No Publisher Detected"
    assert val[3] == "No ISBN Number Detected"
    return


def test_directory():
    val = start('1', 'images/dir1')
    assert val[0][0] == "Automata and Computability"
    assert val[0][1] == "DEXTER (. KozEN"
    assert val[0][2] == "Springer"
    assert val[0][3] == "No ISBN Number Detected"

    assert val[1][0] == "Mathematics For Class XII Volume"
    assert val[1][1] == "RD: Sharma"
    assert val[1][2] == "DHANPAT RAI PUBLICATIONS"
    assert val[1][3] == "No ISBN Number Detected"
    return
