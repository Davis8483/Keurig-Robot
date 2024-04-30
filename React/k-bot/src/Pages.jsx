import start_video from "./start_background.mp4";
import products_video from "./products_background.mp4";
import title from "./title.png";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import { useState } from "react";

export const StartScreen = () => {
  return (
    <div className="Start">
      <video className="background-video" autoPlay loop muted>
        <source src={start_video} type="video/mp4"></source>
      </video>
      <img src={title} id="title-image" alt="title" />
    </div>
  );
};

export const ProductSelection = () => {
  const [width, setWidth] = useState(window.innerWidth);

  return (
    <div className="Products">
      <video className="background-video" autoPlay loop muted>
        <source src={products_video} type="video/mp4"></source>
      </video>
      <Swiper
        spaceBetween={0}
        slidesPerView={3}
        onSwiper={(swiper) => console.log(swiper)}
        centeredSlides={true}
        className="swiper-container"
        slidesOffsetBefore={width * -0.15}
      >
        <SwiperSlide className="swiper-slide" proper>
          <img
            className="swiper-img"
            src="https://files.stripe.com/links/MDB8YWNjdF8xT3E1OGFFT1Vnb1ozQ3NrfGZsX3Rlc3Rfb3g2R2k4MkNyRjZhbURmV0pzOFJjWmxB00USG8gYgU"
          ></img>
        </SwiperSlide>
        <SwiperSlide className="swiper-slide">
          <img
            className="swiper-img"
            src="https://files.stripe.com/links/MDB8YWNjdF8xT3E1OGFFT1Vnb1ozQ3NrfGZsX3Rlc3Rfb3g2R2k4MkNyRjZhbURmV0pzOFJjWmxB00USG8gYgU"
          ></img>{" "}
        </SwiperSlide>
        <SwiperSlide className="swiper-slide">
          <img
            className="swiper-img"
            src="https://files.stripe.com/links/MDB8YWNjdF8xT3E1OGFFT1Vnb1ozQ3NrfGZsX3Rlc3Rfb3g2R2k4MkNyRjZhbURmV0pzOFJjWmxB00USG8gYgU"
          ></img>{" "}
        </SwiperSlide>
        <SwiperSlide className="swiper-slide">
          <img
            className="swiper-img"
            src="https://files.stripe.com/links/MDB8YWNjdF8xT3E1OGFFT1Vnb1ozQ3NrfGZsX3Rlc3Rfb3g2R2k4MkNyRjZhbURmV0pzOFJjWmxB00USG8gYgU"
          ></img>{" "}
        </SwiperSlide>
        <SwiperSlide className="swiper-slide">
          <img
            className="swiper-img"
            src="https://files.stripe.com/links/MDB8YWNjdF8xT3E1OGFFT1Vnb1ozQ3NrfGZsX3Rlc3Rfb3g2R2k4MkNyRjZhbURmV0pzOFJjWmxB00USG8gYgU"
          ></img>{" "}
        </SwiperSlide>
      </Swiper>
    </div>
  );
};
