# Implementation Plan

## Phase 1: Project Setup & Core Infrastructure

- [-] 1. Initialize React project with TypeScript and Vite
  - Create new Vite project with React + TypeScript template
  - Configure TailwindCSS
  - Set up project structure: `src/components`, `src/hooks`, `src/services`, `src/types`, `src/assets`
  - Add dependencies: `lottie-react`, `mermaid`, `fast-check` (for testing)
  - _Requirements: 1.1, 3.2_

- [x] 2. Define TypeScript types and expert configuration
  - [x] 2.1 Create type definitions for Expert, FrustrationLevel, DebateMessage, WebSocketMessage
    - Define all interfaces from design document in `src/types/`
    - _Requirements: 1.1, 3.2, 4.3_
  - [x] 2.2 Create expert configuration constants
    - Define EXPERTS array with Jeff, Swami, Werner configurations
    - Include color schemes, catchphrases, badges
    - _Requirements: 8.1, 8.2, 8.3_
  - [ ]* 2.3 Write property test for expert styling consistency
    - **Property 1: Expert Styling Consistency**
    - **Validates: Requirements 3.2, 8.1, 8.2, 8.3**

## Phase 2: Core UI Components

- [x] 3. Implement PanelDisplay component
  - [x] 3.1 Create PanelDisplay with horizontal grid layout for 3 experts
    - Render expert avatars with static images as fallback
    - Apply expert-specific color themes (orange, blue, purple)
    - _Requirements: 1.1, 1.2_
  - [x] 3.2 Add Lottie animation integration
    - Integrate lottie-react for avatar animations
    - Implement idle, speaking, and frustrated animation states
    - _Requirements: 1.2, 1.3_
  - [x] 3.3 Implement speaking highlight effect
    - Add glowing border animation when expert is speaking
    - _Requirements: 1.2_

- [x] 4. Implement FrustrationMeter component
  - [x] 4.1 Create visual frustration indicator (1-5 levels)
    - Display frustration level per expert
    - Animate transitions between levels
    - _Requirements: 1.4, 5.1, 5.2_
  - [x] 4.2 Add dramatic effects for high frustration
    - Implement screen shake at level 4+
    - Add color shift effects approaching finale
    - _Requirements: 5.4_
  - [ ]* 4.3 Write property test for frustration display consistency
    - **Property 4: Frustration Display Consistency**
    - **Validates: Requirements 5.2, 5.4**

- [x] 5. Implement ProblemInput component
  - [x] 5.1 Create text input with placeholder and submit button
    - Style "Summon the Panel" button
    - Add loading state with "Assembling the panel..." text
    - _Requirements: 2.1, 2.2_
  - [x] 5.2 Implement input state management
    - Disable input during debate
    - Re-enable after debate concludes
    - _Requirements: 2.2, 2.3_
  - [ ]* 5.3 Write property test for input state management
    - **Property 2: Input State Management**
    - **Validates: Requirements 2.2, 2.3**

- [ ] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 3: Debate Display & Real-time Features

- [x] 7. Implement DebateDisplay component
  - [x] 7.1 Create speech bubble layout with expert colors
    - Style bubbles with expert signature colors
    - Add expert badges ("Keep it Simple", "Ship It!", "Scale or Fail")
    - _Requirements: 3.2, 8.1, 8.2, 8.3_
  - [x] 7.2 Implement typewriter streaming effect
    - Stream text word-by-word as it arrives
    - Auto-scroll to keep latest content visible
    - _Requirements: 3.1, 3.3_
  - [x] 7.3 Add catchphrase display for disagreements
    - Show "But why?", "Just ship it!", "Won't scale!" on disagreements
    - _Requirements: 8.4_
  - [ ]* 7.4 Write property test for expert catchphrase display
    - **Property 6: Expert Catchphrase Display**
    - **Validates: Requirements 8.4**

- [x] 8. Implement WebSocketClient service
  - [x] 8.1 Create WebSocket connection manager
    - Connect to API Gateway WebSocket endpoint
    - Handle connection lifecycle (connect, disconnect)
    - _Requirements: 4.1, 4.4_
  - [x] 8.2 Implement message sending with action routing
    - Send messages with `action` field for route selection
    - Format submitProblem payload correctly
    - _Requirements: 4.2_
  - [x] 8.3 Implement message receiving and routing
    - Parse incoming message types
    - Route to appropriate UI handlers
    - _Requirements: 4.3_
  - [ ]* 8.4 Write property test for WebSocket message routing
    - **Property 3: WebSocket Message Routing**
    - **Validates: Requirements 4.3**

- [x] 9. Implement AudioPlayer component
  - [x] 9.1 Create audio player for Nova Sonic responses
    - Play audio URLs from S3
    - Handle autoplay and completion callbacks
    - _Requirements: 3.1_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 4: Finale & Architecture Reveal

- [x] 11. Implement "Disagree and Commit" finale sequence
  - [x] 11.1 Create finale trigger logic
    - Detect when any expert reaches frustration level 5
    - Trigger dramatic animation sequence
    - _Requirements: 5.3_
  - [x] 11.2 Add finale visual effects
    - Implement dramatic transition animation
    - Add "DISAGREE AND COMMIT" text reveal
    - _Requirements: 6.1_

- [x] 12. Implement ArchitectureReveal component
  - [x] 12.1 Create Mermaid diagram renderer
    - Integrate mermaid.js library
    - Render architecture diagram from string
    - _Requirements: 6.2_
  - [x] 12.2 Add cost estimate display
    - Show satirical monthly cost breakdown
    - Display service-by-service justifications
    - _Requirements: 6.3_
  - [x] 12.3 Add expert endorsement quotes
    - Display each expert's reluctant agreement
    - _Requirements: 6.4_
  - [ ]* 12.4 Write property test for Mermaid diagram validity
    - **Property 5: Mermaid Diagram Validity**
    - **Validates: Requirements 6.2**

- [x] 13. Implement design assets download
  - [x] 13.1 Create diagram export functionality
    - Export Mermaid diagram as PNG
    - Trigger browser download
    - _Requirements: 7.1, 7.2_
  - [x] 13.2 Add download success feedback
    - Show success message on completion
    - _Requirements: 7.3_

## Phase 5: Integration & Polish

- [x] 14. Create main App component and wire everything together
  - [x] 14.1 Implement main application state management
    - Manage debate state (pending, in_progress, completed)
    - Track current speaking expert, frustration levels, messages
    - _Requirements: All_
  - [x] 14.2 Connect all components with WebSocket events
    - Wire WebSocket messages to UI state updates
    - Handle full debate flow from submit to reveal
    - _Requirements: All_

- [x] 15. Add placeholder Lottie animations and assets
  - [x] 15.1 Create or source Lottie animation files
    - Add idle, speaking, frustrated animations for each expert
    - Place in `public/lottie/` directory
    - _Requirements: 1.2, 1.3_
  - [x] 15.2 Add expert avatar images
    - Add placeholder images for Jeff, Swami, Werner
    - Place in `public/avatars/` directory
    - _Requirements: 1.1_

- [ ] 16. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Phase 6: AWS Infrastructure (CDK/SAM)

- [ ] 17. Set up AWS infrastructure
  - [ ] 17.1 Create S3 bucket for static site hosting
    - Configure bucket policy for CloudFront OAI
    - _Requirements: Infrastructure_
  - [ ] 17.2 Create S3 bucket for generated assets
    - Configure CORS for frontend access
    - _Requirements: 7.1, 7.2_
  - [ ] 17.3 Create CloudFront distribution
    - Configure origins for static site and assets
    - Set up HTTPS and caching
    - _Requirements: Infrastructure_
  - [ ] 17.4 Create API Gateway WebSocket API
    - Configure routes: $connect, $disconnect, submitProblem, $default
    - Set route selection expression to `$request.body.action`
    - _Requirements: 4.1, 4.2_
  - [ ] 17.5 Create Lambda functions for WebSocket routes
    - Implement connection handler (store/remove connectionId)
    - Implement problem handler (forward to AgentCore)
    - _Requirements: 4.1, 4.2, 4.4_

- [ ] 18. Deploy and test end-to-end
  - [ ] 18.1 Build and deploy frontend to S3
    - Run `npm run build`
    - Upload to S3, invalidate CloudFront cache
    - _Requirements: All_
  - [ ] 18.2 Test WebSocket connectivity
    - Verify connection establishment
    - Test message flow with mock backend responses
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 19. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

