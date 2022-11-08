import React from "react";

export default class Search extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const leagueIDChangeHandler = (event) => {
      this.props.setLeagueID(event.target.value);
    };
    const teamNameChangeHandler = (event) => {
      this.props.setTeamName(event.target.value);
    };

    return (
      <div className="Inputs">
        <div>
          <input
            className="Search-League-ID"
            type="search"
            onChange={leagueIDChangeHandler}
            placeholder="Enter your League ID..."
            autoFocus
          />
          <input
            className="Search-Team-Name"
            type="search"
            onChange={teamNameChangeHandler}
            placeholder="Enter your Team Name..."
            autoFocus
          />
        </div>
      </div>
    );
  }
}
