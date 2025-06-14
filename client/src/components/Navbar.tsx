'use client';

import React from 'react';

const Navbar = () => {
  const navbar = {
    backgroundColor: '#1f2937',
    color: 'white',
    padding: '12px 16px'
  };

  const container = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    maxWidth: '1200px',
    margin: '0 auto'
  };

  const leftSection = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    
  };

  const logo = {
    width: '32px',
    height: '32px',
    backgroundColor: '#4b5563',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };

  const logoS = {
    width: '40px',
    height: '30px',
    borderRadius: '50%',
  };

  const title = {
    fontSize: '18px',
    fontWeight: '500',
    margin: '0'
  };

  const rightSection = {
    display: 'flex',
    alignItems: 'center',
    gap: '24px'
  };

  const link = {
    color: '#d1d5db',
    textDecoration: 'none',
    transition: 'color 0.2s ease-in-out'
  };

  const handleMouseEnter = (e) => {
    e.target.style.color = 'white';
  };

  const handleMouseLeave = (e) => {
    e.target.style.color = '#d1d5db';
  };

  return (
    <nav style={navbar}>
      <div style={container}>
        <div style={leftSection}>
          <div style={logo}>
            <img src="/logo.png" alt="Logo" style={logoS} />
          </div>
          <h1 style={title}>Prof. Peter's Students</h1>
        </div>
        
        <div style={rightSection}>
          <a 
            href="/about" 
            style={link}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            About
          </a>
          <a 
            href="/help" 
            style={link}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            Help
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;