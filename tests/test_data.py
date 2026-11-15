import pandas as pd

from tennisplot.data import _parse_js, _process_matches


FEMALE_JS = '''
var morematchmx = [["19951030", "Canadian Open", "Carpet", "W", "L", "", "", "WC", "Q1", "6-1 6-1", "3", "Anne Miller", "149", "7", "", "R", "19770119", "", "USA", "0", "", "", "", "", "", "", "1995-W-WT-CAN-02A-1995-013"],
["19970307", "Indian Wells", "Hard", "W", "L", "", "", "WC", "Q1", "6-4 6-0", "3", "Alexia Dechaume Balleret", "87", "", "", "R", "19700503", "", "FRA", "0", "", "", "", "", "", "", "1997-W-WT-USA-02A-1997-006"]]
'''

MALE_JS = '''
var morematchmx = [["20010910", "Spain F10", "Hard", "S", "L", "", "", "WC", "R32", "2-6 7-5 6-2", "3", "Guillermo Platel", "731", "", "", "R", "22.264202601", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-M-FU-ESP-10A-2001-002", "", "1", "1"],
["20010917", "Seville CH", "Clay", "C", "W", "", "", "WC", "R32", "6-4 6-4", "3", "Israel Matos Gil", "751", "", "Q", "U", "18.7597535934", "", "ESP", "0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "2001-784-015", "", "1", "1"]]
'''


def test_female_processing():
    matches = _parse_js(FEMALE_JS)
    data = _process_matches(matches, "1981-09-26")

    assert len(data) == 2
    assert data.loc[0, "opponent_name"] == "Anne Miller"
    assert round(data.loc[0, "player_age"], 2) == 14.09
    assert round(data.loc[0, "opponent_age"], 2) == 18.78
    assert data.loc[0, "match_outcome"] == 0


def test_male_processing():
    matches = _parse_js(MALE_JS)
    data = _process_matches(matches, "1986-06-03")

    assert len(data) == 2
    assert data.loc[0, "opponent_name"] == "Guillermo Platel"
    assert round(data.loc[0, "opponent_age"], 2) == 22.26
    assert round(data.loc[1, "opponent_age"], 2) == 18.76
    assert data.loc[1, "match_outcome"] == 1