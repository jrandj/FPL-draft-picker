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
      candidates: [],
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

  findBestFormationOnLoad = () => {
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
      .slice(0, 3);

    var midfielders = this.newPlayers
      .filter((obj) => obj.element_type === 3)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 3);

    var attackers = this.newPlayers
      .filter((obj) => obj.element_type === 4)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 1);

    let selected = goalkeepers.concat(defenders, midfielders, attackers);

    // choose the skeleton team based on ICT index
    this.newPlayers.forEach((obj) => {
      let player = selected.find((ee) => ee.id === obj.id);
      if (player) {
        obj.selected = true;
      }
    });

    // choose "the rest" of the team (need 3 more outfield players who aren't already selected)
    var theRest = this.newPlayers
      .filter((obj) => obj.selected === false && obj.element_type !== 1)
      .sort((a, b) => b.ict_index - a.ict_index)
      .slice(0, 3);

    selected = selected.concat(theRest);

    this.newPlayers.forEach((obj) => {
      let player = selected.find((ee) => ee.id === obj.id);
      if (player) {
        obj.selected = true;
      }
    });

    const newFormation =
      String(
        this.newPlayers.filter(
          (obj) => obj.selected === true && obj.element_type === 2
        ).length
      ) +
      String(
        this.newPlayers.filter(
          (obj) => obj.selected === true && obj.element_type === 3
        ).length
      ) +
      String(
        this.newPlayers.filter(
          (obj) => obj.selected === true && obj.element_type === 4
        ).length
      );

    this.setState({
      myPlayers: this.newPlayers,
      formation: newFormation,
    });
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
          // find entry_id from entry_name
          entryId: res.data.league_entries.find(
            (x) => x.entry_name === this.state.teamName
          ).entry_id,
        });
        return axios.get(elementsURL);
      })
      .then((res) => {
        // console.log("res is " + JSON.stringify(res)),
        this.setState(
          {
            // find players by entry_id
            myPlayersByEntryID: res.data.element_status.filter(
              (x) => x.owner === this.state.entryId
            ),
            unownedPlayersByEntryID: res.data.element_status.filter(
              (x) => x.owner === null
            ),
          }
          // () => {
          //   console.log("res is " + JSON.stringify(res.data.element_status));
          // }
        );
        return axios.get(bootstrapURL);
      })
      .then((res) => {
        this.setState(
          {
            myPlayers: res.data.elements.filter((el) => {
              return this.state.myPlayersByEntryID.some((f) => {
                return f.element === el.id;
              });
            }),
            unownedPlayers: res.data.elements.filter((el) => {
              return this.state.unownedPlayersByEntryID.some((f) => {
                return f.element === el.id;
              });
            }),
          },
          () => {
            this.findBestFormationOnLoad();
            this.addCandidates();
          }
        );
      })
      .catch((error) => console.log(error.response));
  };

  addCandidates = () => {
    // console.log("unownedPlayers: " + JSON.stringify(this.state.unownedPlayers));
    let newPlayers = this.state.myPlayers;
    this.newPlayers.forEach((obj, index) => {
      let candidates = this.state.unownedPlayers.filter(
        (ee) =>
          ee.element_type === obj.element_type && ee.ict_index > obj.ict_index
      );
      // console.log("candidates: " + JSON.stringify(candidates));
      if (candidates) {
        newPlayers[index].candidates = candidates;
      }
    });
    // console.log(
    //   "newPlayers after adding candidates from unowned: " +
    //     JSON.stringify(newPlayers)
    // );
    this.setState(
      {
        myPlayers: newPlayers,
      }
      // () => {
      //   console.log(
      //     "CANDIDATES UPDATED: " + JSON.stringify(this.state.myPlayers)
      //   );
      // }
    );
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
          />
        </div>
        {/* {
          (console.log("players: " + this.state.myPlayers),
          this.state.myPlayers.map((player) => <Candidates></Candidates>))
        } */}
        <Pitch
          myPlayers={this.state.myPlayers}
          setSelectedPlayer={this.setSelectedPlayer}
        />
      </div>
    );
  }
}
