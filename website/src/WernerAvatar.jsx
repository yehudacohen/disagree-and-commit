// WarnerAvatar.jsx - Avatar component for Warner character
import React, { useState } from 'react';
import './WarnerAvatar.css';

const WarnerAvatar = ({ size = 200, onSpeak }) => {
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
      className={`warner-avatar-container ${isTalking ? 'talking' : 'idle'}`}
      style={{ width: size, height: size }}
    >
      <div className="warner-avatar">
        <div className="avatar-head">
          <div className="bald-head"></div>
          <div className="eyebrows">
            <div className="eyebrow left"></div>
            <div className="eyebrow right"></div>
          </div>
          <div className="eyes">
            <div className="eye left"></div>
            <div className="eye right"></div>
          </div>
          <div className="nose"></div>
          <div className="mouth"></div>
          <div className="beard"></div>
        </div>
        <div className="avatar-body">
          <div className="black-shirt"></div>
          <div className="collar left"></div>
          <div className="collar right"></div>
          <div className="arm left"></div>
          <div className="arm right"></div>
          <div className="hand left"></div>
          <div className="hand right"></div>
        </div>
      </div>
    </div>
  );
};

export default WarnerAvatar;
