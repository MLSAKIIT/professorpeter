'use client';

import React from 'react';

const Footer = () => {
  return (
    <footer className="glass-card border-t border-gray-700/50 backdrop-blur-xl mt-16">
      <div className="container mx-auto max-w-6xl py-12 px-6">
        <div className="text-center mb-8">
          <h3 className="text-white text-2xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            About Professor Peter
          </h3>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">🎬</span>
            </div>
            <h4 className="text-white font-semibold mb-2">AI-Powered</h4>
            <p className="text-gray-400 text-sm">Advanced language models generate Peter Griffin-style explanations</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">⚡</span>
            </div>
            <h4 className="text-white font-semibold mb-2">Instant Results</h4>
            <p className="text-gray-400 text-sm">Generate educational videos in minutes, not hours</p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl mx-auto mb-4 flex items-center justify-center">
              <span className="text-2xl">🚀</span>
            </div>
            <h4 className="text-white font-semibold mb-2">Easy Sharing</h4>
            <p className="text-gray-400 text-sm">Share your videos instantly with friends and colleagues</p>
          </div>
        </div>
        
        <div className="text-center border-t border-gray-700/50 pt-8">
          <p className="text-gray-400 text-sm mb-4 max-w-2xl mx-auto leading-relaxed">
            Experience the most unconventional educational platform on the internet. Transform complex topics into 
            hilariously simple explanations with Peter Griffin's unique perspective.
          </p>
          <div className="flex justify-center items-center gap-4 mb-4">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
            <p className="text-blue-400 font-medium italic">
              "Welcome to PeterTalks • Where prompts die and videos cry."
            </p>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
          </div>
          <div className="mt-6 pt-4 border-t border-gray-700/30">
            <p className="text-purple-400 text-sm font-medium mb-2">
              Built by Team Prof. Peters Students for MLSA Internal Hackathon 2025
            </p>
            <div className="flex flex-wrap justify-center gap-x-4 gap-y-1 text-xs text-gray-400 mb-2">
              <span className="font-medium text-blue-400">Mentor:</span>
              <span>Soham Roy</span>
            </div>
            <div className="flex flex-wrap justify-center gap-x-4 gap-y-1 text-xs text-gray-400">
              <span className="font-medium text-blue-400">Team:</span>
              <span>Kartikeya Trivedi</span>
              <span>•</span>
              <span>Vaibhav Deep Srivastava</span>
              <span>•</span>
              <span>Yash Raj Gupta</span>
              <span>•</span>
              <span>Vaibhav Raj</span>
              <span>•</span>
              <span>Aditya Shukla</span>
              <span>•</span>
              <span>Sidhi Kumari</span>
            </div>
          </div>
          <p className="text-gray-500 text-xs mt-4">
            © 2024 Professor Peter. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;