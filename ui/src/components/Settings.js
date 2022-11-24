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
    const onClick = () => {
      this.props.getPlayers();
      // this.leagueIDChangeHandlerRef.current.value = "";
      // this.teamNameChangeHandlerRef.current.value = "";
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
          <DropdownButton className="dropdown" title="Formation">
            <Dropdown.Item href="#/action-1">5-3-2</Dropdown.Item>
            <Dropdown.Item href="#/action-1">5-4-1</Dropdown.Item>
            <Dropdown.Item href="#/action-1">5-2-3</Dropdown.Item>
            <Dropdown.Item href="#/action-1">4-3-3</Dropdown.Item>
            <Dropdown.Item href="#/action-1">4-5-1</Dropdown.Item>
            <Dropdown.Item href="#/action-1">4-4-2</Dropdown.Item>
            <Dropdown.Item href="#/action-1">3-5-2</Dropdown.Item>
            <Dropdown.Item href="#/action-1">3-4-3</Dropdown.Item>
          </DropdownButton>
          <button className="CTA" onClick={onClick}>
            Get my Team
          </button>
        </div>
      </div>
    );
  }
}
