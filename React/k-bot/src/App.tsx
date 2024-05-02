import React from "react";
import "./App.css";
import { StartScreen, ProductSelection } from "./Pages.tsx";
import MenuBar from "./Bar.tsx";
import { ReactComponent as Loading } from "./loading.svg";
import { useEffect, useState } from "react";
import maximize_sound from "./maximize.ogg";
import minimize_sound from "./minimize.ogg";
import select_sound from "./select.ogg";
import { Kpod } from "./APImodels.tsx";
import { getProducts } from "./APIfunctions.tsx";
import {
  NotificationContainer,
  NotificationManager,
} from "react-notifications";
import "react-notifications/lib/notifications.css";

function App() {
  const [barType, setBarType] = useState("BottomMenu");
  const [barComponents, setBarComponents] = useState(<h1>Tap to start...</h1>);
  const [pageContents, setPageContents] = useState(<StartScreen />);
  const maximize = new Audio(maximize_sound);
  const minimize = new Audio(minimize_sound);
  const select = new Audio(select_sound);

  const podSelected = (index) => {
    const clone: HTMLAudioElement = select.cloneNode(true) as HTMLAudioElement; // Create a copy of the audio element
    clone.volume = 0.8;
    clone.play(); // Play the cloned element
  };

  const handleClick = () => {
    maximize.play();
    setBarType("FullMenu"); // Update text on click
    setBarComponents(<Loading className="Loading" />);
    setTimeout(() => {
      // load the page with the products fetched from the api
      getProducts((pods: Kpod[]) => {
        setPageContents(
          <ProductSelection onSelected={podSelected} products={pods} />
        );
        // wait another half second for assets to load
        setTimeout(() => {
          minimize.play();
          setBarType("SideMenu");
          setTimeout(() => {
            setBarComponents(<></>);
          }, 500);
        }, 1000);
      });
    }, 1000);
  };

  useEffect(() => {
    window.addEventListener("mouseup", handleClick);
  }, []);

  function imagesLoaded(parentNode) {
    const imgElements = parentNode.querySelectorAll("img");
    for (const img of imgElements) {
      if (!img.complete) {
        return false;
      }
    }
    return true;
  }

  return (
    <div className="App">
      {pageContents}
      <MenuBar permutation={barType}>{barComponents}</MenuBar>
      <NotificationContainer />
    </div>
  );
}

export default App;
