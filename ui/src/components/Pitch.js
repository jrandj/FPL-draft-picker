import React from "react";
// import ReactDOM from "react-dom";
import pitchImage from "../data/pitch.svg";

export default class Pitch extends React.Component {
  render() {
    return (
      <div className="Pitch">
        {/* <div className="Flexbox-Column-Container"> */}
        <img className="Outlines" src={pitchImage} alt="Pitch outlines" />
        <div className="Flexbox-Row-Container">
          <div className="Flexbox-Row-Item">Goalkeeper</div>
        </div>
        <div className="Flexbox-Row-Container">
          <div className="Flexbox-Row-Item">LB</div>
          <div className="Flexbox-Row-Item">DC1</div>
          <div className="Flexbox-Row-Item">DC2</div>
          <div className="Flexbox-Row-Item">RB</div>
        </div>
        <div className="Flexbox-Row-Container">
          <div className="Flexbox-Row-Item">MID1</div>
          <div className="Flexbox-Row-Item">MID2</div>
          <div className="Flexbox-Row-Item">MID3</div>
        </div>
        <div className="Flexbox-Row-Container">
          <div className="Flexbox-Row-Item">FWD1</div>
          <div className="Flexbox-Row-Item">FWD2</div>
          <div className="Flexbox-Row-Item">FWD3</div>
        </div>
        <div className="Flexbox-Row-Container">
          <div className="Flexbox-Row-Item">SUB1</div>
          <div className="Flexbox-Row-Item">SUB2</div>
          <div className="Flexbox-Row-Item">SUB3</div>
          <div className="Flexbox-Row-Item">SUB4</div>
        </div>
      </div>
    );
  }
}
