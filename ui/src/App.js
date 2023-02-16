import React from "react";
import axios from "axios";
import ControlPanel from "./components/ControlPanel.js";
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
      formation: "Highest Rated",
      formations: ["343", "352", "532", "541", "433", "442", "451"],
      selectedPlayer: "",
      pointsCandidates: "",
      projectionsResponse: "",
      rankMethod: "NGW Pts Projection",
      rankMethods: ["ICT Index", "NGW Pts Projection"],
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

  setRankMethod = (newRankMethod) => {
    this.setState({ rankMethod: newRankMethod }, () => {
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
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
      .slice(0, 1);

    var defenders = this.newPlayers
      .filter((obj) => obj.element_type === 2)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
      .slice(0, parseInt(this.state.formation.charAt(0)));

    var midfielders = this.newPlayers
      .filter((obj) => obj.element_type === 3)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
      .slice(0, parseInt(this.state.formation.charAt(1)));

    var attackers = this.newPlayers
      .filter((obj) => obj.element_type === 4)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
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
    console.log(
      "about to find formation with players: " + JSON.stringify(myPlayers)
    );
    let newPlayers = myPlayers.map((v) => ({
      ...v,
      selected: false,
    }));

    var goalkeepers = newPlayers
      .filter((obj) => obj.element_type === 1)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
      .slice(0, 1);

    var defenders = newPlayers
      .filter((obj) => obj.element_type === 2)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
      .slice(0, 3);

    console.log("Defenders are: " + JSON.stringify(defenders));

    var midfielders = newPlayers
      .filter((obj) => obj.element_type === 3)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
      .slice(0, 3);

    var attackers = newPlayers
      .filter((obj) => obj.element_type === 4)
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
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
      .sort((a, b) => {
        if (this.state.rankMethod === "NGW Pts Projection")
          return b.ngw_pts_projection - a.ngw_pts_projection;
        else if (this.state.rankMethod === "ICT Index")
          return b.ict_index - a.ict_index;
      })
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
    const detailsURL =
      "http://127.0.0.1:8000/app/details/" + this.state.leagueID;
    const elementsURL =
      "http://127.0.0.1:8000/app/elements/" + this.state.leagueID;
    const bootstrapURL = "http://127.0.0.1:8000/app/bootstrap";
    const projectionsURL =
      "http://127.0.0.1:8000/app/candidates/" +
      this.state.leagueID +
      "/" +
      this.state.teamName;

    var myPlayers,
      unownedPlayers,
      myPlayersByEntryID,
      unownedPlayersByEntryID,
      entryId;

    axios
      .get(detailsURL)
      .then((res) => {
        entryId = res.data.league_entries.find(
          (x) => x.entry_name === this.state.teamName
        ).entry_id;
        return axios.get(elementsURL);
      })
      .then((res) => {
        myPlayersByEntryID = res.data.element_status.filter(
          (x) => x.owner === entryId
        );
        unownedPlayersByEntryID = res.data.element_status.filter(
          (x) => x.owner === null
        );
        // elementsURLRes = res;
        return axios.get(bootstrapURL);
      })
      .then((res) => {
        // find matching players
        myPlayers = res.data.elements.filter((el) => {
          return myPlayersByEntryID.some((f) => {
            return f.element === el.id;
          });
        });
        unownedPlayers = res.data.elements.filter((el) => {
          return unownedPlayersByEntryID.some((f) => {
            return f.element === el.id;
          });
        });
        return axios.get(projectionsURL);
      })
      .then((res) => {
        myPlayers.forEach((obj, index) => {
          let candidates = res.data.filter((ee) => obj.id === ee.id);
          if (candidates) {
            myPlayers[index].ngw_pts_projection =
              candidates[0]["NGW Pts Projection"];
            myPlayers[index].candidates = candidates[0]["NGW Candidates"];
          }
        });

        var results = this.findBestFormationOnLoad(myPlayers);
        // this.addPlayersToFormation();

        this.setState(
          {
            myPlayers: results[0],
            unownedPlayers: unownedPlayers,
            entryId: entryId,
            myPlayersByEntryID: myPlayersByEntryID,
            unownedPlayersByEntryID: unownedPlayersByEntryID,
            formation: results[1],
          },
          () => {
            console.log(
              "Setting myPlayers state: " + JSON.stringify(results[1])
            );
            console.log(
              "Setting unownedPlayers state: " + JSON.stringify(unownedPlayers)
            );
          }
        );
      })
      .catch((error) => console.log(error.response));
  };

  render() {
    return (
      <div id="app" className="App">
        <div className="ControlPanel">
          <ControlPanel
            setLeagueID={this.setLeagueID}
            setTeamName={this.setTeamName}
            setFormation={this.setFormation}
            setRankMethod={this.setRankMethod}
            getPlayers={this.getPlayers}
            formation={this.state.formation}
            formations={this.state.formations}
            rankMethod={this.state.rankMethod}
            rankMethods={this.state.rankMethods}
            myPlayers={this.state.myPlayers}
            unownedPlayers={this.state.unownedPlayers}
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
