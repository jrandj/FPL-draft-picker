import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import "bootstrap/dist/css/bootstrap.min.css";

export default class Settings extends React.Component {
  constructor(props) {
    super(props);
    this.leagueIDChangeHandlerRef = React.createRef();
    this.teamNameChangeHandlerRef = React.createRef();
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
          <button className="PimpMyTeam" onClick={onGetMyTeam}>
            Pimp my Team
          </button>
          <button className="GetMyTeam" onClick={onGetMyTeam}>
            Get my Team
          </button>
        </div>
      </div>
    );
  }
}
