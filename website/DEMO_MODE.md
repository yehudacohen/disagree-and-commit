# Demo Mode Configuration

Demo mode allows you to run the Disagree and Commit app without a backend by using pre-recorded audio files from S3.

## Four-Round Debate Structure

The demo mode simulates a four-round panel discussion:

1. **Round 1: Initial Opinions** - Each panelist provides their opinion on how to solve the problem
2. **Round 2: Disagreements** - Each panelist disagrees with the other panelists based on their own worldview
3. **Round 3: Personal Callouts** - Panelists call out each other's solutions in a personal way based on their personality
4. **Round 4: Disagree and Commit** - Panelists disagree but commit to one solution

The frustration meter progresses as each panelist speaks, increasing with each round.

## Setup

1. **Upload your audio files to S3**
   - Create an S3 bucket or use an existing one
   - Upload MP3 audio files for each panelist (Jeff, Swami, Werner) for each round
   - Make sure the files are publicly accessible OR generate pre-signed URLs

2. **Configure CORS on your S3 bucket** (if using public URLs)
   ```json
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["GET", "HEAD"],
       "AllowedOrigins": ["http://localhost:5173", "https://your-domain.com"],
       "ExposeHeaders": ["Content-Length", "Content-Type"],
       "MaxAgeSeconds": 3000
     }
   ]
   ```

3. **Update the demo configuration**
   
   Edit `src/config/demo.ts`:

   ```typescript
   export const DEMO_CONFIG: DemoAudioConfig = {
     enabled: true, // Enable demo mode
     showBanner: true, // Set to false to hide the demo banner
     
     audioUrls: {
       jeff: {
         round1: 'https://your-bucket.s3.amazonaws.com/jeff-round1.mp3',
         round2: 'https://your-bucket.s3.amazonaws.com/jeff-round2.mp3',
         round3: 'https://your-bucket.s3.amazonaws.com/jeff-round3.mp3',
         round4: 'https://your-bucket.s3.amazonaws.com/jeff-round4.mp3',
       },
       swami: {
         round1: 'https://your-bucket.s3.amazonaws.com/swami-round1.mp3',
         round2: 'https://your-bucket.s3.amazonaws.com/swami-round2.mp3',
         round3: 'https://your-bucket.s3.amazonaws.com/swami-round3.mp3',
         round4: 'https://your-bucket.s3.amazonaws.com/swami-round4.mp3',
       },
       werner: {
         round1: 'https://your-bucket.s3.amazonaws.com/werner-round1.mp3',
         round2: 'https://your-bucket.s3.amazonaws.com/werner-round2.mp3',
         round3: 'https://your-bucket.s3.amazonaws.com/werner-round3.mp3',
         round4: 'https://your-bucket.s3.amazonaws.com/werner-round4.mp3',
       },
     },
   };
   ```

## How It Works

When demo mode is enabled:

1. **WebSocket connection is disabled** - No backend required
2. **Four-round structure** - Each expert speaks in each of the four rounds
3. **Frustration progression** - Frustration levels increase as rounds progress
4. **Audio playback** - MP3 files play for each panelist when available
5. **Graceful fallback** - Missing MP3 URLs are gracefully ignored, text still displays
6. **Visual indicator** - An orange banner shows "DEMO MODE" at the top (can be disabled)

## URL Formats

You can use different S3 URL formats:

### Public URLs
```
https://your-bucket.s3.amazonaws.com/path/to/file.mp3
https://your-bucket.s3.us-east-1.amazonaws.com/path/to/file.mp3
```

### Pre-signed URLs (for private buckets)
Generate these on your backend or using AWS CLI:
```bash
aws s3 presign s3://your-bucket/path/to/file.mp3 --expires-in 3600
```

Then paste the generated URL into the config.

## Configuration Options

### `enabled`
Set to `true` to enable demo mode, `false` to use the live WebSocket backend.

### `showBanner`
Set to `true` to show the orange "DEMO MODE" banner, `false` to hide it. Useful for presentations where you don't want to show it's a demo.

### `audioUrls`
Configure MP3 URLs for each expert and each round. You can:
- Provide URLs for all rounds for all experts
- Provide URLs for only some rounds (missing URLs are gracefully ignored)
- Provide URLs for only some experts
- Leave all URLs as `undefined` to test the debate flow without audio

## Testing

1. Set `enabled: true` in `src/config/demo.ts`
2. Optionally add audio URLs for each expert and round
3. Run the app: `npm run dev`
4. Submit any problem statement
5. Watch the four-round debate play out

## Switching Back to Live Mode

Simply set `enabled: false` in `src/config/demo.ts` to reconnect to the WebSocket backend.

## Tips

- Missing MP3 URLs are gracefully ignored - the text will still display
- The frustration meter increases progressively through the rounds
- Round 1 starts at frustration level 1-2
- Round 4 reaches frustration level 4-5, triggering the finale
- Demo mode is great for presentations, testing, or when the backend is unavailable
- Set `showBanner: false` for a cleaner presentation experience
