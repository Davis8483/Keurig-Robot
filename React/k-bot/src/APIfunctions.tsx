import { Kpod } from "./APImodels";
import axios from "axios";

export function getProducts(callback: (products: Kpod[]) => void) {
  axios
    .get("/products/")
    .then((response) => {
      console.log("t1");
      callback(response.data as Kpod[]);
    })
    .catch((error) => {
      callback([] as Kpod[]);
    });
}
