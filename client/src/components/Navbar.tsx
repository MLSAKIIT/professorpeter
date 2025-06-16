'use client';

import React from 'react';

const Navbar = () => {
  return (
    <nav className="glass-card border-b border-gray-700/50 backdrop-blur-xl">
      <div className="container mx-auto flex items-center justify-between max-w-6xl py-4 px-6">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25">
            <img 
              src="/logo.png" 
              alt="Logo" 
              className="w-12 h-9 rounded-xl object-cover"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
                e.currentTarget.nextElementSibling.style.display = 'flex';
              }}
            />
            <span className="text-white text-xl font-bold hidden">🎓</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Prof. Peter's Students</h1>
            <p className="text-xs text-gray-400">AI Video Explainer</p>
          </div>
        </div>
        
        <div className="flex items-center gap-8">
          <a 
            href="/about" 
            className="text-gray-300 hover:text-white transition-all duration-300 text-sm font-medium hover:scale-105 px-3 py-2 rounded-lg hover:bg-gray-800/50"
          >
            About
          </a>
          <a 
            href="/help" 
            className="text-gray-300 hover:text-white transition-all duration-300 text-sm font-medium hover:scale-105 px-3 py-2 rounded-lg hover:bg-gray-800/50"
          >
            Help
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;