import React from "react";

export default class Candidate extends React.Component {
  render() {
    return (
      <p className="Result-player">
        {
          (console.log("player: " + JSON.stringify(this.props.player)),
          this.props.player.web_name)
        }
      </p>
    );
    // return (
    //   <div
    //     key={this.props.player.id}
    //     className="Result-player grabbable"
    //     onClick={() => {
    //       if (this.props.lastPlayerToAdd && window.innerWidth <= 910) {
    //         // Close keyboard before creating screenshot
    //         document.querySelector(".Search-player").blur();
    //         this.props.updateValue("");
    //         this.props.selectPlayer(this.props.player);
    //       } else {
    //         this.props.selectPlayer(this.props.player);
    //         this.props.updateValue("");
    //       }
    //     }}
    //   >
    //     <img
    //       alt={this.props.player.name}
    //       src={this.state.picture}
    //       className="Photo"
    //     />
    //     {this.props.player.rating !== "0" && (
    //       <p className="Name">{this.props.player.name}</p>
    //     )}
    //     {this.props.player.rating === "0" && (
    //       <p className="Name">Add "{this.props.player.name}"</p>
    //     )}
    //     <img
    //       className="Icon"
    //       alt={this.props.player.club.name}
    //       src={this.state.logo}
    //     />
    //   </div>
    // );
  }
}
