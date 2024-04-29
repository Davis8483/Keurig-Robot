import "./App.css";
import StartScreen from "./Start";
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

  return (
    <div className="App">
      <StartScreen />
    </div>
  );
}

export default App;
