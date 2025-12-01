import { useEffect, useRef, useState } from 'react';
import Lottie, { type LottieRefCurrentProps } from 'lottie-react';
import type { Expert, FrustrationLevel } from '../types';
import { FrustrationMeter } from './FrustrationMeter';
import './PanelDisplay.css';

interface PanelDisplayProps {
  experts: Expert[];
  speakingExpertId: string | null;
  frustrationLevels: Record<string, FrustrationLevel>;
}

export function PanelDisplay({ experts, speakingExpertId, frustrationLevels }: PanelDisplayProps) {
  return (
    <div className="panel-display">
      <div className="experts-grid">
        {experts.map((expert) => (
          <ExpertAvatar
            key={expert.id}
            expert={expert}
            isSpeaking={speakingExpertId === expert.id}
            frustrationLevel={frustrationLevels[expert.id] || 1}
          />
        ))}
      </div>
    </div>
  );
}

interface ExpertAvatarProps {
  expert: Expert;
  isSpeaking: boolean;
  frustrationLevel: FrustrationLevel;
}

function ExpertAvatar({ expert, isSpeaking, frustrationLevel }: ExpertAvatarProps) {
  const lottieRef = useRef<LottieRefCurrentProps>(null);
  const [animationData, setAnimationData] = useState<unknown>(null);
  const [loadError, setLoadError] = useState(false);

  // Determine which animation to show
  const getAnimationUrl = () => {
    if (isSpeaking) {
      return expert.lottieAnimations.speaking;
    }
    if (frustrationLevel > 1) {
      return expert.lottieAnimations.frustrated[frustrationLevel];
    }
    return expert.lottieAnimations.idle;
  };

  // Load Lottie animation
  useEffect(() => {
    const animationUrl = getAnimationUrl();
    
    fetch(animationUrl)
      .then(response => {
        if (!response.ok) throw new Error('Failed to load animation');
        return response.json();
      })
      .then(data => {
        setAnimationData(data);
        setLoadError(false);
      })
      .catch(() => {
        setLoadError(true);
      });
  }, [isSpeaking, frustrationLevel]);

  // Color theme classes
  const colorClasses = {
    orange: 'border-orange-500 bg-orange-50',
    blue: 'border-blue-500 bg-blue-50',
    purple: 'border-purple-500 bg-purple-50',
  };

  const glowClasses = {
    orange: 'shadow-orange-glow',
    blue: 'shadow-blue-glow',
    purple: 'shadow-purple-glow',
  };

  const baseColorClass = colorClasses[expert.color as keyof typeof colorClasses] || 'border-gray-500 bg-gray-50';
  const glowClass = isSpeaking ? (glowClasses[expert.color as keyof typeof glowClasses] || '') : '';

  return (
    <div className="expert-avatar-container">
      <div 
        className={`expert-avatar ${baseColorClass} ${glowClass} ${isSpeaking ? 'speaking' : ''}`}
        data-expert-id={expert.id}
      >
        {/* Avatar display - Lottie animation or fallback */}
        <div className="avatar-display">
          {!loadError && animationData ? (
            <Lottie
              lottieRef={lottieRef}
              animationData={animationData}
              loop={true}
              autoplay={true}
              style={{ width: '100%', height: '100%' }}
            />
          ) : (
            <img 
              src={expert.avatarImage} 
              alt={expert.name}
              className="avatar-fallback"
              onError={(e) => {
                // If image also fails, show placeholder
                (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          )}
        </div>

        {/* Expert info */}
        <div className="expert-info">
          <h3 className="expert-name">{expert.name}</h3>
          <p className="expert-title">{expert.title}</p>
          <span className={`expert-badge badge-${expert.color}`}>
            {expert.badge}
          </span>
        </div>
      </div>

      {/* Frustration Meter */}
      <FrustrationMeter 
        level={frustrationLevel}
      />
    </div>
  );
}
