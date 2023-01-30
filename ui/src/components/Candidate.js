import React from "react";

export default class Candidate extends React.Component {
  render() {
    return (
      <p className="Result-player">
        {
          this.props.unownedPlayers.find((o) => o.id === this.props.player[0])
            .web_name
        }
      </p>
    );
  }
}
