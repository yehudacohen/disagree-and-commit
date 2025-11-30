# Requirements Document

## Introduction

The Disagree and Commit Agents system is a multi-agent debate orchestration platform that simulates technical discussions between three AWS expert personas. The system receives complex engineering problems and orchestrates a structured 9-minute debate across three rounds, culminating in a synthesized architecture proposal. The system leverages Amazon Bedrock AgentCore Runtime for deployment, Strands framework for agent implementation, AgentCore Memory for context management, and Amazon Nova Sonic for text-to-speech conversion.

## Glossary

- **Orchestrator Agent**: The master agent responsible for coordinating debate flow, managing timing, and triggering synthesis
- **Expert Agent**: One of three persona-based agents (Jeff Barr, Swami Sivasubramanian, Werner Vogels) that participates in debates
- **Synthesis Agent**: The agent that consumes all debate context and generates unified architecture proposals
- **AgentCore Memory**: Amazon Bedrock's persistent memory service for storing conversation context across debate rounds
- **Memory Session**: A unique conversation context identified by `debate_{problemId}_{timestamp}`
- **Debate Round**: A 3-minute period where each expert speaks for 1 minute sequentially
- **Consensus Round**: The final 3-minute round where experts converge toward agreement
- **Problem Statement**: A complex engineering challenge presented to the expert panel for architectural discussion
- **Nova Sonic**: Amazon's text-to-speech service for converting agent responses to natural speech
- **Strands Framework**: The agent development framework used for building all agents
- **Claude Sonnet 4.1**: The foundation model used for agent reasoning

## Requirements

### Requirement 1

**User Story:** As a user, I want to submit a complex engineering problem to the debate system, so that I can receive diverse architectural perspectives from expert personas.

#### Acceptance Criteria

1. WHEN a user submits a problem statement THEN the Orchestrator Agent SHALL create a new Memory Session with identifier format `debate_{problemId}_{timestamp}`
2. WHEN the Memory Session is created THEN the Orchestrator Agent SHALL initialize context storage for three expert users: jeff_barr, swami, and werner_vogels
3. WHEN the problem statement exceeds 1000 characters THEN the Orchestrator Agent SHALL accept and process the full statement without truncation
4. WHEN the Orchestrator Agent receives the problem THEN the Orchestrator Agent SHALL validate that the problem statement is non-empty before proceeding
5. WHEN validation succeeds THEN the Orchestrator Agent SHALL return a session identifier to the caller for tracking

### Requirement 2

**User Story:** As the orchestrator, I want to coordinate three sequential debate rounds with precise timing, so that each expert has equal opportunity to contribute.

#### Acceptance Criteria

1. WHEN the debate begins THEN the Orchestrator Agent SHALL execute exactly three rounds of 3 minutes each
2. WHEN a debate round starts THEN the Orchestrator Agent SHALL invoke each Expert Agent sequentially in the order: jeff_barr, swami, werner_vogels
3. WHEN an Expert Agent is invoked THEN the Orchestrator Agent SHALL enforce a 1-minute speaking duration per expert
4. WHEN Round 1 completes THEN the Orchestrator Agent SHALL immediately begin Round 2 without user intervention
5. WHEN Round 2 completes THEN the Orchestrator Agent SHALL immediately begin Round 3 with consensus instructions
6. WHEN all three rounds complete THEN the Orchestrator Agent SHALL trigger the Synthesis Agent with full debate context

### Requirement 3

**User Story:** As Jeff Barr, I want to advocate for serverless and managed AWS services, so that I can push the architecture toward simplicity.

#### Acceptance Criteria

1. WHEN Jeff Barr Agent receives a problem statement THEN the Jeff Barr Agent SHALL generate a response emphasizing AWS Lambda, Step Functions, and EventBridge
2. WHEN Jeff Barr Agent reviews previous expert responses THEN the Jeff Barr Agent SHALL challenge over-engineered solutions with simpler managed service alternatives
3. WHEN Jeff Barr Agent generates a response THEN the Jeff Barr Agent SHALL limit output to approximately 200 words for 1-minute speech duration
4. WHEN Jeff Barr Agent speaks THEN the Jeff Barr Agent SHALL begin responses with phrases like "Here's the simple approach..." to maintain persona consistency
5. WHEN Jeff Barr Agent encounters infrastructure management proposals THEN the Jeff Barr Agent SHALL counter with serverless alternatives

### Requirement 4

**User Story:** As Swami Sivasubramanian, I want to prioritize rapid deployment and AI/ML solutions, so that I can drive the architecture toward fast time-to-market.

#### Acceptance Criteria

1. WHEN Swami Agent receives a problem statement THEN the Swami Agent SHALL generate responses emphasizing Amazon Bedrock, SageMaker, and rapid iteration
2. WHEN Swami Agent reviews previous expert responses THEN the Swami Agent SHALL challenge slow or perfectionist approaches with MVP-focused alternatives
3. WHEN Swami Agent generates a response THEN the Swami Agent SHALL limit output to approximately 200 words for 1-minute speech duration
4. WHEN Swami Agent speaks THEN the Swami Agent SHALL begin responses with phrases like "We can ship this in weeks..." to maintain persona consistency
5. WHEN Swami Agent encounters complex planning proposals THEN the Swami Agent SHALL advocate for shipping quickly and iterating in production

### Requirement 5

**User Story:** As Werner Vogels, I want to ensure architectures scale to billions of requests, so that I can drive the design toward distributed systems and fault tolerance.

#### Acceptance Criteria

1. WHEN Werner Agent receives a problem statement THEN the Werner Agent SHALL generate responses emphasizing distributed systems, eventual consistency, and fault tolerance
2. WHEN Werner Agent reviews previous expert responses THEN the Werner Agent SHALL identify single points of failure and scale bottlenecks
3. WHEN Werner Agent generates a response THEN the Werner Agent SHALL limit output to approximately 200 words for 1-minute speech duration
4. WHEN Werner Agent speaks THEN the Werner Agent SHALL begin responses with phrases like "At scale, we need..." to maintain persona consistency
5. WHEN Werner Agent encounters centralized architecture proposals THEN the Werner Agent SHALL counter with distributed alternatives

### Requirement 6

**User Story:** As an expert agent, I want to access previous debate context from AgentCore Memory, so that I can build upon and respond to other experts' arguments.

#### Acceptance Criteria

1. WHEN an Expert Agent is invoked for Round 2 or Round 3 THEN the Orchestrator Agent SHALL retrieve all previous responses from the Memory Session
2. WHEN context is retrieved THEN the Orchestrator Agent SHALL format it as a chronological conversation showing agent name, round number, and content
3. WHEN an Expert Agent receives context THEN the Expert Agent SHALL reference specific points from previous experts in the current response
4. WHEN storing a response THEN the Orchestrator Agent SHALL persist it to AgentCore Memory with metadata including userId, round number, and timestamp
5. WHEN multiple experts have spoken THEN the Orchestrator Agent SHALL ensure each subsequent expert receives cumulative context from all previous speakers

### Requirement 7

**User Story:** As the synthesis agent, I want to consume all debate rounds from memory, so that I can create a unified architecture that honors all three perspectives.

#### Acceptance Criteria

1. WHEN the Synthesis Agent is triggered THEN the Synthesis Agent SHALL retrieve all responses from all three rounds for all three experts from the Memory Session
2. WHEN generating synthesis THEN the Synthesis Agent SHALL incorporate serverless principles from Jeff Barr, speed-to-market from Swami, and scale considerations from Werner
3. WHEN creating the architecture THEN the Synthesis Agent SHALL produce a comprehensive but functional design that balances all three perspectives
4. WHEN synthesis completes THEN the Synthesis Agent SHALL generate a Mermaid flowchart diagram showing the AWS services architecture
5. WHEN the Mermaid diagram is generated THEN the Synthesis Agent SHALL include services advocated by all three experts in the visual representation

### Requirement 8

**User Story:** As a user, I want agent responses converted to natural speech, so that I can experience the debate as a realistic conversation.

#### Acceptance Criteria

1. WHEN an Expert Agent generates a text response THEN the Orchestrator Agent SHALL invoke Amazon Nova Sonic to convert text to speech
2. WHEN invoking Nova Sonic THEN the Orchestrator Agent SHALL apply distinct voice characteristics for each expert persona
3. WHEN speech is generated THEN the Orchestrator Agent SHALL return audio in a streaming format compatible with web playback
4. WHEN the Synthesis Agent generates output THEN the Orchestrator Agent SHALL convert the synthesis text to speech using a neutral voice profile
5. WHEN audio generation fails THEN the Orchestrator Agent SHALL return the text response and log the error without blocking the debate flow

### Requirement 9

**User Story:** As a developer, I want all agents deployed on Amazon Bedrock AgentCore Runtime, so that the system benefits from serverless scaling and managed infrastructure.

#### Acceptance Criteria

1. WHEN deploying the Orchestrator Agent THEN the deployment system SHALL package it as a BedrockAgentCoreApp with Python 3.11 runtime
2. WHEN deploying Expert Agents THEN the deployment system SHALL configure each agent with Claude Sonnet 4.1 as the reasoning model
3. WHEN deploying the Synthesis Agent THEN the deployment system SHALL configure it with Claude Sonnet 4.1 and synthesis-specific instructions
4. WHEN configuring memory THEN the deployment system SHALL set the MEMORY_ID environment variable to reference the AgentCore Memory resource
5. WHEN setting timeouts THEN the deployment system SHALL configure a 600-second timeout to accommodate the full 9-minute debate plus synthesis

### Requirement 10

**User Story:** As a frontend developer, I want to receive structured WebSocket messages during the debate, so that I can update the UI in real-time as each expert speaks.

#### Acceptance Criteria

1. WHEN an Expert Agent completes a response THEN the Orchestrator Agent SHALL emit a WebSocket message containing agent name, round number, text content, and audio URL
2. WHEN the debate progresses THEN the Orchestrator Agent SHALL emit status messages indicating current round and active speaker
3. WHEN synthesis begins THEN the Orchestrator Agent SHALL emit a message indicating synthesis is in progress
4. WHEN synthesis completes THEN the Orchestrator Agent SHALL emit a message containing the full synthesis text, Mermaid diagram code, and session identifier
5. WHEN an error occurs THEN the Orchestrator Agent SHALL emit an error message with error type and description without terminating the session

### Requirement 11

**User Story:** As a system administrator, I want the debate system to handle three predefined problem statements, so that users can quickly experience the system with curated scenarios.

#### Acceptance Criteria

1. WHEN the system initializes THEN the Orchestrator Agent SHALL load problem statements from a configuration file containing mars_currency, air_taxi_pollution, and personal_air_taxi scenarios
2. WHEN a user requests a problem by identifier THEN the Orchestrator Agent SHALL retrieve the full problem statement text and pass it to the debate flow
3. WHEN a user submits a custom problem THEN the Orchestrator Agent SHALL accept and process it using the same debate flow as predefined problems
4. WHEN problem statements are stored THEN the configuration SHALL include problem id, title, and full statement text with technical considerations
5. WHEN the Orchestrator Agent processes any problem THEN the Orchestrator Agent SHALL apply identical debate rules regardless of problem source

### Requirement 12

**User Story:** As a developer, I want clear separation between orchestration, expert reasoning, memory management, and synthesis, so that the system is maintainable and testable.

#### Acceptance Criteria

1. WHEN implementing the Orchestrator Agent THEN the system SHALL isolate orchestration logic from expert agent implementations
2. WHEN implementing Expert Agents THEN the system SHALL define each agent with independent instruction sets and model configurations
3. WHEN implementing memory operations THEN the system SHALL encapsulate all AgentCore Memory API calls in a dedicated MemoryManager class
4. WHEN implementing the Synthesis Agent THEN the system SHALL separate synthesis logic from debate orchestration
5. WHEN modifying an Expert Agent persona THEN the system SHALL allow changes without affecting orchestration or other agents
