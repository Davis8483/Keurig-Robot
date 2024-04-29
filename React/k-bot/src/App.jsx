import "./App.css";
import StartScreen from "./Start";
import MenuBar from "./Bar";
import { useState } from "react";
import { ReactComponent as Loading } from "./loading.svg";
import axios from "axios";

function App() {
  // const newSocket = new WebSocket("ws://127.0.0.1:8000/ws");
  // newSocket.onopen = () => console.log('WS Connected');
  // newSocket.onclose = () => console.log('WS Disconnected');
  // newSocket.onerror = (err) => console.log("WS Error");
  // newSocket.onmessage = (e) => {
  //   const data = JSON.parse(e.data);
  //   console.log("WS Receives: ", data);
  // }
  const [barType, setBarType] = useState("BottomMenu");
  const [barComponents, setBarComponents] = useState(<h1>Tap to start...</h1>);
  const handleClick = () => {
    setBarType("FullMenu"); // Update text on click
    setBarComponents(<Loading className="Loading" />);
    console.log("clicked");
  };
  window.addEventListener("mouseup", handleClick);
  window.addEventListener("keypress", (event) => {
    setBarType("SideMenu");
  });

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
      <StartScreen />
      <MenuBar permutation={barType}>{barComponents}</MenuBar>
    </div>
  );
}

export default App;
