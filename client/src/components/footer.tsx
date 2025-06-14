'use client';

import React from 'react';

const Footer = () => {
  const footer = {
    backgroundColor: '#1f2937',
    color: '#9ca3af',
    padding: '32px 16px',
    borderTop: '1px solid #374151'
  };

  const container= {
    maxWidth: '1200px',
    margin: '0 auto'
  };

  const title = {
    color: '#f9fafb',
    fontSize: '18px',
    fontWeight: '600',
    marginBottom: '16px'
  };

  const text = {
    fontSize: '14px',
    lineHeight: '1.6',
    margin: '0'
  };

  return (
    <footer style={footer}>
      <div style={container}>
        <h3 style={title}>About</h3>
        <p style={text}>
          Lorem ipsum dolor sit amet, leo tristique arcu egestas ut a "template." Nunc bibendum eros. Consectetur ornare elit, 
          sed leo ex facilisibus mauris posuere consectetur. Ultricised tempor dignissim ut tellus ut ut ultricies magna altera, 
          Vehicula dictum tempor donec vitae velit. Neque eleifend arcu enim diam at faucibus. Maecenas imperdiet varius in 
          neque dolore 🟡 amet, placerat ut velit colluban. Consectetur sed consectetur duis tellus ac febre ante velit quis nulla, 
          leo in integer elit quam tristique viverra. Vel et pulbinar mauris, eget lobortis sed rhoncus leo mauris mauris.
        </p>
      </div>
    </footer>
  );
};

export default Footer;