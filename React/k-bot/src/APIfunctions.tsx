import { Kpod } from "./APImodels";
import axios from "axios";
import { NotificationManager } from "react-notifications";

export function getProducts(callback: (products: Kpod[]) => void) {
  axios
    .get("/products/")
    .then((response) => {
      console.log("t1");
      callback(response.data as Kpod[]);
    })
    .catch((error) => {
      // display error to use for 10 seconds
      NotificationManager.error(`${error}`, "Failed to Fetch Products", 10000);
      callback([] as Kpod[]);
    });
}
