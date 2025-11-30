import { useEffect, useState } from 'react';
import './FinaleOverlay.css';

interface FinaleOverlayProps {
  isTriggered: boolean;
  onComplete?: () => void;
}

export function FinaleOverlay({ isTriggered, onComplete }: FinaleOverlayProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [showText, setShowText] = useState(false);

  useEffect(() => {
    if (isTriggered) {
      // Start the overlay animation
      setIsVisible(true);
      
      // Show text after initial dramatic pause
      const textTimer = setTimeout(() => {
        setShowText(true);
      }, 800);

      // Call onComplete after full animation sequence
      const completeTimer = setTimeout(() => {
        if (onComplete) {
          onComplete();
        }
      }, 4000);

      return () => {
        clearTimeout(textTimer);
        clearTimeout(completeTimer);
      };
    }
  }, [isTriggered, onComplete]);

  if (!isVisible) {
    return null;
  }

  return (
    <div className="finale-overlay">
      <div className="finale-background" />
      <div className="finale-content">
        {showText && (
          <>
            <div className="finale-text-main">
              DISAGREE AND COMMIT
            </div>
            <div className="finale-text-sub">
              The panel has reached a decision...
            </div>
          </>
        )}
      </div>
    </div>
  );
}
