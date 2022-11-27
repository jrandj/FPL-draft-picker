import React from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import "bootstrap/dist/css/bootstrap.min.css";

export default class Settings extends React.Component {
  constructor(props) {
    super(props);
    this.leagueIDChangeHandlerRef = React.createRef();
    this.teamNameChangeHandlerRef = React.createRef();
    this.formationChangeHandlerRef = React.createRef();
    console.log("Create with this.props: " + JSON.stringify(this.props));
  }
  componentDidUpdate(prevProps) {
    console.log("Component did update");
    console.log("this.props: " + JSON.stringify(this.props));
    console.log("prevProps: " + JSON.stringify(prevProps));
  }
  render() {
    const leagueIDChangeHandler = (event) => {
      this.props.setLeagueID(event.target.value);
    };
    const teamNameChangeHandler = (event) => {
      this.props.setTeamName(event.target.value);
    };
    const onGetMyTeam = () => {
      this.props.getPlayers();
      // this.leagueIDChangeHandlerRef.current.value = "";
      // this.teamNameChangeHandlerRef.current.value = "";
    };
    const onSetFormation = (event) => {
      console.log("event is " + event);
      this.props.setFormation(event);
    };

    return (
      <div className="Inputs">
        <div>
          <input
            className="Search-League-ID"
            value={this.props.leagueID}
            type="search"
            onChange={leagueIDChangeHandler}
            placeholder="Enter your League ID..."
            ref={this.leagueIDChangeHandlerRef}
            autoFocus
          />
          <input
            className="Search-Team-Name"
            value={this.props.teamName}
            type="search"
            onChange={teamNameChangeHandler}
            placeholder="Enter your Team Name..."
            ref={this.teamNameChangeHandlerRef}
            autoFocus
          />
        </div>

        <div className="Submit">
          <DropdownButton
            className="Dropdown"
            onSelect={onSetFormation}
            title={`Formation: ${this.props.formation}`}
            // key={`${this.props.formation}`}
            // ref={this.formationChangeHandlerRef}
          >
            <Dropdown.Item eventKey="343">3-4-3</Dropdown.Item>
            <Dropdown.Item eventKey="352">3-5-2</Dropdown.Item>
            <Dropdown.Item eventKey="532">5-3-2</Dropdown.Item>
            <Dropdown.Item eventKey="541">5-4-1</Dropdown.Item>
            <Dropdown.Item eventKey="433">4-3-3</Dropdown.Item>
            <Dropdown.Item eventKey="442">4-4-2</Dropdown.Item>
            <Dropdown.Item eventKey="451">4-5-1</Dropdown.Item>
          </DropdownButton>
          <button className="CTA" onClick={onGetMyTeam}>
            Get my Team
          </button>
        </div>
      </div>
    );
  }
}
