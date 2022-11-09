import React from "react";

export default class Submit extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const onClick = (event) => {
      this.props.getPlayers();
      //   this.props.setLeagueID("");
      //   this.props.setTeamName("");
    };

    return (
      <div className="Submit">
        <button className="CTA" onClick={onClick}>
          Get my Team
        </button>
      </div>
    );
  }
}
