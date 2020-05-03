# FPL-draft-picker

FPL-draft-picker is a Python application for finding available players in the selected league that have a higher 
projected score than players already in the selected team. This application uses APIs available from 
draft.premierleague.com to obtain player data and then matches against the projections from fantasyfootballscout.co.uk.

## Output

Sample output is shown below:

| web_name      | team_name   | position_name   |   GW31-36 Pts | candidates                                                                                                                                                                                                                                                             |
|---------------|-------------|-----------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Aurier        | TOT         | DEF             |          16.4 | [('Laporte', 18.0)]                                                                                                                                                                                                                                                    |
| Boly          | WOL         | DEF             |          17.2 | [('Laporte', 18.0)]                                                                                                                                                                                                                                                    |
| Doherty       | WOL         | DEF             |          20   | []                                                                                                                                                                                                                                                                     |
| Foster        | WAT         | GKP             |          19   | []                                                                                                                                                                                                                                                                     |
| Gomez         | LIV         | DEF             |          14.5 | [('Laporte', 18.0), ('Mina', 15.5), ('Rüdiger', 15.0), ('Sidibé', 14.7)]                                                                                                                                                                                               |
| Jota          | WOL         | FWD             |          18.4 | []                                                                                                                                                                                                                                                                     |
| King          | BOU         | FWD             |          14.2 | [('Samatta', 14.6)]                                                                                                                                                                                                                                                    |
| Lacazette     | ARS         | FWD             |          13.9 | [('Samatta', 14.6)]                                                                                                                                                                                                                                                    |
| Lloris        | TOT         | GKP             |          16.8 | []                                                                                                                                                                                                                                                                     |
| Maddison      | LEI         | MID             |          18.4 | [('David Silva', 18.6)]                                                                                                                                                                                                                                                |
| Pépé          | ARS         | MID             |          18.5 | [('David Silva', 18.6)]                                                                                                                                                                                                                                                |
| Saint-Maximin | NEW         | MID             |          15.8 | [('David Silva', 18.6), ('Sigurdsson', 17.9), ('Bowen', 16.0)]                                                                                                                                                                                                         |
| Stephens      | SOU         | DEF             |          11.6 | [('Laporte', 18.0), ('Mina', 15.5), ('Rüdiger', 15.0), ('Sidibé', 14.7), ('James', 13.8), ('Holgate', 13.6), ('Cresswell', 13.3), ('Ogbonna', 13.2), ('Kiko Femenía', 13.1), ('Cathcart', 13.0), ('Kabasele', 12.6), ('Diop', 12.5), ('Aké', 12.4), ('Webster', 12.0)] |
| Trossard      | BHA         | MID             |          14.9 | [('David Silva', 18.6), ('Sigurdsson', 17.9), ('Bowen', 16.0), ('Buendía', 15.8), ('Hughes', 15.1)]                                                                                                                                                                    |
| Westwood      | BUR         | MID             |          13.6 | [('David Silva', 18.6), ('Sigurdsson', 17.9), ('Bowen', 16.0), ('Buendía', 15.8), ('Hughes', 15.1), ('Almirón', 14.9), ('Pereyra', 14.8), ('Shelvey', 14.4), ('Noble', 14.3)]                                                                                          |

536 active players have been matched to 533 projections.

The previous line shows how many players from draft.premierleague.com could be matched to projections from fantasyfootballscout.co.uk.

## Getting Started

### Pre-requisites
* Python 3.8

### Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install FPL-draft-picker. Using Windows Command Prompt:

1. Create a virtual environment
    ```bash
    py -m venv venv
    ```
2. Activate virtual environment
    ```bash
    "venv/Scripts/activate.bat"
    ```
3. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```
   
### Usage
Run the script from the command line.

```python
app.py -myLeague <value> -myTeamName <value> -ffslogin <value> -ffspassword <value>
```