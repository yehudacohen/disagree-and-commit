// Demo mode configuration for pre-recorded audio from S3
// This allows the app to run without a backend by using pre-recorded audio files

export interface DemoAudioConfig {
  enabled: boolean;
  audioUrls: {
    [expertId: string]: string[];
  };
}

// Configure your S3 URLs here
// Each expert can have multiple audio clips that will be played in sequence
export const DEMO_CONFIG: DemoAudioConfig = {
  enabled: true, // Set to true to enable demo mode
  
  audioUrls: {
    jeff: [
      // Example: 'https://your-bucket.s3.amazonaws.com/jeff-response-1.mp3',
      // Example: 'https://your-bucket.s3.us-east-1.amazonaws.com/jeff-response-2.mp3',
    ],
    swami: [
      // Example: 'https://your-bucket.s3.amazonaws.com/swami-response-1.mp3',
    ],
    werner: [
      'https://road-to-reinvent-redteam.s3.amazonaws.com/debate_fast_3min.mp3',
    ],
  },
};

// Helper to get next audio URL for an expert in demo mode
let audioIndexes: Record<string, number> = {
  jeff: 0,
  swami: 0,
  werner: 0,
};

export function getNextDemoAudioUrl(expertId: string): string | undefined {
  if (!DEMO_CONFIG.enabled) {
    return undefined;
  }

  const urls = DEMO_CONFIG.audioUrls[expertId];
  if (!urls || urls.length === 0) {
    return undefined;
  }

  const currentIndex = audioIndexes[expertId] || 0;
  const url = urls[currentIndex];
  
  // Cycle through available URLs
  audioIndexes[expertId] = (currentIndex + 1) % urls.length;
  
  return url;
}

export function resetDemoAudioIndexes(): void {
  audioIndexes = {
    jeff: 0,
    swami: 0,
    werner: 0,
  };
}

export function isDemoMode(): boolean {
  return DEMO_CONFIG.enabled;
}
