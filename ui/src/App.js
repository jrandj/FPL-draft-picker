import React from "react";
import Settings from "./components/Settings.js";
import Pitch from "./components/Pitch.js";
import "./App.css";

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      leagueID: "",
      teamName: "",
    };
  }

  setLeagueID = (newLeagueID) => {
    this.setState({ leagueID: newLeagueID });
  };

  setTeamName = (newTeamName) => {
    this.setState({ teamName: newTeamName });
  };

  getPlayers = () => {
    console.log("getPlayers()");
    this.setState({ leagueID: "", teamName: "" });
    console.log("App.js League ID is: " + this.state.leagueID);
    console.log("App.js teamName is: " + this.state.teamName);
  };

  render() {
    return (
      <div id="app" className="App">
        <div className="Settings">
          <Settings
            setLeagueID={this.setLeagueID}
            setTeamName={this.setTeamName}
            getPlayers={this.getPlayers}
          />
        </div>
        <Pitch />
      </div>
    );
  }
}
