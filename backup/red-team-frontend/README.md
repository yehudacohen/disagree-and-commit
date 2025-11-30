# Install and start the REACT frontend application

1. Navigate to the `frontend` folder
    ```bash
    cd frontend
    ```
2. Install
    ```bash
    npm install
    ```

3. This step is optional: set environment variables for the React app. If not provided, the application defaults to `ws://localhost:8081`.

    ```bash
    export REACT_APP_WEBSOCKET_URL='YOUR_WEB_SOCKET_URL'
    ```

4. If you want to run the React code outside the workshop environment, update the `homepage` value in the `react-client/package.json` file from "/proxy/3000/" to "."

5. Run
    ```
    npm start
    ```

When using Chrome, if there's no sound, please ensure the sound setting is set to Allow, as shown below.
![chrome-sound](./static/chrome-sound-setting.png)

⚠️ **Warning:** Known issue: This UI is intended for demonstration purposes and may encounter state management issues after frequent conversation start/stop actions. Refreshing the page can help resolve the issue.


## How the Frontend Handles Nova Sonic Streaming Audio

The React frontend establishes a bidirectional WebSocket connection with the Python backend to enable real-time speech-to-speech interaction with Nova Sonic.

**Key Components:**

1. **Audio Input Capture**
   - Uses the Web Audio API's `getUserMedia()` to capture microphone input
   - Converts raw audio to base64-encoded chunks and sends them via WebSocket to the server
   - Maintains a continuous stream of audio data without waiting for the entire recording to complete

2. **WebSocket Communication**
   - Establishes a persistent WebSocket connection to `ws://localhost:8081` (or custom URL via `REACT_APP_WEBSOCKET_URL`)
   - Sends `audioInput` events containing base64-encoded audio chunks with metadata (promptName, contentName)
   - Receives streaming responses from the server in real-time

3. **Audio Playback**
   - Receives audio chunks from the server as base64-encoded data
   - Decodes chunks to Float32Array format using the Web Audio API
   - Buffers and plays audio continuously as chunks arrive, enabling low-latency playback
   - Uses `AudioContext` to manage audio playback without waiting for the complete response

4. **Session Management**
   - Sends `sessionStart` event to initialize a new conversation session
   - Sends `sessionEnd` event to clean up resources when done
   - Handles connection state (connecting, connected, disconnected) with automatic reconnection logic

**Audio Flow:**
```
Microphone → Audio Capture → Base64 Encode → WebSocket → Server
→ Nova Sonic Processing → Streaming Response → WebSocket → Decode
→ Audio Playback → Speaker
```

The frontend maintains simultaneous bidirectional streaming, allowing users to hear responses while still sending audio input for natural conversation-like interaction.
