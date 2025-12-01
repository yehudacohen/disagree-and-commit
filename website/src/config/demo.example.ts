// Example demo configuration with sample S3 URLs
// Copy this to demo.ts and update with your actual S3 URLs

import type { DemoAudioConfig } from './demo';

export const DEMO_CONFIG_EXAMPLE: DemoAudioConfig = {
  enabled: true,
  showBanner: false,
  showFinaleAnimation: false,
  showPlayAudioButton: false,
  
  audioUrls: {
    jeff: {
      round1: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-round1.mp3',
      round2: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-round2.mp3',
      round3: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-round3.mp3',
      round4: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-round4.mp3',
    },
    swami: {
      round1: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-round1.mp3',
      round2: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-round2.mp3',
      round3: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-round3.mp3',
      round4: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-round4.mp3',
    },
    werner: {
      round1: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-round1.mp3',
      round2: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-round2.mp3',
      round3: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-round3.mp3',
      round4: 'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-round4.mp3',
    },
  },
};

// Alternative: Using pre-signed URLs (for private buckets)
export const DEMO_CONFIG_PRESIGNED_EXAMPLE: DemoAudioConfig = {
  enabled: true,
  showBanner: false,
  showFinaleAnimation: false,
  showPlayAudioButton: false,
  
  audioUrls: {
    jeff: {
      round1: 'https://my-bucket.s3.amazonaws.com/audio/jeff-round1.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round2: 'https://my-bucket.s3.amazonaws.com/audio/jeff-round2.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round3: 'https://my-bucket.s3.amazonaws.com/audio/jeff-round3.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round4: 'https://my-bucket.s3.amazonaws.com/audio/jeff-round4.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
    },
    swami: {
      round1: 'https://my-bucket.s3.amazonaws.com/audio/swami-round1.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round2: 'https://my-bucket.s3.amazonaws.com/audio/swami-round2.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round3: 'https://my-bucket.s3.amazonaws.com/audio/swami-round3.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round4: 'https://my-bucket.s3.amazonaws.com/audio/swami-round4.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
    },
    werner: {
      round1: 'https://my-bucket.s3.amazonaws.com/audio/werner-round1.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round2: 'https://my-bucket.s3.amazonaws.com/audio/werner-round2.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round3: 'https://my-bucket.s3.amazonaws.com/audio/werner-round3.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
      round4: 'https://my-bucket.s3.amazonaws.com/audio/werner-round4.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
    },
  },
};
