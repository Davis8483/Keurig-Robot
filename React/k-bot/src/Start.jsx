import { useState } from "react";
import start_video from "./start_background.mp4";
import title from "./title.png";

const StartScreen = () => {
  const [text, setText] = useState(""); // Initialize state for text

  const handleClick = () => {
    setText("Clicked!"); // Update text on click
    console.log("clicked");
  };
  window.addEventListener("mouseup", handleClick);

  return (
    <div className="Start">
      {text} {/* Display the text state */}
      <video className="background-video" autoPlay loop muted>
        <source src={start_video} type="video/mp4"></source>
      </video>
      <img src={title} id="title-image" alt="title" />
    </div>
  );
};

export default StartScreen;
