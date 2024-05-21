import React from "react";
import QRCode from "react-qr-code";
import { Kpod } from "./APImodels.tsx";
import { useQuery } from "@tanstack/react-query";
import { ReactComponent as Loading } from "./loading.svg";
import outOfStock from "./out_of_stock.png";

export const MenuBarBase = (props) => {
  var typeName = props.permutation || "BottomBar";

  return (
    <div className={`acrylic ${typeName}`} id="menu-bar">
      {props.children}
    </div>
  );
};

export const PaymentQR = (props) => {
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
    <>
      {pLink.isFetching ? (
        <Loading className="Loading" />
      ) : (
        <div id="product_payment">
          <div id="qr_label">Scan to Pay • ${product.price}</div>
          <QRCode
            id="payment-qr-code"
            value={pLink.data}
            bgColor={"transparent"}
            fgColor="#ffffff"
            size={500}
          />
        </div>
      )}
    </>
  );
};

export const ProductInfo = (props) => {
  const product = props.product as Kpod;

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
      {product.in_stock ? (
        <PaymentQR product={product} />
      ) : (
        <div id="product_payment">
          <img src={outOfStock} id="out_of_stock_image"></img>
          <text id="out_of_stock_label">Out of Stock</text>
        </div>
      )}
    </div>
  );
};
