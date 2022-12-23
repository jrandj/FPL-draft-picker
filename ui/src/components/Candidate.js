import React from "react";

export default class Candidate extends React.Component {
  render() {
    return (
      <p className="Result-player">
        {
          this.props.player.web_name
        }
      </p>
    );
  }
}
