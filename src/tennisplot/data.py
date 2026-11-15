import ast
from io import StringIO

import pandas as pd

from urllib.error import HTTPError
from urllib.request import Request, urlopen


def _parse_js(js_text):
    text = js_text.replace("var morematchmx =", "", 1).strip().rstrip(";")
    return ast.literal_eval(text)


def _is_female_format(value):
    return len(value) == 8 and value.isdigit()


def _build_dataframe(matches):
    return pd.DataFrame({
        "date": [row[0] for row in matches],
        "result": [row[4] for row in matches],
        "opponent_name": [row[11] for row in matches],
        "opponent_info": [row[16] for row in matches],
    })


def _clean_dates(data):
    data["date"] = pd.to_datetime(data["date"], format="%Y%m%d")
    return data


def _process_female(data):
    opponent_dob = pd.to_datetime(
        data["opponent_info"],
        format="%Y%m%d",
        errors="coerce",
    )
    data["opponent_age"] = (
        (data["date"] - opponent_dob).dt.days / 365.25
    )
    return data


def _process_male(data):
    data["opponent_age"] = pd.to_numeric(data["opponent_info"])
    return data

def _add_player_age(data, player_dob):
    player_dob = pd.Timestamp(player_dob)
    data["player_age"] = (
        (data["date"] - player_dob).dt.days / 365.25
    )
    return data


def _add_match_columns(data):
    data["age_diff"] = (
        data["player_age"] - data["opponent_age"]
    )
    data["match_outcome"] = data["result"].map({
        "W": 1,
        "L": 0,
    })
    return data


def _process_matches(matches, player_dob):
    data = _build_dataframe(matches)
    data = _clean_dates(data)

    if _is_female_format(data["opponent_info"].iloc[0]):
        data = _process_female(data)
    else:
        data = _process_male(data)

    data = _add_player_age(data, player_dob)
    data = _add_match_columns(data)

    return data

def _normalize_name(player_name):
    name = player_name.strip()

    if " " in name:
        return "".join(word.capitalize() for word in name.split())

    return name[0].upper() + name[1:]

def _download_js(player_name):
    name = _normalize_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    try:
        with urlopen(request) as response:
            return response.read().decode("utf-8")
    except HTTPError as error:
        raise ValueError(f"Player not found: {player_name}") from error

def get_player_matches(player_name, player_dob):
    js_text = _download_js(player_name)
    matches = _parse_js(js_text)
    return _process_matches(matches, player_dob)