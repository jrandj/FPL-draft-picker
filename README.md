# FPL-draft-picker

FPL-draft-picker is a Python application for finding available players in the selected league that have a higher 
projected score than players already in the selected team.

## Output

| web_name      | team_name   | position_name   |   GW31-36 Pts |   GW31 |   GW32 |   GW33 |   GW34 |   GW35 |   GW36 | candidates                                                                                                                                                                                                                                                             |
|---------------|-------------|-----------------|---------------|--------|--------|--------|--------|--------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Aurier        | TOT         | DEF             |          16.4 |      0 |    3.2 |    3.6 |    3.2 |    3   |    3.4 | [('Laporte', 18.0)]                                                                                                                                                                                                                                                    |
| Boly          | WOL         | DEF             |          17.2 |      0 |    3.5 |    3.3 |    3.2 |    3.7 |    3.5 | [('Laporte', 18.0)]                                                                                                                                                                                                                                                    |
| Doherty       | WOL         | DEF             |          20   |      0 |    4.1 |    3.9 |    3.7 |    4.2 |    4   | []                                                                                                                                                                                                                                                                     |
| Foster        | WAT         | GKP             |          19   |      0 |    3.9 |    3.3 |    4.1 |    4.2 |    3.6 | []                                                                                                                                                                                                                                                                     |
| Gomez         | LIV         | DEF             |          14.5 |      0 |    1.6 |    3.6 |    3.1 |    3.7 |    2.5 | [('Laporte', 18.0), ('Mina', 15.5), ('Rüdiger', 15.0), ('Sidibé', 14.7)]                                                                                                                                                                                               |
| Jota          | WOL         | FWD             |          18.4 |      0 |    4   |    3.8 |    3.3 |    3.8 |    3.6 | []                                                                                                                                                                                                                                                                     |
| King          | BOU         | FWD             |          14.2 |      0 |    2.6 |    2.5 |    3.3 |    3.2 |    2.5 | [('Samatta', 14.6)]                                                                                                                                                                                                                                                    |
| Lacazette     | ARS         | FWD             |          13.9 |      0 |    3.5 |    2.5 |    2.8 |    2.6 |    2.5 | [('Samatta', 14.6)]                                                                                                                                                                                                                                                    |
| Lloris        | TOT         | GKP             |          16.8 |      0 |    3.3 |    3.5 |    3.3 |    3.2 |    3.4 | []                                                                                                                                                                                                                                                                     |
| Maddison      | LEI         | MID             |          18.4 |      0 |    2.5 |    4   |    3.5 |    4.1 |    4.2 | [('David Silva', 18.6)]                                                                                                                                                                                                                                                |
| Pépé          | ARS         | MID             |          18.5 |      0 |    4.8 |    3.3 |    3.7 |    3.4 |    3.2 | [('David Silva', 18.6)]                                                                                                                                                                                                                                                |
| Saint-Maximin | NEW         | MID             |          15.8 |      0 |    3.3 |    3.7 |    2.4 |    3.1 |    3.3 | [('David Silva', 18.6), ('Sigurdsson', 17.9), ('Bowen', 16.0)]                                                                                                                                                                                                         |
| Stephens      | SOU         | DEF             |          11.6 |      0 |    2.5 |    1.6 |    2.3 |    2   |    3.2 | [('Laporte', 18.0), ('Mina', 15.5), ('Rüdiger', 15.0), ('Sidibé', 14.7), ('James', 13.8), ('Holgate', 13.6), ('Cresswell', 13.3), ('Ogbonna', 13.2), ('Kiko Femenía', 13.1), ('Cathcart', 13.0), ('Kabasele', 12.6), ('Diop', 12.5), ('Aké', 12.4), ('Webster', 12.0)] |
| Trossard      | BHA         | MID             |          14.9 |      0 |    3.2 |    3.4 |    2.7 |    2.7 |    3   | [('David Silva', 18.6), ('Sigurdsson', 17.9), ('Bowen', 16.0), ('Buendía', 15.8), ('Hughes', 15.1)]                                                                                                                                                                    |
| Westwood      | BUR         | MID             |          13.6 |      0 |    2.9 |    3   |    2.8 |    2.1 |    2.8 | [('David Silva', 18.6), ('Sigurdsson', 17.9), ('Bowen', 16.0), ('Buendía', 15.8), ('Hughes', 15.1), ('Almirón', 14.9), ('Pereyra', 14.8), ('Shelvey', 14.4), ('Noble', 14.3)]                                                                                          |

536 active players have been matched to 533 projections.

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
Update the below values in app.py accordingly.

```python
    myLeague = 48188
    myTeamName = "wearetherunnersup"
```

Add credentials to http://members.fantasyfootballscout.co.uk/ in a config.py in your local copy of the repository.

```python
    login = {
        'username' : <VALUE>,
        'password' : <VALUE>
    }
```