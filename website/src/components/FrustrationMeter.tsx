import { useEffect, useState } from 'react';
import type { FrustrationLevel } from '../types';
import './FrustrationMeter.css';

interface FrustrationMeterProps {
  level: FrustrationLevel;
  onFinaleTriggered?: () => void;
}

export function FrustrationMeter({ level, onFinaleTriggered }: FrustrationMeterProps) {
  const [displayLevel, setDisplayLevel] = useState<FrustrationLevel>(level);
  const [isAnimating, setIsAnimating] = useState(false);

  // Animate transitions between levels
  useEffect(() => {
    if (level === displayLevel) {
      return;
    }

    // Start animation
    const animationTimer = setTimeout(() => {
      setIsAnimating(true);
    }, 0);
    
    // Delay the level change to allow animation
    const levelTimer = setTimeout(() => {
      setDisplayLevel(level);
      setIsAnimating(false);
      
      // Trigger finale if level reaches 5
      if (level === 5 && onFinaleTriggered) {
        onFinaleTriggered();
      }
    }, 300);

    return () => {
      clearTimeout(animationTimer);
      clearTimeout(levelTimer);
    };
  }, [level, displayLevel, onFinaleTriggered]);

  // Apply dramatic effects for high frustration (level 4+)
  useEffect(() => {
    if (displayLevel >= 4) {
      // Add screen shake class to body
      document.body.classList.add('screen-shake');
      
      // Add color shift class based on level
      if (displayLevel === 5) {
        document.body.classList.add('color-shift-critical');
      } else {
        document.body.classList.add('color-shift-high');
      }
    } else {
      // Remove dramatic effects when frustration drops
      document.body.classList.remove('screen-shake', 'color-shift-high', 'color-shift-critical');
    }

    // Cleanup on unmount
    return () => {
      document.body.classList.remove('screen-shake', 'color-shift-high', 'color-shift-critical');
    };
  }, [displayLevel]);

  // Determine color based on level
  const getColorClass = () => {
    if (displayLevel <= 2) return 'frustration-low';
    if (displayLevel === 3) return 'frustration-medium';
    if (displayLevel === 4) return 'frustration-high';
    return 'frustration-critical';
  };

  // Get label for frustration level
  const getLabel = () => {
    const labels: Record<FrustrationLevel, string> = {
      1: 'Calm',
      2: 'Concerned',
      3: 'Annoyed',
      4: 'Frustrated',
      5: 'CRITICAL'
    };
    return labels[displayLevel];
  };

  return (
    <div className={`frustration-meter ${getColorClass()} ${isAnimating ? 'animating' : ''}`}>
      <div className="frustration-label">
        {getLabel()}
      </div>
      <div className="frustration-bars">
        {[1, 2, 3, 4, 5].map((barLevel) => (
          <div
            key={barLevel}
            className={`frustration-bar ${barLevel <= displayLevel ? 'active' : ''}`}
            data-level={barLevel}
          />
        ))}
      </div>
      <div className="frustration-level-text">
        Level {displayLevel}/5
      </div>
    </div>
  );
}
