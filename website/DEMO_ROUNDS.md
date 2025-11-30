# Demo Mode - Four Round Structure

## Overview

The demo mode now features a structured four-round debate system where each panelist (Jeff, Swami, Werner) speaks in each round with progressively increasing frustration levels.

## Round Structure

### Round 1: Initial Opinions
Each panelist provides their opinion on how to solve the problem based on their worldview:
- **Jeff**: Advocates for simplicity and maintainability
- **Swami**: Focuses on speed and modern technologies
- **Werner**: Emphasizes scalability and distributed systems

**Frustration Level**: 1-2

### Round 2: Disagreements
Each panelist disagrees with the other panelists based on their own worldview:
- **Jeff**: Criticizes complexity and chasing new tech
- **Swami**: Argues against sacrificing performance and premature optimization
- **Werner**: Points out limitations of simple approaches and technical debt

**Frustration Level**: 2-3

### Round 3: Personal Callouts
Panelists call out each other's solutions in a personal way based on their personality:
- **Jeff**: Calls out Werner's tendency to over-engineer and Swami's focus on shiny objects
- **Swami**: Criticizes Jeff's outdated approaches and Werner's academic tendencies
- **Werner**: Challenges Jeff's simplicity obsession and Swami's lack of architectural thinking

**Frustration Level**: 3-4

### Round 4: Disagree and Commit
Panelists disagree but commit to one solution:
- **Jeff**: Commits to a balanced solution despite disagreements
- **Swami**: Commits to a hybrid approach with scalability hooks
- **Werner**: Commits to a pragmatic solution that grows over time

**Frustration Level**: 4-5 (triggers finale)

## Audio Configuration

Each expert can have an MP3 file for each round:

```typescript
audioUrls: {
  jeff: {
    round1: 'https://your-bucket.s3.amazonaws.com/jeff-round1.mp3',
    round2: 'https://your-bucket.s3.amazonaws.com/jeff-round2.mp3',
    round3: 'https://your-bucket.s3.amazonaws.com/jeff-round3.mp3',
    round4: 'https://your-bucket.s3.amazonaws.com/jeff-round4.mp3',
  },
  // ... same for swami and werner
}
```

## Features

- **Graceful Fallback**: Missing MP3 URLs are gracefully ignored - text still displays
- **Progressive Frustration**: Frustration meter increases as each panelist speaks
- **Audio Playback**: MP3 files play for each panelist when available
- **Banner Control**: `showBanner` flag allows hiding the demo mode banner
- **Finale Trigger**: Round 4 reaches frustration level 5, triggering the finale animation

## Configuration Flags

### `enabled`
Set to `true` to enable demo mode, `false` for live WebSocket mode.

### `showBanner`
Set to `true` to show the orange "DEMO MODE" banner, `false` to hide it for presentations.

## Timing

- **Streaming delay**: 2 seconds (simulates typing)
- **With audio**: 6 second delay between messages
- **Without audio**: 3 second delay between messages
- **Finale trigger**: 1 second after final message
- **Architecture reveal**: 2 seconds after finale
