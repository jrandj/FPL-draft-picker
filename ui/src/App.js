import React from "react";
import Search from "./components/Search.js";
import Submit from "./components/Submit.js";
import Pitch from "./components/Pitch.js";
// import Footer from "./components/Footer.js";
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
    console.log("App.js League ID is: " + this.state.leagueID);
  };

  setTeamName = (newTeamName) => {
    this.setState({ teamName: newTeamName });
    console.log("App.js teamName is: " + this.state.teamName);
  };

  getPlayers = () => {
    console.log("getPlayers()");
    console.log("App.js League ID is: " + this.state.leagueID);
    console.log("App.js teamName is: " + this.state.teamName);
  };

  render() {
    return (
      <div id="app" className="App">
        <div className="Settings">
          <Search
            setLeagueID={this.setLeagueID}
            setTeamName={this.setTeamName}
          />
          <Submit
            getPlayers={this.getPlayers}
            // setLeagueID={this.setLeagueID}
            // setTeamName={this.setTeamName}
          />
        </div>
        <Pitch />
      </div>
    );
  }
}
