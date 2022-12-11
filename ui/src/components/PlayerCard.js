import React from "react";
import playerImagePlaceholder from "../data/player.svg";

export default class PlayerCard extends React.Component {
  // constructor(props) {
  //   super(props);
  // }

  render() {
    return (
      <div className="PlayerCard">
        {/* {console.log("props receiving " + JSON.stringify(this.props))} */}
        {console.log("player receiving " + JSON.stringify(this.props.player))}
        <img
          src={playerImagePlaceholder}
          alt="Player"
          style={{ width: "40%", height: "40%" }}
        ></img>
        <p
          style={{
            margin: 0,
            padding: 0,
            backgroundColor: `rgb(55, 0, 60)`,
            color: `rgb(255,255,255)`,
            fontSize: 12,
          }}
        >
          {this.props.player.team}
        </p>
        <p
          style={{
            margin: 0,
            padding: 0,
            backgroundColor: `#fff`,
            color: `#242424`,
            fontSize: 12,
          }}
        >
          {this.props.player.web_name}
        </p>
      </div>
    );
  }
}
