// Demo mode configuration for pre-recorded audio from S3
// This allows the app to run without a backend by using pre-recorded audio files

export interface DemoAudioConfig {
  enabled: boolean;
  showBanner: boolean; // Flag to show/hide the demo banner
  showFinaleAnimation: boolean; // Flag to show/hide the "disagree and commit" animation
  showPlayAudioButton: boolean; // Flag to show/hide the play audio button
  architectureDiagramUrl?: string; // URL to architecture diagram image to display at the end
  audioUrls: {
    [expertId: string]: {
      round1?: string; // Initial opinion
      round2?: string; // Disagreement with others
      round3?: string; // Personal callout
      round4?: string; // Disagree and commit
    };
  };
}

// Configure your S3 URLs here
// Each expert has audio for each of the 4 rounds
export const DEMO_CONFIG: DemoAudioConfig = {
  enabled: true, // Set to true to enable demo mode
  showBanner: false, // Set to false to hide the demo banner
  showFinaleAnimation: false, // Set to false to skip the "disagree and commit" animation
  showPlayAudioButton: false, // Set to false to hide the play audio button
  architectureDiagramUrl: undefined, // URL to architecture diagram image (e.g., 'https://your-bucket.s3.amazonaws.com/architecture.png')
  
  audioUrls: {
    jeff: {
      round1: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round1_jeff.mp3',
      round2: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round2_jeff.mp3',
      round3: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round3_jeff.mp3',
      round4: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round4_jeff.mp3',
    },
    swami: {
      round1: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round1_swami.mp3',
      round2: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round2_swami.mp3',
      round3: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round3_swami.mp3',
      round4: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round4_swami.mp3',
    },
    werner: {
      round1: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round1_werner.mp3',
      round2: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round2_werner.mp3',
      round3: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round3_werner.mp3',
      round4: 'https://road-to-reinvent-redteam.s3.amazonaws.com/audio/round4_werner.mp3',
    },
  },
};

// Helper to get audio URL for an expert in a specific round
export function getDemoAudioUrl(expertId: string, round: number): string | undefined {
  if (!DEMO_CONFIG.enabled) {
    return undefined;
  }

  const expertUrls = DEMO_CONFIG.audioUrls[expertId];
  if (!expertUrls) {
    return undefined;
  }

  const roundKey = `round${round}` as keyof typeof expertUrls;
  return expertUrls[roundKey];
}

export function isDemoMode(): boolean {
  return DEMO_CONFIG.enabled;
}

export function shouldShowDemoBanner(): boolean {
  return DEMO_CONFIG.enabled && DEMO_CONFIG.showBanner;
}

export function shouldShowFinaleAnimation(): boolean {
  return DEMO_CONFIG.enabled && DEMO_CONFIG.showFinaleAnimation;
}

export function shouldShowPlayAudioButton(): boolean {
  return DEMO_CONFIG.enabled && DEMO_CONFIG.showPlayAudioButton;
}

export function getArchitectureDiagramUrl(): string | undefined {
  return DEMO_CONFIG.enabled ? DEMO_CONFIG.architectureDiagramUrl : undefined;
}
