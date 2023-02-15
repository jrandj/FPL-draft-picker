import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import CandidatesTable from "./CandidatesTable";
import "bootstrap/dist/css/bootstrap.min.css";

export default class ControlPanel extends React.Component {
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
    const onSetRankMethod = (event) => {
      this.props.setRankMethod(event);
    };

    return [
      <div className="Inputs">
        <div className="Input">
          <label>
            <b>League ID: </b>
          </label>
          <input
            className="Input-League-ID"
            value={this.props.leagueID}
            type="text"
            onChange={leagueIDChangeHandler}
            placeholder="Enter your League ID..."
            ref={this.leagueIDChangeHandlerRef}
            autoFocus
          />
        </div>
        <div className="Input">
          <label>
            <b>Team: </b>
          </label>
          <input
            className="Input-Team-Name"
            value={this.props.teamName}
            type="text"
            onChange={teamNameChangeHandler}
            placeholder="Enter your Team Name..."
            ref={this.teamNameChangeHandlerRef}
            autoFocus
          />
        </div>
        <div className="DropDown">
          <label>
            <b>Formation: </b>
          </label>
          <DropdownButton
            // className="DropdownButton"
            onSelect={onSetFormation}
            title={`${this.props.formation}`}
          >
            {this.props.formations.map((e) => (
              <Dropdown.Item key={e} eventKey={e}>
                {e}
              </Dropdown.Item>
            ))}
          </DropdownButton>
        </div>
        <div className="DropDown">
          <label>
            <b>Rank Method: </b>
          </label>
          <DropdownButton
            // className="DropdownButton"
            onSelect={onSetRankMethod}
            title={`${this.props.rankMethod}`}
          >
            {this.props.rankMethods.map((e) => (
              <Dropdown.Item key={e} eventKey={e}>
                {e}
              </Dropdown.Item>
            ))}
          </DropdownButton>
        </div>
      </div>,
      <div className="Candidates">
        {this.props.selectedPlayer &&
          (console.log(
            "In Candidates with selected player.candidates: " +
              JSON.stringify(this.props.selectedPlayer.candidates)
          ),
          console.log(
            "unownedPlayers: " + JSON.stringify(this.props.unownedPlayers)
          ),
          (
            <CandidatesTable
              player={this.props.selectedPlayer}
              unownedPlayers={this.props.unownedPlayers}
            ></CandidatesTable>
          ))}
      </div>,
      <div className="Submit">
        <button className="GetMyTeam" onClick={onGetMyTeam}>
          Get my Team
        </button>
      </div>,
    ];
  }
}
