// SwamiAvatar.jsx - Avatar component for Swami character
import React, { useState } from 'react';
import './SwamiAvatar.css';

const SwamiAvatar = ({ size = 200, onSpeak }) => {
  const [isTalking, setIsTalking] = useState(false);

  const speak = (duration = 2000) => {
    setIsTalking(true);
    if (onSpeak) onSpeak();
    
    setTimeout(() => {
      setIsTalking(false);
    }, duration);
  };

  const speakText = (text) => {
    const words = text.match(/\b\w+\b/g) || [];
    const duration = words.length * 200;
    speak(duration);
  };

  return (
    <div 
      className={`swami-avatar-container ${isTalking ? 'talking' : 'idle'}`}
      style={{ width: size, height: size }}
    >
      <div className="swami-avatar">
        <div className="avatar-head">
          <div className="hair"></div>
          <div className="glasses">
            <div className="glass-frame left">
              <div className="lens"></div>
              <div className="eye"></div>
            </div>
            <div className="bridge"></div>
            <div className="glass-frame right">
              <div className="lens"></div>
              <div className="eye"></div>
            </div>
          </div>
          <div className="nose"></div>
          <div className="mouth">
            <div className="smile-line"></div>
            <div className="teeth"></div>
          </div>
        </div>
        <div className="avatar-body">
          <div className="suit-jacket"></div>
          <div className="shirt"></div>
          <div className="tie"></div>
        </div>
      </div>
    </div>
  );
};

export default SwamiAvatar;
