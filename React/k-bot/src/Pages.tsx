import React from "react";
import start_video from "./start_background.mp4";
import products_video from "./products_background.mp4";
import title from "./title.png";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/css";
import { useState, useEffect } from "react";
import { Kpod } from "./APImodels.tsx";

export const StartScreen = (props) => {
  return (
    <div className="Start">
      <video className="background-video" autoPlay loop muted>
        <source src={start_video} type="video/mp4"></source>
      </video>
      <img src={title} id="title-image" alt="title" />
    </div>
  );
};

export const ProductSelection = (props) => {
  const [width, setWidth] = useState(window.innerWidth);
  const pods: Kpod[] = props.products || [];

  return (
    <div className="Products">
      <video className="background-video" autoPlay loop muted>
        <source src={products_video} type="video/mp4"></source>
      </video>
      <Swiper
        spaceBetween={0}
        slidesPerView={3}
        centeredSlides={true}
        className="swiper-container"
        slidesOffsetBefore={width * -0.15}
        onSlideChange={(swiper) => {
          props.onSelected(pods[swiper.activeIndex]);
        }}
        onInit={(swiper) => {
          if (pods.length > 0) {
            setTimeout(
              (product) => {
                props.onSelected(product, true);
              },
              2000,
              pods[swiper.activeIndex]
            );
          }
        }}
      >
        {pods.map((data) => {
          return (
            <SwiperSlide className="swiper-slide">
              <img className="swiper-img" alt="Kpod" src={data.image_url}></img>
            </SwiperSlide>
          );
        })}
      </Swiper>
    </div>
  );
};
