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

For local development, the package can be installed in editable mode:
```
pip install -e .
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

## Data Processing
Career match data is downloaded from Tennis Abstract.

The package processes female and male player files differently because the Tennis Abstract JavaScript files use different formats.

For female players, the opponent's date of birth is provided in the career match file. The package uses this date to calculate the opponent's age at the time of the match.

For male players, the opponent's age is already included in the career match file.

The processed data includes variables such as:
- match date
- tournament
- match result
- opponent name
- player age
- opponent age
- age difference
- match outcome

The age difference is calculated as:
```
player age - opponent age
```

A positive value means the player was older than their opponent, while a negative value means the player was younger.

## Visualization
The `plot_age_difference()` function produces a scatterplot similar to the visualization reproduced in HW2.

The plot uses:
- x-axis: player's age
- y-axis: player's age minus opponent's age
- blue points: matches the player won
- purple points: matches the player lost

Example:
```
serena = get_player_matches("Serena Williams")
fig = plot_age_difference(serena)
```

## Testing
Automated tests are included in the tests/ directory.

The tests do not contact Tennis Abstract's live servers. Instead, they use the mock female and male JavaScript data provided in the assignment instructions.

To run the tests:
```
pytest
```

The tests verify that:
- female match data is processed correctly
- opponent age is calculated correctly from date of birth
- male opponent ages are processed correctly
- player age is calculated correctly
- match outcomes are encoded correctly

## Package Structure
```
.
├── README.md
├── instructions.md
├── pyproject.toml
├── src/
│   └── tennisplot/
│       ├── __init__.py
│       ├── data.py
│       └── plot.py
└── tests/
    └── test_data.py
```

## Reflections
This assignment helped me understand how code from a reproducible analysis can be generalized into a reusable software package. In HW2, the workflow was written specifically for Serena Williams, but converting it into a package required separating the code into smaller functions that could work for different players.

One important challenge was handling the different formats used by Tennis Abstract for female and male players. Female player files provide opponent birth dates, while male player files provide opponent ages directly. I learned that reusable code often needs to account for differences in how similar data is represented.

I also learned more about package structure and public versus private functions. Instead of having one long script, I separated the workflow into smaller helper functions and exposed only the two functions that a user needs.

Another important part of this assignment was testing. Because the raw data comes from a live website, the tests use local mock data instead of making network requests. This makes the tests faster and more reproducible and avoids depending on whether an external website is available.

Finally, I learned how pyproject.toml allows a Python project to be installed as a package. Installing the package with pip install -e . made it possible to import tennisplot from outside the src directory, which is closer to how another user would actually use the package.

Overall, this assignment taught me how to turn analysis into reusable software packages and how to deal with messy real-world data that is not always formatted consistently.