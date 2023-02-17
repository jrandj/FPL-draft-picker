import React from "react";

export default class CandidatesTable extends React.Component {
  render() {
    return (
      <table>
        <thead>
          <tr>
            <th>Player</th>
            <th>{this.props.rankMethod}</th>
          </tr>
        </thead>
        <tbody>
          {this.props.player.candidates.map((item) => (
            <tr key={item[0]}>
              <td>
                {
                  this.props.unownedPlayers.find((o) => o.id === item[0])
                    .web_name
                }
              </td>
              <td>{item[1]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
}
