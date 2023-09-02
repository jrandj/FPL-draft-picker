import React from "react";
import playerImagePlaceholder from "../data/player.svg";
import PlayerPopup from "./PlayerPopup";
import { IoAlertCircleSharp } from "react-icons/io5";
import "reactjs-popup/dist/index.css";

export default class PlayerCard extends React.Component {
  render() {
    const setSelectedPlayer = (event) => {
      // console.log("Receiving event at PlayerCard: " + JSON.stringify(event));
      this.props.setSelectedPlayer(event);
    };
    return (
      <div
        className="PlayerCard"
        onClick={() => setSelectedPlayer(this.props.player)}
        style={{ display: "flex", flexDirection: "column" }}
      >
        <div
          className="PlayerCardHeader"
          style={{ display: "flex", flexDirection: "row" }}
        >
          <div
            className="PlayerCardStatus"
            style={{
              display: "flex",
              flexDirection: "row",
              width: "50%",
              height: "50%",
            }}
          >
            <IoAlertCircleSharp
              style={{ color: "crimson" }}
            ></IoAlertCircleSharp>
          </div>
          <div className="PlayerCardHeaderIcon">
            <img
              src={playerImagePlaceholder}
              alt="Player"
              style={{
                width: "100%",
                height: "100%",
              }}
            ></img>
          </div>
          <div
            className="PlayerCardInfo"
            style={{
              display: "flex",
              flexDirection: "row",
              width: "50%",
              height: "50%",
            }}
          >
            <PlayerPopup></PlayerPopup>
          </div>
        </div>

        <div
          className="PlayerCardPoints"
          style={{
            margin: 0,
            padding: 0,
            backgroundColor: `rgb(55, 0, 60)`,
            color: `rgb(255,255,255)`,
            fontSize: 12,
          }}
        >
          {/* {this.props.player.team} */}
          {this.props.player.ngw_pts_projection}
        </div>

        <div
          className="PlayerCardName"
          style={{
            margin: 0,
            padding: 0,
            backgroundColor: `#fff`,
            color: `#242424`,
            fontSize: 12,
          }}
        >
          {this.props.player.web_name}
        </div>
      </div>
    );
  }
}
