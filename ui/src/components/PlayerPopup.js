import React from "react";
import Popup from "reactjs-popup";
import { FaInfoCircle } from "react-icons/fa";
import PlayerPopupCSS from "./PlayerPopup.module.css";
// import Modal from "react-bootstrap-modal";

import "reactjs-popup/dist/index.css";

export default () => (
  <Popup
    trigger={<FaInfoCircle style={{ color: "snow" }}></FaInfoCircle>}
    modal
    nested
  >
    {(close) => (
      <div className={PlayerPopupCSS.modal}>
        <div>
          <button className={PlayerPopupCSS.close} onClick={close}>
            &times;
          </button>
          <div className={PlayerPopupCSS.header}> Modal Title </div>
          <div className={PlayerPopupCSS.content}>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Atque, a
            nostrum. Dolorem, repellat quidem ut, minima sint vel eveniet
            quibusdam voluptates delectus doloremque, explicabo tempore dicta
            adipisci fugit amet dignissimos? <br /> Lorem ipsum dolor sit amet,
            consectetur adipisicing elit. Consequatur sit commodi beatae optio
            voluptatum sed eius cumque, delectus saepe repudiandae explicabo
            nemo nam libero ad, doloribus, voluptas rem alias. Vitae?{" "}
          </div>
          <div className={PlayerPopupCSS.actions}>
            {/* <Popup
              trigger={
                <button className={PlayerPopupCSS.button}> Trigger </button>
              }
              position="top center"
              nested
            >
              <span>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit. Beatae
                magni omnis delectus nemo, maxime molestiae dolorem numquam
                mollitia, voluptate ea, accusamus excepturi deleniti ratione
                sapiente! Laudantium, aperiam doloribus. Odit, aut.
              </span>
            </Popup> */}
            <button
              className="button"
              onClick={() => {
                close();
              }}
            >
              close
            </button>
          </div>
        </div>
      </div>
    )}
  </Popup>
);
