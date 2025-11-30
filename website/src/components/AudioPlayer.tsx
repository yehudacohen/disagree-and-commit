import { useEffect, useRef } from 'react';

interface AudioPlayerProps {
  audioUrl: string | null;
  expertId: string;
  onComplete: () => void;
  autoPlay: boolean;
}

export default function AudioPlayer({ audioUrl, expertId, onComplete, autoPlay }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!audioUrl) {
      return;
    }

    // Create new audio element
    const audio = new Audio(audioUrl);
    audioRef.current = audio;

    // Set up event listeners
    const handleEnded = () => {
      onComplete();
    };

    const handleError = (e: ErrorEvent) => {
      console.error(`Audio playback error for ${expertId}:`, e);
      // Still call onComplete to allow the UI to continue
      onComplete();
    };

    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('error', handleError as EventListener);

    // Autoplay if enabled
    if (autoPlay) {
      audio.play().catch((error) => {
        console.error(`Autoplay failed for ${expertId}:`, error);
        // Call onComplete if autoplay fails
        onComplete();
      });
    }

    // Cleanup function
    return () => {
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('error', handleError as EventListener);
      audio.pause();
      audio.src = '';
      audioRef.current = null;
    };
  }, [audioUrl, expertId, onComplete, autoPlay]);

  // This component doesn't render any visible UI
  // Audio playback is handled programmatically
  return null;
}
