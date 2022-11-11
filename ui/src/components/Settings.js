import React from "react";

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
      this.leagueIDChangeHandlerRef.current.value = "";
      this.teamNameChangeHandlerRef.current.value = "";
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
          <button className="CTA" onClick={onClick}>
            Get my Team
          </button>
        </div>
      </div>
    );
  }
}
