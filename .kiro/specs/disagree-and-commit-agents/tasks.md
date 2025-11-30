# Implementation Plan

- [ ] 1. Set up project structure and dependencies
  - Create directory structure for orchestrator, experts, memory, and synthesis modules
  - Set up Python 3.11 virtual environment
  - Install Strands framework, boto3, and testing dependencies (pytest, hypothesis)
  - Create agentcore.yaml configuration file
  - _Requirements: 9.1, 9.4, 9.5_

- [ ] 2. Implement Memory Manager with AgentCore Memory integration
  - [ ] 2.1 Create MemoryManager class with session management
    - Implement create_session() method with session ID format `debate_{hash}_{timestamp}`
    - Implement store_response() method with metadata (userId, round, content, timestamp)
    - Implement get_context() method for retrieving previous responses
    - Implement get_full_context() method for synthesis
    - Add retry logic with exponential backoff for API failures
    - _Requirements: 1.1, 1.2, 6.4, 6.5_

  - [ ]* 2.2 Write property test for session ID format
    - **Property 1: Session ID format consistency**
    - **Validates: Requirements 1.1**

  - [ ]* 2.3 Write property test for expert initialization
    - **Property 2: Expert initialization completeness**
    - **Validates: Requirements 1.2**

  - [ ]* 2.4 Write property test for context retrieval
    - **Property 24: Context retrieval completeness**
    - **Property 28: Cumulative context building**
    - **Validates: Requirements 6.1, 6.5**

- [ ] 3. Implement Expert Agents with persona-specific instructions
  - [ ] 3.1 Create Jeff Barr Agent with serverless focus
    - Define Strands Agent with Claude Sonnet 4.1 model
    - Write instruction set emphasizing Lambda, Step Functions, EventBridge
    - Configure response length constraints (~200 words)
    - Add persona-specific language patterns ("Here's the simple approach...")
    - _Requirements: 3.1, 3.3, 3.4_

  - [ ] 3.2 Create Swami Agent with AI/ML and speed focus
    - Define Strands Agent with Claude Sonnet 4.1 model
    - Write instruction set emphasizing Bedrock, SageMaker, rapid iteration
    - Configure response length constraints (~200 words)
    - Add persona-specific language patterns ("We can ship this in weeks...")
    - _Requirements: 4.1, 4.3, 4.4_

  - [ ] 3.3 Create Werner Agent with scale and distributed systems focus
    - Define Strands Agent with Claude Sonnet 4.1 model
    - Write instruction set emphasizing distributed systems, fault tolerance, eventual consistency
    - Configure response length constraints (~200 words)
    - Add persona-specific language patterns ("At scale, we need...")
    - _Requirements: 5.1, 5.3, 5.4_

  - [ ]* 3.4 Write property tests for Jeff Barr persona consistency
    - **Property 12: Jeff Barr serverless emphasis**
    - **Property 14: Jeff Barr response length**
    - **Property 15: Jeff Barr persona consistency**
    - **Validates: Requirements 3.1, 3.3, 3.4**

  - [ ]* 3.5 Write property tests for Swami persona consistency
    - **Property 16: Swami AI/ML emphasis**
    - **Property 18: Swami response length**
    - **Property 19: Swami persona consistency**
    - **Validates: Requirements 4.1, 4.3, 4.4**

  - [ ]* 3.6 Write property tests for Werner persona consistency
    - **Property 20: Werner scale emphasis**
    - **Property 22: Werner response length**
    - **Property 23: Werner persona consistency**
    - **Validates: Requirements 5.1, 5.3, 5.4**

- [ ] 4. Implement Synthesis Agent
  - [ ] 4.1 Create Synthesis Agent with multi-perspective instructions
    - Define Strands Agent with Claude Sonnet 4.1 model
    - Write instruction set for combining all three expert perspectives
    - Add Mermaid diagram generation instructions
    - Configure output format (Architecture Overview, Core Components, Mermaid Diagram, Trade-offs)
    - _Requirements: 7.2, 7.4, 7.5_

  - [ ] 4.2 Implement Mermaid diagram extraction utility
    - Create extract_mermaid() function to parse Mermaid code blocks
    - Add fallback logic for finding graph declarations
    - Validate Mermaid syntax
    - _Requirements: 7.4_

  - [ ]* 4.3 Write property test for synthesis context completeness
    - **Property 29: Synthesis context completeness**
    - **Validates: Requirements 7.1**

  - [ ]* 4.4 Write property test for multi-perspective synthesis
    - **Property 30: Multi-perspective synthesis**
    - **Property 32: Mermaid multi-perspective representation**
    - **Validates: Requirements 7.2, 7.5**

  - [ ]* 4.5 Write property test for Mermaid generation
    - **Property 31: Mermaid diagram generation**
    - **Validates: Requirements 7.4**

- [ ] 5. Implement Text-to-Speech integration with Nova Sonic
  - [ ] 5.1 Create text_to_speech() function
    - Implement Nova Sonic API integration using boto3
    - Create voice profile mapping for each expert (jeff_barr, swami, werner_vogels, neutral)
    - Implement S3 upload for generated audio files
    - Generate presigned URLs for web playback
    - Add error handling with text-only fallback
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [ ] 5.2 Create get_voice_profile() utility function
    - Map expert names to distinct voice profiles
    - Return neutral profile for synthesis
    - _Requirements: 8.2, 8.4_

  - [ ]* 5.3 Write property test for TTS invocation
    - **Property 33: TTS invocation consistency**
    - **Property 34: Voice profile differentiation**
    - **Validates: Requirements 8.1, 8.2**

  - [ ]* 5.4 Write property test for TTS error handling
    - **Property 37: TTS failure resilience**
    - **Validates: Requirements 8.5**

- [ ] 6. Implement Problem Statement management
  - [ ] 6.1 Create problem statement loader
    - Load problem_statements.json configuration file
    - Implement get_problem_by_id() function
    - Validate problem structure (id, title, statement fields)
    - _Requirements: 11.1, 11.2, 11.4_

  - [ ]* 6.2 Write property test for problem lookup
    - **Property 43: Problem lookup correctness**
    - **Validates: Requirements 11.2**

- [ ] 7. Implement Orchestrator Agent core logic
  - [ ] 7.1 Create debate_orchestrator entrypoint function
    - Implement BedrockAgentCoreApp entrypoint decorator
    - Add input validation for problem statements
    - Implement session creation via MemoryManager
    - _Requirements: 1.4, 1.5, 9.1_

  - [ ] 7.2 Implement round execution logic
    - Create execute_round() method for coordinating expert invocations
    - Implement expert invocation ordering (jeff_barr, swami, werner_vogels)
    - Add timing enforcement (60 seconds per expert)
    - Implement context retrieval and distribution
    - _Requirements: 2.1, 2.2, 2.3, 6.1, 6.2_

  - [ ] 7.3 Implement automatic round progression
    - Add logic to automatically start Round 2 after Round 1
    - Add logic to automatically start Round 3 (consensus) after Round 2
    - Trigger synthesis after Round 3 completion
    - _Requirements: 2.4, 2.5, 2.6_

  - [ ]* 7.4 Write property tests for debate flow
    - **Property 6: Round count invariant**
    - **Property 7: Expert invocation ordering**
    - **Property 9: Automatic round progression**
    - **Property 10: Consensus round transition**
    - **Property 11: Synthesis triggering**
    - **Validates: Requirements 2.1, 2.2, 2.4, 2.5, 2.6**

  - [ ]* 7.5 Write property test for input validation
    - **Property 4: Empty input rejection**
    - **Property 5: Valid input session creation**
    - **Validates: Requirements 1.4, 1.5**

- [ ] 8. Implement WebSocket communication
  - [ ] 8.1 Create emit_websocket() function
    - Implement API Gateway Management API integration
    - Add connection ID management
    - Handle GoneException for disconnected clients
    - Add message buffering for reconnection
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ] 8.2 Implement WebSocket message formatting
    - Create message builders for expert_response, status, synthesis_started, synthesis_complete, error
    - Ensure all required fields are included in each message type
    - Add timestamp to all messages
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ]* 8.3 Write property tests for WebSocket messages
    - **Property 38: Expert response message completeness**
    - **Property 39: Status message emission**
    - **Property 40: Synthesis status notification**
    - **Property 41: Synthesis completion message structure**
    - **Property 42: Error message emission without termination**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4, 10.5**

- [ ] 9. Implement error handling and resilience
  - [ ] 9.1 Create error handling utilities
    - Implement RetryConfig class with exponential backoff
    - Create ErrorResponse dataclass
    - Add error logging with CloudWatch integration
    - Implement graceful degradation for agent timeouts
    - _Requirements: 8.5_

  - [ ] 9.2 Add error handling to orchestrator
    - Wrap agent invocations with timeout and retry logic
    - Handle TTS failures with text-only fallback
    - Handle memory service errors with in-memory fallback
    - Emit error messages via WebSocket without terminating session
    - _Requirements: 8.5, 10.5_

  - [ ]* 9.3 Write property test for error resilience
    - **Property 37: TTS failure resilience**
    - **Property 42: Error message emission without termination**
    - **Validates: Requirements 8.5, 10.5**

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Create deployment configuration
  - [ ] 11.1 Create agentcore.yaml for orchestrator deployment
    - Configure Python 3.11 runtime
    - Set memory to 2048 MB
    - Set timeout to 600 seconds
    - Add environment variables (MEMORY_ID, WEBSOCKET_ENDPOINT, NOVA_SONIC_ENDPOINT)
    - Configure IAM permissions for Bedrock, AgentCore Memory, and Polly
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ] 11.2 Create infrastructure deployment scripts
    - Create script to create AgentCore Memory resource
    - Create CloudFormation template for API Gateway WebSocket
    - Create S3 bucket for audio storage with lifecycle policy
    - Add CloudWatch log group configuration
    - _Requirements: 9.1_

- [ ]* 12. Create integration tests
  - Write end-to-end test for full debate flow
  - Test memory persistence across rounds
  - Test TTS pipeline integration
  - Test WebSocket message delivery
  - Test error recovery scenarios

- [ ] 13. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
