import { useEffect, useRef } from 'react';
import type { DebateMessage, StreamingMessage } from '../types';
import { getExpertById } from '../config/experts';
import './DebateDisplay.css';

interface DebateDisplayProps {
  messages: DebateMessage[];
  currentStreamingMessage: StreamingMessage | null;
  onPlayAudio?: (audioUrl: string) => void;
}

export function DebateDisplay({ 
  messages, 
  currentStreamingMessage,
  onPlayAudio 
}: DebateDisplayProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to keep latest content visible
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentStreamingMessage]);

  return (
    <div className="debate-display">
      <div className="messages-container">
        {messages.map((message) => (
          <MessageBubble 
            key={message.id} 
            message={message}
            onPlayAudio={onPlayAudio}
          />
        ))}
        
        {/* Show streaming message if present */}
        {currentStreamingMessage && (
          <StreamingBubble streamingMessage={currentStreamingMessage} />
        )}
        
        {/* Auto-scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

interface MessageBubbleProps {
  message: DebateMessage;
  onPlayAudio?: (audioUrl: string) => void;
}

function MessageBubble({ message, onPlayAudio }: MessageBubbleProps) {
  const expert = getExpertById(message.expertId);
  
  if (!expert) return null;

  // Color theme classes for speech bubbles
  const bubbleColorClasses = {
    orange: 'bg-orange-100 border-orange-400',
    blue: 'bg-blue-100 border-blue-400',
    purple: 'bg-purple-100 border-purple-400',
  };

  const badgeColorClasses = {
    orange: 'bg-orange-500 text-white',
    blue: 'bg-blue-500 text-white',
    purple: 'bg-purple-500 text-white',
  };

  const bubbleClass = bubbleColorClasses[expert.color as keyof typeof bubbleColorClasses] || 'bg-gray-100 border-gray-400';
  const badgeClass = badgeColorClasses[expert.color as keyof typeof badgeColorClasses] || 'bg-gray-500 text-white';

  return (
    <div className="message-bubble-container" data-expert-id={expert.id}>
      <div className={`message-bubble ${bubbleClass}`}>
        {/* Expert header with badge */}
        <div className="message-header">
          <div className="expert-identity">
            <span className="expert-name-small">{expert.name}</span>
            <span className={`expert-badge-small ${badgeClass}`}>
              {expert.badge}
            </span>
          </div>
        </div>

        {/* Message content */}
        <div className="message-content">
          {message.content}
        </div>

        {/* Show catchphrase if this is a disagreement */}
        {message.isDisagreement && (
          <div className="catchphrase">
            <span className="catchphrase-text">"{expert.catchphrase}"</span>
          </div>
        )}

        {/* Audio player button if audio is available */}
        {message.audioUrl && onPlayAudio && (
          <button 
            className="audio-play-button"
            onClick={() => onPlayAudio(message.audioUrl!)}
            aria-label={`Play audio for ${expert.name}'s message`}
          >
            🔊 Play Audio
          </button>
        )}
      </div>
    </div>
  );
}

interface StreamingBubbleProps {
  streamingMessage: StreamingMessage;
}

function StreamingBubble({ streamingMessage }: StreamingBubbleProps) {
  const expert = getExpertById(streamingMessage.expertId);
  
  if (!expert) return null;

  const bubbleColorClasses = {
    orange: 'bg-orange-100 border-orange-400',
    blue: 'bg-blue-100 border-blue-400',
    purple: 'bg-purple-100 border-purple-400',
  };

  const badgeColorClasses = {
    orange: 'bg-orange-500 text-white',
    blue: 'bg-blue-500 text-white',
    purple: 'bg-purple-500 text-white',
  };

  const bubbleClass = bubbleColorClasses[expert.color as keyof typeof bubbleColorClasses] || 'bg-gray-100 border-gray-400';
  const badgeClass = badgeColorClasses[expert.color as keyof typeof badgeColorClasses] || 'bg-gray-500 text-white';

  return (
    <div className="message-bubble-container streaming" data-expert-id={expert.id}>
      <div className={`message-bubble ${bubbleClass}`}>
        <div className="message-header">
          <div className="expert-identity">
            <span className="expert-name-small">{expert.name}</span>
            <span className={`expert-badge-small ${badgeClass}`}>
              {expert.badge}
            </span>
          </div>
        </div>

        <div className="message-content streaming-content">
          {streamingMessage.partialContent}
          <span className="typing-cursor">|</span>
        </div>
      </div>
    </div>
  );
}
