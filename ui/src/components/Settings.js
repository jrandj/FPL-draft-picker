import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Candidate from "./Candidate";
import "bootstrap/dist/css/bootstrap.min.css";

export default class Settings extends React.Component {
  constructor(props) {
    super(props);
    this.leagueIDChangeHandlerRef = React.createRef();
    this.teamNameChangeHandlerRef = React.createRef();
    // this.state = {
    //   selectedPlayer: "",
    // };
  }
  render() {
    const leagueIDChangeHandler = (event) => {
      this.props.setLeagueID(event.target.value);
    };
    const teamNameChangeHandler = (event) => {
      this.props.setTeamName(event.target.value);
    };
    const onGetMyTeam = () => {
      this.props.getPlayers();
      // this.leagueIDChangeHandlerRef.current.value = "";
      // this.teamNameChangeHandlerRef.current.value = "";
    };
    const onSetFormation = (event) => {
      this.props.setFormation(event);
    };

    return (
      <div className="Inputs">
        <div>
          <input
            className="Search-League-ID"
            value={this.props.leagueID}
            type="search"
            onChange={leagueIDChangeHandler}
            placeholder="Enter your League ID..."
            ref={this.leagueIDChangeHandlerRef}
            autoFocus
          />
          <input
            className="Search-Team-Name"
            value={this.props.teamName}
            type="search"
            onChange={teamNameChangeHandler}
            placeholder="Enter your Team Name..."
            ref={this.teamNameChangeHandlerRef}
            autoFocus
          />
        </div>
        <p
          style={{
            margin: 0,
            padding: 0,
            fontWeight: "bold",
          }}
        >
          Candidates (shown on player selection)
        </p>
        <div className="Candidates">
          {/* {console.log("In Settings with selectedPlayer: " + JSON.stringify(this.props.selectedPlayer))} */}
          {this.props.selectedPlayer &&
            (console.log(
              "In Candidates with selected player.candidates: " +
                JSON.stringify(this.props.selectedPlayer.candidates)
            ),
            console.log(
              "unownedPlayers: " + JSON.stringify(this.props.unownedPlayers)
            ),
            this.props.selectedPlayer.candidates.map((player) => (
              <Candidate
                player={player}
                unownedPlayers={this.props.unownedPlayers}
              ></Candidate>
            )))}
        </div>
        <div className="Submit">
          <DropdownButton
            className="Dropdown"
            onSelect={onSetFormation}
            title={`Formation: ${this.props.formation}`}
          >
            {this.props.formations.map((e) => (
              <Dropdown.Item key={e} eventKey={e}>
                {e}
              </Dropdown.Item>
            ))}
          </DropdownButton>
          {/* <button className="PimpMyTeam" onClick={onGetMyTeam}>
            Pimp my Team
          </button> */}
          <button className="GetMyTeam" onClick={onGetMyTeam}>
            Get my Team
          </button>
        </div>
      </div>
    );
  }
}
