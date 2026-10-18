import pytest
from arsenal.forensics.decode import ghici_strat, desfa, sparge_xor

def test_ghici_strat():
    assert ghici_strat("414243") == "hex"
    assert ghici_strat("SGVsbG8=") == "base64"
    assert ghici_strat("%20test") == "url"

def test_desfa():
    strat, date = desfa("4142")
    assert strat == "hex"
    assert date == b"AB"

def test_sparge_xor():
    original = b"TEST_FLAG"
    criptat = bytes(b ^ 15 for b in original)
    gasite = sparge_xor(criptat)
    assert any(k == 15 and "TEST_FLAG" in t for k, t in gasite)