import React from "react";

export default class Submit extends React.Component {
  render() {
    let getMyTeam = null;
    getMyTeam = (
      <a title="Get my Team" className="CTA">
        Get my Team
      </a>
    );
    return <div className="Submit">{getMyTeam}</div>;
  }
}
