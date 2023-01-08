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
      myPlayersByEntryID: [],
      myPlayers: [],
      unownedPlayersByEntryID: [],
      unownedPlayers: [],
      leagueID: "",
      teamName: "",
      teamID: "",
      formation: "TBC",
      formations: ["343", "352", "532", "541", "433", "442", "451"],
      selectedPlayer: "",
    };
  }
  setSelectedPlayer = (player) => {
    this.setState({ selectedPlayer: player }, () => {
      console.log("Selected player is: " + JSON.stringify(player));
    });
  };

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
    this.newPlayers = this.state.myPlayers.map((v) => ({
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
        myPlayers: this.newPlayers,
      },
      () => {
        // console.log("State is now: " + JSON.stringify(this.state.myPlayers));
      }
    );
  };

  findBestFormationOnLoad = (myPlayers) => {
    let newPlayers = myPlayers.map((v) => ({
      ...v,
      selected: false,
    }));

    var goalkeepers = newPlayers
      .filter((obj) => obj.element_type === 1)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 1);

    var defenders = newPlayers
      .filter((obj) => obj.element_type === 2)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 3);

    var midfielders = newPlayers
      .filter((obj) => obj.element_type === 3)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 3);

    var attackers = newPlayers
      .filter((obj) => obj.element_type === 4)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 1);

    let selected = goalkeepers.concat(defenders, midfielders, attackers);

    // choose the skeleton team based on ICT index
    newPlayers.forEach((obj) => {
      let player = selected.find((ee) => ee.id === obj.id);
      if (player) {
        obj.selected = true;
      }
    });

    // choose "the rest" of the team (need 3 more outfield players who aren't already selected)
    var theRest = newPlayers
      .filter((obj) => obj.selected === false && obj.element_type !== 1)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 3);

    selected = selected.concat(theRest);

    newPlayers.forEach((obj) => {
      let player = selected.find((ee) => ee.id === obj.id);
      if (player) {
        obj.selected = true;
      }
    });

    const newFormation =
      String(
        newPlayers.filter(
          (obj) => obj.selected === true && obj.element_type === 2
        ).length
      ) +
      String(
        newPlayers.filter(
          (obj) => obj.selected === true && obj.element_type === 3
        ).length
      ) +
      String(
        newPlayers.filter(
          (obj) => obj.selected === true && obj.element_type === 4
        ).length
      );

    return [newPlayers, newFormation];
  };

  getPlayers = () => {
    // const detailsURL =
    //   "https://draft.premierleague.com/api/league/" +
    //   this.state.leagueID +
    //   "/details";
    const detailsURL =
      "http://127.0.0.1:8000/app/details/" + this.state.leagueID;
    // const elementsURL =
    //   "https://draft.premierleague.com/api/league/" +
    //   this.state.leagueID +
    //   "/element-status";
    const elementsURL =
      "http://127.0.0.1:8000/app/elements/" + this.state.leagueID;
    // const bootstrapURL = "https://draft.premierleague.com/api/bootstrap-static";
    const bootstrapURL = "http://127.0.0.1:8000/app/boostrap";

    axios
      .get(detailsURL)
      .then((res) => {
        this.setState({
          // find entry_id from entry_name
          entryId: res.data.league_entries.find(
            (x) => x.entry_name === this.state.teamName
          ).entry_id,
        });
        return axios.get(elementsURL);
      })
      .then((res) => {
        this.setState({
          // find players by entry_id
          myPlayersByEntryID: res.data.element_status.filter(
            (x) => x.owner === this.state.entryId
          ),
          unownedPlayersByEntryID: res.data.element_status.filter(
            (x) => x.owner === null
          ),
        });
        return axios.get(bootstrapURL);
      })
      .then((res) => {
        let myPlayers = res.data.elements.filter((el) => {
          return this.state.myPlayersByEntryID.some((f) => {
            return f.element === el.id;
          });
        });
        let unownedPlayers = res.data.elements.filter((el) => {
          return this.state.unownedPlayersByEntryID.some((f) => {
            return f.element === el.id;
          });
        });
        let results = this.findBestFormationOnLoad(myPlayers);
        let newPlayers = this.addCandidates(results[0], unownedPlayers);

        this.setState({ myPlayers: newPlayers, formation: results[1] }, () => {
          console.log("Setting player state: " + JSON.stringify(newPlayers));
        });
      })
      .catch((error) => console.log(error.response));
  };

  addCandidates = (pnewPlayers, unownedPlayers) => {
    let newPlayers = pnewPlayers;
    newPlayers.forEach((obj, index) => {
      let candidates = unownedPlayers.filter(
        (ee) =>
          ee.element_type === obj.element_type && ee.ict_index > obj.ict_index
      );
      if (candidates) {
        newPlayers[index].candidates = candidates;
      }
    });
    return newPlayers;
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
            formations={this.state.formations}
            myPlayers={this.state.myPlayers}
            selectedPlayer={this.state.selectedPlayer}
          />
        </div>
        <Pitch
          myPlayers={this.state.myPlayers}
          setSelectedPlayer={this.setSelectedPlayer}
        />
      </div>
    );
  }
}
