import React from "react";
import pitchImage from "../data/pitch.svg";
import PlayerCard from "./PlayerCard";

export default class Pitch extends React.Component {
  // constructor(props) {
  //   super(props);
  // }

  render() {
    return (
      <div className="Pitch">
        <img className="Outlines" src={pitchImage} alt="Pitch outlines" />
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 1 && val.selected === true)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  {console.log("player passing is " + JSON.stringify(o))}
                  <PlayerCard player={o} />
                </div>
              );
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 2 && val.selected === true)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 3 && val.selected === true)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 4 && val.selected === true)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 1 && val.selected === false)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
          {this.props.players
            .filter((val) => val.element_type === 2 && val.selected === false)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
          {this.props.players
            .filter((val) => val.element_type === 3 && val.selected === false)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
          {this.props.players
            .filter((val) => val.element_type === 4 && val.selected === false)
            .map(function (o) {
              return (
                <div className="Flexbox-Row-Item" key={o.id}>
                  <PlayerCard player={o} />
                </div>
              );
            })}
        </div>
      </div>
    );
  }
}
