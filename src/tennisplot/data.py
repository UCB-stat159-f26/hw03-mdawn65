import ast
import json
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


def _parse_js(js_text):
    text = js_text.replace("var morematchmx =", "", 1).strip().rstrip(";")
    return ast.literal_eval(text)


def _is_female_format(value):
    return len(value) == 8 and value.isdigit()


def _build_dataframe(matches):
    return pd.DataFrame({
        "date": [row[0] for row in matches],
        "tournament": [row[1] for row in matches],
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
    data["opponent_age"] = pd.to_numeric(
        data["opponent_info"],
        errors="coerce",
    )
    return data


def _add_player_age(data, player_dob):
    player_dob = pd.Timestamp(player_dob)
    data["player_age"] = (
        (data["date"] - player_dob).dt.days / 365.25
    )
    return data


def _add_match_columns(data):
    data["age_diff"] = data["player_age"] - data["opponent_age"]
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
    return _add_match_columns(data)


def _normalize_name(player_name):
    name = player_name.strip()

    if " " in name:
        return "".join(word.capitalize() for word in name.split())

    return name[0].upper() + name[1:]


def _display_name(player_name):
    name = player_name.strip()

    if " " in name:
        return " ".join(word.capitalize() for word in name.split())

    return "".join(
        f" {char}" if char.isupper() and i > 0 else char
        for i, char in enumerate(name)
    )


def _download_url(url):
    request = Request(
        url,
        headers={"User-Agent": "tennisplot/0.1"},
    )
    with urlopen(request) as response:
        return response.read().decode("utf-8")


def _download_js(player_name):
    name = _normalize_name(player_name)
    url = (
        "https://www.tennisabstract.com/"
        f"jsmatches/{name}Career.js"
    )

    try:
        return _download_url(url)
    except HTTPError as error:
        raise ValueError(
            f"Player not found: {player_name}"
        ) from error


def _find_wikidata_id(player_name):
    params = urlencode({
        "action": "wbsearchentities",
        "search": _display_name(player_name),
        "language": "en",
        "format": "json",
        "limit": 1,
    })
    data = json.loads(
        _download_url(
            f"https://www.wikidata.org/w/api.php?{params}"
        )
    )
    if not data["search"]:
        raise ValueError(f"Player not found: {player_name}")
    return data["search"][0]["id"]


def _get_player_dob(player_name):
    entity_id = _find_wikidata_id(player_name)
    url = (
        "https://www.wikidata.org/wiki/"
        f"Special:EntityData/{entity_id}.json"
    )
    data = json.loads(_download_url(url))
    claims = data["entities"][entity_id]["claims"]

    if "P569" not in claims:
        raise ValueError(
            f"Could not determine birth date for: {player_name}"
        )

    value = claims["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
    return pd.to_datetime(value[1:11])


def get_player_matches(player_name):
    js_text = _download_js(player_name)
    player_dob = _get_player_dob(player_name)
    matches = _parse_js(js_text)

    return _process_matches(matches, player_dob)