import "./App.css";
import { StartScreen, ProductSelection } from "./Pages";
import MenuBar from "./Bar";
import { useState } from "react";
import { ReactComponent as Loading } from "./loading.svg";
import axios from "axios";
import { useEffect } from "react";

function App() {
  const [barType, setBarType] = useState("BottomMenu");
  const [barComponents, setBarComponents] = useState(<h1>Tap to start...</h1>);
  const [pageContents, setPageContents] = useState(<StartScreen />);

  const handleClick = () => {
    setBarType("FullMenu"); // Update text on click
    setBarComponents(<Loading className="Loading" />);
    setInterval(() => {
      setPageContents(<ProductSelection />);
      setInterval(() => {
        setBarType("SideMenu");
        setInterval(() => {
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
