import React from "react";
import QRCode from "react-qr-code";

export const MenuBar = (props) => {
  var typeName = props.permutation || "BottomBar";

  return (
    <div className={`acrylic ${typeName}`} id="menu-bar">
      {props.children}
    </div>
  );
};

export const ProductInfo = (props) => {
  return (
    <div className="ProductInfo">
      <QRCode
        id="payment-qr-code"
        value={props.link}
        bgColor={"transparent"}
        fgColor="#ffffff"
        size={500}
      />
    </div>
  );
};
