import React from "react";
// import ReactDOM from "react-dom";
import pitchImage from "../data/pitch.svg";

export default class Pitch extends React.Component {
  constructor(props) {
    super(props);
    console.log("this constructor " + JSON.stringify(this.props));
  }
  // componentDidUpdate(prevProps, prevState) {
  //   if (prevProps.players != this.props.players) {
  //     // console.log(
  //     //   "this componentDidUpdate prevPops: " +
  //     //     JSON.stringify(prevProps) +
  //     //     " this.props.players: " +
  //     //     JSON.stringify(this.props.players) +
  //     //     " this.props.prevState: " +
  //     //     JSON.stringify(prevState)
  //     // );
  //     // console.log(
  //     //   "keys: " +
  //     //     JSON.stringify(
  //     //       this.props.players
  //     //         .filter((val) => val.element_type === 1)
  //     //         .map(function (o) {
  //     //           return o.web_name;
  //     //         })
  //     //     )
  //     // );
  //   }
  // }
  render() {
    return (
      <div className="Pitch">
        <img className="Outlines" src={pitchImage} alt="Pitch outlines" />
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 1)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 2)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 3)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
        </div>
        <div className="Flexbox-Row-Container">
          {this.props.players
            .filter((val) => val.element_type === 4)
            .map(function (o) {
              return <div className="Flexbox-Row-Item"> {o.web_name} </div>;
            })}
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
