import start_video from "./start_background.mp4";
import title from "./title.png";

console.log(title);

const StartScreen = () => {
  return (
    <div className="Start">
      <video id="background-video" autoPlay loop muted>
        <source src={start_video} type="video/mp4"></source>
      </video>
      <img src={title} id="title-image" alt="title" />
    </div>
  );
};

export default StartScreen;
