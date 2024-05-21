import React from "react";
import QRCode from "react-qr-code";
import { Kpod } from "./APImodels.tsx";
import { useQuery } from "@tanstack/react-query";
import { ReactComponent as Loading } from "./loading.svg";

export const MenuBar = (props) => {
  var typeName = props.permutation || "BottomBar";

  return (
    <div className={`acrylic ${typeName}`} id="menu-bar">
      {props.children}
    </div>
  );
};

export const ProductInfo = (props) => {
  const product = props.product as Kpod;

  const { isPending, error, data } = useQuery({
    queryKey: ["productInfo", product.id, props.randID], // randID should be generated using Math.random() and is used to force the loading image instead of displaying old data
    queryFn: () =>
      fetch(
        "/products/select?" + new URLSearchParams({ stripeID: product.id }),
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
      {isPending ? (
        <Loading className="Loading" />
      ) : (
        <QRCode
          id="payment-qr-code"
          value={data}
          bgColor={"transparent"}
          fgColor="#ffffff"
          size={500}
        />
      )}
    </div>
  );
};
