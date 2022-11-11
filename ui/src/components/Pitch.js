import React from "react";
import ReactDOM from "react-dom";
import pitchImage from "../data/pitch.svg";

export default class Pitch extends React.Component {
  render() {
    return (
      <div className="Pitch">
        <img className="Outlines" src={pitchImage} alt="Pitch outlines" />
      </div>
    );
  }
}
