// Demo mode configuration for pre-recorded audio from S3
// This allows the app to run without a backend by using pre-recorded audio files

export interface DemoAudioConfig {
  enabled: boolean;
  showBanner: boolean; // Flag to show/hide the demo banner
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
  showBanner: true, // Set to false to hide the demo banner
  
  audioUrls: {
    jeff: {
      round1: undefined, // Initial opinion on how to solve the problem
      round2: undefined, // Disagreement with other panelists
      round3: undefined, // Personal callout based on personality
      round4: undefined, // Disagree and commit to one solution
    },
    swami: {
      round1: undefined,
      round2: undefined,
      round3: undefined,
      round4: undefined,
    },
    werner: {
      round1: 'https://road-to-reinvent-redteam.s3.amazonaws.com/debate_fast_3min.mp3',
      round2: undefined,
      round3: undefined,
      round4: undefined,
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
