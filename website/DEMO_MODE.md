# Demo Mode Configuration

Demo mode allows you to run the Disagree and Commit app without a backend by using pre-recorded audio files from S3.

## Setup

1. **Upload your audio files to S3**
   - Create an S3 bucket or use an existing one
   - Upload MP3 audio files for each panelist (Jeff, Swami, Werner)
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
     
     audioUrls: {
       jeff: [
         'https://your-bucket.s3.amazonaws.com/jeff-response-1.mp3',
         'https://your-bucket.s3.amazonaws.com/jeff-response-2.mp3',
         'https://your-bucket.s3.amazonaws.com/jeff-response-3.mp3',
       ],
       swami: [
         'https://your-bucket.s3.amazonaws.com/swami-response-1.mp3',
         'https://your-bucket.s3.amazonaws.com/swami-response-2.mp3',
         'https://your-bucket.s3.amazonaws.com/swami-response-3.mp3',
       ],
       werner: [
         'https://your-bucket.s3.amazonaws.com/werner-response-1.mp3',
         'https://your-bucket.s3.amazonaws.com/werner-response-2.mp3',
         'https://your-bucket.s3.amazonaws.com/werner-response-3.mp3',
       ],
     },
   };
   ```

## How It Works

When demo mode is enabled:

1. **WebSocket connection is disabled** - No backend required
2. **Audio URLs are cycled** - Each expert's audio files play in sequence
3. **Debate is simulated** - Messages appear with timing similar to a real debate
4. **Visual indicator** - An orange banner shows "DEMO MODE" at the top

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

## Testing

1. Set `enabled: true` in `src/config/demo.ts`
2. Add at least one audio URL per expert
3. Run the app: `npm run dev`
4. Submit any problem statement
5. Watch the demo debate play with your audio files

## Switching Back to Live Mode

Simply set `enabled: false` in `src/config/demo.ts` to reconnect to the WebSocket backend.

## Tips

- Audio files will cycle through the array, so you can have multiple responses per expert
- If no audio URL is provided, the message will still appear but without sound
- Demo mode is great for presentations, testing, or when the backend is unavailable
- You can mix experts with and without audio URLs
