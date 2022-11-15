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
    };
  }

  setLeagueID = (newLeagueID) => {
    this.setState({ leagueID: newLeagueID });
  };

  setTeamName = (newTeamName) => {
    this.setState({ teamName: newTeamName });
  };

  getPlayers = () => {
    // console.log("getPlayers()");
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
              // return f.userid === el.userid && f.projectid === el.projectid;
            }),
          },
          () => {
            console.log(
              "These are my players: " + JSON.stringify(this.state.players)
            );
            console.log(
              "These are my temp: " +
                JSON.stringify({
                  ...this.state.playersByEntryID,
                  ...res.data.elements,
                })
            );
          }
        );
      })
      .catch((error) => console.log(error.response));

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
