# HW3: R/Python Package

## Overview

This repository contains a Python package for retrieving and visualizing tennis career match data from tennis abstract.

The package builds on HW1 and HW2.

The package provides two public functions:
- `get_player_matches()` retrieves and processes a player's career match data.
- `plot_age_difference()` produces a scatterplot showing the player's age relative to the ages of their opponents.

## Installation

The package can be installed directly from GitHub using:
```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-mdawn65.git
```

## Usage

Import the two public functions:
```
from tennisplot import get_player_matches, plot_age_difference
```

### For Serena Williams
```
serena = get_player_matches("Serena Williams")
plot_age_difference(serena)
```

The player name can also be written in different formats:
```
serena = get_player_matches("serena williams")
serena = get_player_matches("SerenaWilliams")
```

### For Rafael Nadal
```
nadal = get_player_matches("Rafael Nadal")
plot_age_difference(nadal)
```

### For Invalid Players
If the player cannot be found, the function returns a meaningful error:
```
get_player_matches("GastonSanchez")
```
Which raises:
```
ValueError: Player not found: GastonSanchez
```

