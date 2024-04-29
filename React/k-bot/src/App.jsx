import "./App.css";
import StartScreen from "./Start";
import MenuBar from "./Bar";
import { useState } from "react";
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

  const handleClick = () => {
    setBarType("FullMenu"); // Update text on click
    console.log("clicked");
  };
  window.addEventListener("mouseup", handleClick);

  return (
    <div className="App">
      <StartScreen name={"hello world"} />
      <MenuBar typeName={barType} />
    </div>
  );
}

export default App;
