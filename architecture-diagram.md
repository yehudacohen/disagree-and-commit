# Disagree-and-Commit System Architecture Diagram

## High-Level Architecture

```mermaid
graph TB
    subgraph "Input Layer"
        User[User/API Request]
        Problem[Problem Statement]
    end
    
    subgraph "AgentCore Runtime Environment"
        Orchestrator[Orchestrator Agent<br/>Coordinates Debate Flow]
        
        subgraph "Expert Agents"
            Jeff[Jeff Barr Agent<br/>Serverless Expert<br/>Claude Sonnet 4]
            Swami[Swami Agent<br/>AI/ML Expert<br/>Claude Sonnet 4]
            Werner[Werner Vogels Agent<br/>Scale Expert<br/>Claude Sonnet 4]
        end
    end
    
    subgraph "Memory Layer"
        Memory[(AgentCore Memory<br/>Session-based Storage<br/>Actor Context)]
    end
    
    subgraph "Storage Layer"
        S3Markdown[S3 Bucket<br/>road-to-reinvent-redteam<br/>{sessionId}/conversation_response/<br/>debate_synthesis.md]
        S3Audio[S3 Bucket<br/>road-to-reinvent-redteam<br/>{sessionId}/audio_response/<br/>debate_synthesis.mp3]
    end
    
    subgraph "Processing Layer"
        Lambda[Lambda Function<br/>Audio Converter<br/>Python 3.11]
        Polly[Amazon Polly<br/>Neural Voice<br/>Text-to-Speech]
    end
    
    User -->|POST /debate| Problem
    Problem -->|1. Problem Statement| Orchestrator
    
    Orchestrator -->|2. Round 1-3<br/>Invoke with Context| Jeff
    Orchestrator -->|2. Round 1-3<br/>Invoke with Context| Swami
    Orchestrator -->|2. Round 1-3<br/>Invoke with Context| Werner
    
    Jeff -->|3. Store Response<br/>create_event| Memory
    Swami -->|3. Store Response<br/>create_event| Memory
    Werner -->|3. Store Response<br/>create_event| Memory
    
    Memory -->|4. Retrieve Context<br/>retrieve_memory| Jeff
    Memory -->|4. Retrieve Context<br/>retrieve_memory| Swami
    Memory -->|4. Retrieve Context<br/>retrieve_memory| Werner
    
    Orchestrator -->|5. Get Full Context<br/>All Rounds| Memory
    Orchestrator -->|6. Generate Synthesis<br/>Markdown Document| S3Markdown
    
    S3Markdown -->|7. S3 Event<br/>ObjectCreated| Lambda
    Lambda -->|8. Read Markdown| S3Markdown
    Lambda -->|9. Convert Text| Polly
    Polly -->|10. Audio Stream| Lambda
    Lambda -->|11. Upload MP3| S3Audio
    
    Orchestrator -->|12. Return Response| User
    
    style Orchestrator fill:#FF9900
    style Jeff fill:#232F3E
    style Swami fill:#232F3E
    style Werner fill:#232F3E
    style Memory fill:#3F8624
    style S3Markdown fill:#569A31
    style S3Audio fill:#569A31
    style Lambda fill:#FF9900
    style Polly fill:#FF9900
```

## Detailed Debate Flow

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator
    participant Jeff as Jeff Barr Agent
    participant Swami as Swami Agent
    participant Werner as Werner Agent
    participant Memory as AgentCore Memory
    participant S3 as S3 Bucket
    participant Lambda as Lambda Function
    participant Polly as Amazon Polly
    
    User->>Orchestrator: Problem Statement
    Orchestrator->>Memory: Create Session
    
    Note over Orchestrator,Werner: Round 1: Initial Positions
    
    Orchestrator->>Jeff: Invoke with Problem
    Jeff->>Memory: Store Response (Round 1)
    Memory-->>Orchestrator: Stored
    
    Orchestrator->>Memory: Get Context for Swami
    Memory-->>Orchestrator: Jeff's Response
    Orchestrator->>Swami: Invoke with Problem + Context
    Swami->>Memory: Store Response (Round 1)
    Memory-->>Orchestrator: Stored
    
    Orchestrator->>Memory: Get Context for Werner
    Memory-->>Orchestrator: Jeff + Swami Responses
    Orchestrator->>Werner: Invoke with Problem + Context
    Werner->>Memory: Store Response (Round 1)
    Memory-->>Orchestrator: Stored
    
    Note over Orchestrator,Werner: Round 2: Rebuttals
    
    Orchestrator->>Memory: Get Full Context
    Memory-->>Orchestrator: All Round 1 Responses
    
    Orchestrator->>Jeff: Invoke with Context
    Jeff->>Memory: Store Response (Round 2)
    
    Orchestrator->>Swami: Invoke with Context
    Swami->>Memory: Store Response (Round 2)
    
    Orchestrator->>Werner: Invoke with Context
    Werner->>Memory: Store Response (Round 2)
    
    Note over Orchestrator,Werner: Round 3: Consensus
    
    Orchestrator->>Memory: Get Full Context
    Memory-->>Orchestrator: All Round 1-2 Responses
    
    Orchestrator->>Jeff: Invoke with Context
    Jeff->>Memory: Store Response (Round 3)
    
    Orchestrator->>Swami: Invoke with Context
    Swami->>Memory: Store Response (Round 3)
    
    Orchestrator->>Werner: Invoke with Context
    Werner->>Memory: Store Response (Round 3)
    
    Note over Orchestrator,Polly: Synthesis & Audio Generation
    
    Orchestrator->>Memory: Get Complete Transcript
    Memory-->>Orchestrator: All 3 Rounds
    
    Orchestrator->>Orchestrator: Generate Synthesis
    Orchestrator->>S3: Upload Markdown
    S3-->>Orchestrator: Upload Complete
    
    S3->>Lambda: S3 Event Trigger
    Lambda->>S3: Read Markdown
    S3-->>Lambda: Markdown Content
    
    Lambda->>Polly: Synthesize Speech
    Polly-->>Lambda: Audio Stream
    
    Lambda->>S3: Upload MP3
    S3-->>Lambda: Upload Complete
    
    Orchestrator->>User: Return Response<br/>(sessionId, s3Paths, status)
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Input"
        A[Problem Statement]
    end
    
    subgraph "Debate Process"
        B[Round 1: Positions]
        C[Round 2: Rebuttals]
        D[Round 3: Consensus]
    end
    
    subgraph "Memory Storage"
        E[(Session Context<br/>Actor Responses<br/>Round Metadata)]
    end
    
    subgraph "Synthesis"
        F[Combine Perspectives]
        G[Generate Mermaid]
        H[Create Markdown]
    end
    
    subgraph "Storage"
        I[S3: Markdown File]
    end
    
    subgraph "Audio Processing"
        J[Parse Markdown]
        K[Text Chunks]
        L[Polly Synthesis]
        M[Combine Audio]
    end
    
    subgraph "Output"
        N[S3: MP3 File]
        O[Response Metadata]
    end
    
    A --> B
    B --> E
    E --> C
    C --> E
    E --> D
    D --> E
    
    E --> F
    F --> G
    G --> H
    H --> I
    
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    
    I --> O
    N --> O
```

## Component Interaction Matrix

| Component | Interacts With | Protocol/API | Purpose |
|-----------|---------------|--------------|---------|
| Orchestrator | Expert Agents | Strands SDK | Invoke agents with prompts |
| Expert Agents | AgentCore Memory | bedrock-agent-runtime | Store responses |
| Expert Agents | AgentCore Memory | bedrock-agent-runtime | Retrieve context |
| Orchestrator | AgentCore Memory | bedrock-agent-runtime | Get full transcript |
| Orchestrator | S3 | boto3 s3 | Upload markdown |
| S3 | Lambda | Event Notification | Trigger on upload |
| Lambda | S3 | boto3 s3 | Read markdown |
| Lambda | Polly | boto3 polly | Convert to speech |
| Lambda | S3 | boto3 s3 | Upload audio |

## Technology Stack

```mermaid
graph TB
    subgraph "AI/ML Layer"
        A1[Claude Sonnet 4<br/>via Bedrock]
        A2[Amazon Polly<br/>Neural Voices]
    end
    
    subgraph "Application Layer"
        B1[Strands SDK<br/>Agent Framework]
        B2[Python 3.11<br/>Lambda Runtime]
    end
    
    subgraph "Compute Layer"
        C1[AgentCore Runtime<br/>Serverless Agents]
        C2[AWS Lambda<br/>Event Processing]
    end
    
    subgraph "Storage Layer"
        D1[AgentCore Memory<br/>Conversation History]
        D2[Amazon S3<br/>Documents & Audio]
    end
    
    subgraph "Infrastructure"
        E1[IAM<br/>Access Control]
        E2[CloudWatch<br/>Monitoring]
        E3[X-Ray<br/>Tracing]
    end
    
    A1 --> B1
    A2 --> B2
    B1 --> C1
    B2 --> C2
    C1 --> D1
    C2 --> D2
    D1 --> E2
    D2 --> E2
    C1 --> E3
    C2 --> E3
    E1 --> C1
    E1 --> C2
```
