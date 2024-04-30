import "./App.css";
import { StartScreen, ProductSelection } from "./Pages";
import MenuBar from "./Bar";
import { useState } from "react";
import { ReactComponent as Loading } from "./loading.svg";
import axios from "axios";
import { useEffect } from "react";
import maximize_sound from "./maximize.ogg";
import minimize_sound from "./minimize.ogg";
import select_sound from "./select.ogg";

function App() {
  const [barType, setBarType] = useState("BottomMenu");
  const [barComponents, setBarComponents] = useState(<h1>Tap to start...</h1>);
  const [pageContents, setPageContents] = useState(<StartScreen />);
  const maximize = new Audio(maximize_sound);
  const minimize = new Audio(minimize_sound);
  const select = new Audio(select_sound);

  const podSelected = (index) => {
    const clone = select.cloneNode(true); // Create a copy of the audio element
    clone.volume = 0.8;
    clone.play(); // Play the cloned element
  };

  const handleClick = () => {
    maximize.play();
    setBarType("FullMenu"); // Update text on click
    setBarComponents(<Loading className="Loading" />);
    setTimeout(() => {
      setPageContents(<ProductSelection onSelected={podSelected} />);
      setTimeout(() => {
        minimize.play();
        setBarType("SideMenu");
        setTimeout(() => {
          setBarComponents();
        }, 1000);
      }, 1000);
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
    </div>
  );
}

export default App;
