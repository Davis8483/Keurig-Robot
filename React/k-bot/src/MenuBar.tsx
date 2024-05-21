import React from "react";
import QRCode from "react-qr-code";
import { Kpod } from "./APImodels.tsx";
import { useQuery } from "@tanstack/react-query";
import { ReactComponent as Loading } from "./loading.svg";

export const MenuBarBase = (props) => {
  var typeName = props.permutation || "BottomBar";

  return (
    <div className={`acrylic ${typeName}`} id="menu-bar">
      {props.children}
    </div>
  );
};

export const ProductInfo = (props) => {
  const product = props.product as Kpod;

  const pLink = useQuery({
    queryKey: ["productInfo", product.id],
    queryFn: () =>
      fetch(
        "/products/select/?" + new URLSearchParams({ stripeID: product.id }),
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json", // Set content type as JSON
          },
        }
      ).then((res) => res.json()),
  });

  return (
    <div className="ProductInfo">
      <div id="product_data">
        <text id="product_name">{product.name}</text>
        <hr />
        <text id="prouct_desc">
          {product.description.length > 0
            ? product.description
            : "No description."}
        </text>
      </div>
      {pLink.isFetching ? (
        <Loading className="Loading" />
      ) : (
        <div id="product_payment">
          <div id="qr_label">Scan to Pay - ${product.price}</div>
          <QRCode
            id="payment-qr-code"
            value={pLink.data}
            bgColor={"transparent"}
            fgColor="#ffffff"
            size={500}
          />
        </div>
      )}
    </div>
  );
};
