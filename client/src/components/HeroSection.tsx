"use client";
import React from "react";
import { Spotlight } from "@/components/ui/Spotlight-new";
import { Button } from "./ui/button";
import Tempelates from "./Tempelates";

export function HeroSection() {

    const scrollToNextSection = () => {
    const nextSection = document.getElementById('next-section');
    if (nextSection) {
      nextSection.scrollIntoView({ behavior: 'smooth' });
    }
  };


  return (
    <>
    <div className="h-[40rem] w-full rounded-md flex flex-col md:items-center md:justify-center bg-black/[0.96] antialiased bg-grid-white/[0.02] relative overflow-hidden">
      <Spotlight />
      <div className=" p-4 max-w-7xl  mx-auto relative z-10  w-full pt-20 md:pt-0">
        <h1 className="text-4xl md:text-6xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400 bg-opacity-50">
          Meet Peter <br /> Your Concepts Explainer On Demand.
        </h1>
        <p className="mt-4 font-normal text-base text-neutral-300 max-w-2xl text-center mx-auto">
            Peter is a virtual assistant designed to help you understand complex
            concepts in a simple and engaging way. Whether you're a student, a
            professional, or just curious, Peter is here to explain anything you
            need to know.
        </p>
      </div>
      {/* Cards section */}
      <section className="w-full flex justify-center items-center gap-4 mt-8">
        <Button 
        onClick={scrollToNextSection}
          className="
            py-6 px-12 
            text-lg
            bg-white/10 backdrop-blur-md border border-white/20
            text-white font-medium 
            shadow-[0_8px_30px_rgb(0,0,0,0.12)]
            transition-all duration-300 ease-out
            hover:bg-white/20 hover:shadow-[0_8px_30px_rgba(255,255,255,0.2)]
            hover:scale-105 hover:border-white/50
            active:scale-95
            rounded-lg
          "
        >
          <span className="flex items-center gap-3">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-6 w-6 transition-transform duration-300 group-hover:rotate-12" 
              viewBox="0 0 20 20" 
              fill="currentColor"
            >
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zm12.553 1.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
            </svg>
            Create a Video
          </span>
        </Button>
      </section>
    </div>
    <div id="next-section" className="h-screen w-full  bg-black/[0.96] text-white bg-grid-white/[0.02]">
        <Tempelates />
    </div>
    </>
  );
}
