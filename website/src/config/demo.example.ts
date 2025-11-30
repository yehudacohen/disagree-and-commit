// Example demo configuration with sample S3 URLs
// Copy this to demo.ts and update with your actual S3 URLs

import type { DemoAudioConfig } from './demo';

export const DEMO_CONFIG_EXAMPLE: DemoAudioConfig = {
  enabled: true,
  
  audioUrls: {
    jeff: [
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-intro.mp3',
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-rebuttal.mp3',
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/jeff-final.mp3',
    ],
    swami: [
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-intro.mp3',
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-rebuttal.mp3',
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/swami-final.mp3',
    ],
    werner: [
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-intro.mp3',
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-rebuttal.mp3',
      'https://my-bucket.s3.us-east-1.amazonaws.com/audio/werner-final.mp3',
    ],
  },
};

// Alternative: Using pre-signed URLs (for private buckets)
export const DEMO_CONFIG_PRESIGNED_EXAMPLE: DemoAudioConfig = {
  enabled: true,
  
  audioUrls: {
    jeff: [
      'https://my-bucket.s3.amazonaws.com/audio/jeff-1.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
    ],
    swami: [
      'https://my-bucket.s3.amazonaws.com/audio/swami-1.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
    ],
    werner: [
      'https://my-bucket.s3.amazonaws.com/audio/werner-1.mp3?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...',
    ],
  },
};
