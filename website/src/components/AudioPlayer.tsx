import { useEffect, useRef } from 'react';

interface AudioPlayerProps {
  audioUrl: string | null;
  expertId: string;
  onComplete: () => void;
  autoPlay: boolean;
}

// Global audio instance to persist across React re-renders
let globalAudio: HTMLAudioElement | null = null;
let currentAudioUrl: string | null = null;

export default function AudioPlayer({ audioUrl, expertId, onComplete, autoPlay }: AudioPlayerProps) {
  const onCompleteRef = useRef(onComplete);
  const hasStartedPlayback = useRef(false);

  // Keep onComplete ref up to date without triggering effect
  useEffect(() => {
    onCompleteRef.current = onComplete;
  }, [onComplete]);

  useEffect(() => {
    if (!audioUrl) {
      return;
    }

    // If this is the same audio URL already playing, don't restart
    if (currentAudioUrl === audioUrl && globalAudio && !globalAudio.paused) {
      console.log(`[AudioPlayer] Audio already playing for ${expertId}`);
      return;
    }

    console.log(`[AudioPlayer] Starting playback for ${expertId}:`, audioUrl);
    hasStartedPlayback.current = false;

    // Stop any existing audio
    if (globalAudio) {
      globalAudio.pause();
      globalAudio.src = '';
    }

    // Create new audio element
    const audio = new Audio(audioUrl);
    globalAudio = audio;
    currentAudioUrl = audioUrl;

    // Set up event listeners
    const handleEnded = () => {
      console.log(`[AudioPlayer] Playback ended for ${expertId}`);
      globalAudio = null;
      currentAudioUrl = null;
      onCompleteRef.current();
    };

    const handleError = (e: Event) => {
      console.error(`[AudioPlayer] Playback error for ${expertId}:`, e);
      globalAudio = null;
      currentAudioUrl = null;
      // Still call onComplete to allow the UI to continue
      onCompleteRef.current();
    };

    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('error', handleError);

    // Autoplay if enabled
    if (autoPlay && !hasStartedPlayback.current) {
      hasStartedPlayback.current = true;
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.catch((error) => {
          console.error(`[AudioPlayer] Autoplay failed for ${expertId}:`, error);
          globalAudio = null;
          currentAudioUrl = null;
          // Call onComplete if autoplay fails
          onCompleteRef.current();
        });
      }
    }

    // Cleanup function - only runs when component unmounts or audioUrl changes
    return () => {
      console.log(`[AudioPlayer] Cleanup called for ${expertId}`);
      // Don't stop audio on cleanup - let it play through
      // Only remove event listeners
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('error', handleError);
    };
  }, [audioUrl, expertId, autoPlay]);

  // This component doesn't render any visible UI
  // Audio playback is handled programmatically
  return null;
}
