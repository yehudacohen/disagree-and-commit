# Requirements Document

## Introduction

This specification defines the requirements for the disagree-and-commit agents system that orchestrates debates between three AWS expert personas (Jeff Barr, Swami Sivasubramanian, and Werner Vogels). The system uses Strands SDK, AgentCore Runtime, and AgentCore Memory for debate orchestration, stores conversation transcripts in S3, and automatically converts them to audio using Amazon Polly via Lambda.

## Glossary

- **Strands SDK**: The AWS agent framework for building AI agents with Bedrock models
- **AgentCore Runtime**: AWS serverless runtime environment for deploying agents
- **AgentCore Memory**: AWS managed memory service for agent conversation history
- **BedrockModel**: Strands model class for AWS Bedrock foundation models
- **Agent**: Strands agent class that combines model, system prompt, and tools
- **Orchestrator Agent**: Main coordinator that processes problem statements and manages debate flow
- **Expert Persona Agents**: Three agents representing Jeff Barr, Swami Sivasubramanian, and Werner Vogels
- **Synthesis**: Process of combining all expert perspectives into a unified architecture document
- **Session**: A unique debate instance with a specific problem statement
- **S3 Bucket**: Storage location for markdown transcripts and audio files (road-to-reinvent-redteam)
- **Lambda Function**: Event-driven function that converts markdown to audio using Polly
- **Amazon Polly**: AWS text-to-speech service with neural voices

## Requirements

### Requirement 1: Orchestrator Agent

**User Story:** As a user, I want an orchestrator agent that coordinates the debate process, so that problem statements are systematically debated by expert personas.

#### Acceptance Criteria

1. WHEN receiving a problem statement THEN the system SHALL create a unique session with format "debate_<hash>_<timestamp>"
2. WHEN orchestrating debates THEN the system SHALL execute exactly 3 rounds (2 debate rounds + 1 consensus round)
3. WHEN invoking expert agents THEN the system SHALL call each agent sequentially in each round
4. WHEN a round completes THEN the system SHALL store all responses in AgentCore Memory before proceeding
5. WHEN all rounds complete THEN the system SHALL generate a synthesis document combining all perspectives
6. WHEN synthesis completes THEN the system SHALL upload the markdown document to S3
7. WHEN returning results THEN the system SHALL include sessionId, status, synthesis, mermaidDiagram, and s3Paths

### Requirement 2: Expert Persona Agents

**User Story:** As a system, I want three distinct expert persona agents, so that diverse perspectives are represented in debates.

#### Acceptance Criteria

1. WHEN creating expert agents THEN the system SHALL define Jeff Barr agent with serverless and simplicity focus
2. WHEN creating expert agents THEN the system SHALL define Swami Sivasubramanian agent with AI/ML and innovation focus
3. WHEN creating expert agents THEN the system SHALL define Werner Vogels agent with scale and distributed systems focus
4. WHEN configuring agents THEN the system SHALL use BedrockModel with model_id "us.anthropic.claude-sonnet-4-20250514-v1:0"
5. WHEN configuring agents THEN the system SHALL set temperature=0.7 and max_tokens=2048
6. WHEN invoking agents THEN the system SHALL use agent(prompt) pattern and extract response.message['content'][0]['text']
7. WHEN agents respond THEN the system SHALL limit responses to approximately 200 words per round

### Requirement 3: AgentCore Memory Integration

**User Story:** As a system, I want to store all debate conversations in AgentCore Memory, so that context is preserved across rounds and can be retrieved for synthesis.

#### Acceptance Criteria

1. WHEN creating a session THEN the system SHALL generate a session ID with minimum 33 characters
2. WHEN storing responses THEN the system SHALL use bedrock-agent-runtime client's create_event method
3. WHEN storing responses THEN the system SHALL include actorId (agent name), sessionId, and round metadata
4. WHEN retrieving context THEN the system SHALL use bedrock-agent-runtime client's retrieve_memory method
5. WHEN retrieving context THEN the system SHALL filter by actorId to get agent-specific history
6. WHEN formatting messages THEN the system SHALL use structure with role ("USER" or "ASSISTANT") and text fields
7. WHEN synthesis begins THEN the system SHALL retrieve complete transcript from all actors and all rounds

### Requirement 4: Synthesis Generation

**User Story:** As a system, I want to generate a comprehensive synthesis document, so that all expert perspectives are combined into a unified architecture.

#### Acceptance Criteria

1. WHEN generating synthesis THEN the system SHALL retrieve complete debate transcript from AgentCore Memory
2. WHEN generating synthesis THEN the system SHALL include problem statement, all rounds, and expert responses
3. WHEN generating synthesis THEN the system SHALL create a unified architecture combining all perspectives
4. WHEN generating synthesis THEN the system SHALL generate a Mermaid diagram showing the architecture
5. WHEN generating synthesis THEN the system SHALL analyze trade-offs between competing approaches
6. WHEN formatting synthesis THEN the system SHALL use markdown format with clear sections
7. WHEN synthesis completes THEN the system SHALL return both full text and extracted Mermaid diagram

### Requirement 5: S3 Storage Integration

**User Story:** As a system, I want to store debate transcripts in S3, so that they are persistently available and can trigger downstream processing.

#### Acceptance Criteria

1. WHEN uploading documents THEN the system SHALL use S3 bucket "road-to-reinvent-redteam"
2. WHEN uploading documents THEN the system SHALL use path structure "{sessionId}/conversation_response/debate_synthesis.md"
3. WHEN uploading documents THEN the system SHALL set ContentType to "text/markdown"
4. WHEN uploading documents THEN the system SHALL include metadata with session-id, timestamp, and status
5. WHEN upload completes THEN the system SHALL return the S3 path in the response
6. WHEN upload fails THEN the system SHALL log error and return error status without crashing

### Requirement 6: Lambda Audio Converter

**User Story:** As a system, I want to automatically convert markdown transcripts to audio, so that debates are available in audio format.

#### Acceptance Criteria

1. WHEN markdown is uploaded to S3 THEN the system SHALL trigger Lambda function via S3 event notification
2. WHEN Lambda executes THEN the system SHALL read markdown content from S3
3. WHEN processing markdown THEN the system SHALL convert markdown to plain text
4. WHEN converting to audio THEN the system SHALL use Amazon Polly with neural voice
5. WHEN calling Polly THEN the system SHALL handle text chunks up to 3000 characters
6. WHEN audio is generated THEN the system SHALL upload MP3 to "{sessionId}/audio_response/debate_synthesis.mp3"
7. WHEN upload completes THEN the system SHALL include metadata with session-id, source-markdown, and duration

### Requirement 7: AgentCore Runtime Deployment

**User Story:** As a developer, I want the orchestrator deployable to AgentCore Runtime, so that it runs as a serverless, scalable agent.

#### Acceptance Criteria

1. WHEN defining the entrypoint THEN the system SHALL use @app.entrypoint decorator
2. WHEN handling requests THEN the system SHALL accept payload dict with problem, problemId, and actor_id
3. WHEN returning responses THEN the system SHALL return dict with sessionId, status, synthesis, mermaidDiagram, and s3Paths
4. WHEN initializing the app THEN the system SHALL use BedrockAgentCoreApp from bedrock_agentcore.runtime
5. WHEN running locally THEN the system SHALL support app.run() for testing

### Requirement 8: Error Handling and Resilience

**User Story:** As a system, I want robust error handling, so that failures in one component don't crash the entire debate process.

#### Acceptance Criteria

1. WHEN agent invocation fails THEN the system SHALL catch exception, log error, and use fallback message
2. WHEN memory operation fails THEN the system SHALL log error and continue debate execution
3. WHEN S3 upload fails THEN the system SHALL log error and return error status in response
4. WHEN Lambda execution fails THEN the system SHALL log error but not block orchestrator response
5. WHEN response extraction fails THEN the system SHALL catch KeyError/TypeError/IndexError and use fallback
6. WHEN environment variables are missing THEN the system SHALL use defaults and log warnings

### Requirement 9: Configuration and Environment

**User Story:** As a developer, I want proper configuration management, so that the system works in different environments.

#### Acceptance Criteria

1. WHEN deploying orchestrator THEN the system SHALL read MEMORY_ID from environment variables
2. WHEN deploying orchestrator THEN the system SHALL read S3_BUCKET from environment variables with default "road-to-reinvent-redteam"
3. WHEN deploying orchestrator THEN the system SHALL read MODEL_ID from environment with default "us.anthropic.claude-sonnet-4-20250514-v1:0"
4. WHEN deploying orchestrator THEN the system SHALL read AWS_REGION from environment with default "us-east-1"
5. WHEN deploying Lambda THEN the system SHALL read POLLY_VOICE_ID from environment with default "Matthew"
6. WHEN deploying Lambda THEN the system SHALL read POLLY_ENGINE from environment with default "neural"
7. WHEN logging THEN the system SHALL use proper logging configuration with timestamps and log levels

### Requirement 10: Monitoring and Observability

**User Story:** As an operator, I want comprehensive monitoring, so that I can track system health and debug issues.

#### Acceptance Criteria

1. WHEN agents are invoked THEN the system SHALL log invocation with agent name and round number
2. WHEN memory operations occur THEN the system SHALL log success/failure with session and actor details
3. WHEN S3 uploads occur THEN the system SHALL log upload status with bucket and key
4. WHEN Lambda executes THEN the system SHALL log processing steps and Polly API calls
5. WHEN errors occur THEN the system SHALL log error type, message, and stack trace
6. WHEN operations complete THEN the system SHALL log duration and status
