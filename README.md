# FPL-draft-picker

FPL-draft-picker is a Python application for finding available players in the selected league that have a higher 
projected score than players already in the selected team. This application uses APIs available from 
`draft.premierleague.com` to obtain player data and then matches against the projections from `fantasyfootballscout.co.uk`.

## Output

**Team Suggestions - Projected Points**
![figure2](res/player_suggestions.JPG)

**Team Suggestions - ICT Index**
![figure2](res/ict_suggestions.JPG)

**Formation Suggestions**
![figure3](res/formation_suggestions.JPG)

**Fixture Prediction**
![figure1](res/fixture_prediction.JPG)

## Getting Started

### Pre-requisites
* Python 3.8

### Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install FPL-draft-picker. Using Windows Command Prompt:

1. Create a virtual environment:
    ```bash
    py -m venv venv
    ```

2. Activate virtual environment:
    ```bash
    "venv/Scripts/activate.bat"
    ```

3. Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

To check for outdated packages run `pip3 list --outdated`.
   
### Usage
Run the script from the command line:

```python
fpldraft.py -leagueID <value> -teamName <value> -fantasyFootballScoutUsername <value> -fantasyFootballScoutPassword <value>
```
Values for the parameters can be found as per the below:
* leagueID - This can be found by inspecting the HTTP GET request to the details endpoint (e.g. `draft.premierleague.com/api/league/<value>/details`) from the League tab in your browsers developer console.
* teamName - The name of the team as shown at `draft.premierleague.com`.
* fantasyFootballScoutUsername - Fantasy Football Scout username.
* fantasyFootballScoutPassword - Fantasy Football Scout password.