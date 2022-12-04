import React from "react";
// import ReactDOM from "react-dom";
import pitchImage from "../data/pitch.svg";

export default class Pitch extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="Pitch">
        <img className="Outlines" src={pitchImage} alt="Pitch outlines" />
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 1 && val.selected === true)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 2 && val.selected === true)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 3 && val.selected === true)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 4 && val.selected === true)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 1 && val.selected === false)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
          {this.props.players
            .filter((val) => val.element_type == 2 && val.selected === false)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
          {this.props.players
            .filter((val) => val.element_type == 3 && val.selected === false)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
          {this.props.players
            .filter((val) => val.element_type == 4 && val.selected === false)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
      </div>
    );
  }
}
