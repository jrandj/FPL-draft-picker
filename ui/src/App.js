import React from "react";
import axios from "axios";
import Settings from "./components/Settings.js";
import Pitch from "./components/Pitch.js";
import "./App.css";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      entryId: "",
      playersByEntryID: [],
      players: [],
      leagueID: "",
      teamName: "",
      teamID: "",
      formation: "442",
    };
  }

  setLeagueID = (newLeagueID) => {
    this.setState({ leagueID: newLeagueID });
  };

  setTeamName = (newTeamName) => {
    this.setState({ teamName: newTeamName });
  };

  setFormation = (newFormation) => {
    this.setState({ formation: newFormation }, () => {
      this.addPlayersToFormation();
    });
  };

  addPlayersToFormation = () => {
    this.newPlayers = this.state.players.map((v) => ({
      ...v,
      selected: false,
    }));

    var goalkeepers = this.newPlayers
      .filter((obj) => obj.element_type === 1)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 1);

    var defenders = this.newPlayers
      .filter((obj) => obj.element_type === 2)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, parseInt(this.state.formation.charAt(0)));

    var midfielders = this.newPlayers
      .filter((obj) => obj.element_type === 3)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, parseInt(this.state.formation.charAt(1)));

    var attackers = this.newPlayers
      .filter((obj) => obj.element_type === 4)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, parseInt(this.state.formation.charAt(2)));

    const selected = goalkeepers.concat(defenders, midfielders, attackers);

    this.newPlayers.forEach((obj) => {
      let player = selected.find((ee) => ee.id === obj.id);
      if (player) {
        obj.selected = true;
      }
    });

    this.setState(
      {
        players: this.newPlayers,
      },
      () => {
        // console.log("State is now: " + JSON.stringify(this.state.players));
      }
    );
  };

  getPlayers = () => {
    const detailsURL =
      "https://draft.premierleague.com/api/league/" +
      this.state.leagueID +
      "/details";
    const elementsURL =
      "https://draft.premierleague.com/api/league/" +
      this.state.leagueID +
      "/element-status";
    const bootstrapURL = "https://draft.premierleague.com/api/bootstrap-static";

    axios
      .get(detailsURL)
      .then((res) => {
        this.setState({
          entryId: res.data.league_entries.find(
            (x) => x.entry_name === this.state.teamName
          ).entry_id,
        });
        return axios.get(elementsURL);
      })
      .then((res) => {
        this.setState({
          playersByEntryID: res.data.element_status.filter(
            (x) => x.owner === this.state.entryId
          ),
        });
        return axios.get(bootstrapURL);
      })
      .then((res) => {
        this.setState(
          {
            players: res.data.elements.filter((el) => {
              return this.state.playersByEntryID.some((f) => {
                return f.element === el.id;
              });
            }),
          },
          () => {
            this.addPlayersToFormation();
          }
        );
      })
      .catch((error) => console.log(error.response));
  };

  render() {
    return (
      <div id="app" className="App">
        <div className="Settings">
          <Settings
            setLeagueID={this.setLeagueID}
            setTeamName={this.setTeamName}
            setFormation={this.setFormation}
            getPlayers={this.getPlayers}
            formation={this.state.formation}
          />
        </div>
        <Pitch players={this.state.players} />
      </div>
    );
  }
}
