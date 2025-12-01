# Disagree-and-Commit Agents Architecture

## System Overview

The Disagree-and-Commit system orchestrates debates between three AWS expert personas (Jeff Barr, Swami Sivasubramanian, and Werner Vogels) on technical problem statements. The system stores conversation history in AgentCore Memory, generates synthesis documents in S3, and automatically converts them to audio using Amazon Polly.

## Architecture Components

### 1. Orchestrator Agent (AgentCore Runtime)
**Purpose:** Main coordinator that processes problem statements and manages the debate flow

**Responsibilities:**
- Receives problem statement as input
- Coordinates 3 rounds of debate between expert agents
- Stores all conversations in AgentCore Memory
- Generates final synthesis document
- Uploads markdown response to S3
- Returns session metadata

**Technology:**
- Strands SDK with BedrockModel (Claude Sonnet 4)
- AgentCore Runtime for serverless deployment
- AgentCore Memory for conversation persistence

### 2. Expert Persona Agents (3 Agents)

#### Jeff Barr Agent
**Persona:** Serverless advocate, simplicity-focused, developer experience champion
**Focus:** Lambda, EventBridge, serverless patterns, developer productivity

#### Swami Sivasubramanian Agent
**Persona:** AI/ML innovator, speed-to-market advocate, cutting-edge technology
**Focus:** Bedrock, SageMaker, AI/ML services, rapid innovation

#### Werner Vogels Agent
**Persona:** Distributed systems architect, scale expert, reliability champion
**Focus:** DynamoDB, distributed patterns, global scale, operational excellence

**Common Characteristics:**
- Each agent uses Claude Sonnet 4 via BedrockModel
- Maintains conversation context via AgentCore Memory
- Responds in ~200 words per round
- Engages in constructive debate with other personas

### 3. AgentCore Memory
**Purpose:** Persistent storage for all debate conversations

**Storage Pattern:**
- Session-based memory with unique session IDs
- Actor-based context (one per expert agent)
- Event-driven storage using `create_event` API
- Context retrieval using `retrieve_memory` API

**Data Structure:**
```python
{
    "memoryId": "memory-resource-id",
    "sessionId": "debate_<hash>_<timestamp>",
    "actorId": "jeff_barr" | "swami" | "werner_vogels",
    "messages": [
        {"role": "USER", "text": "Problem statement and context"},
        {"role": "ASSISTANT", "text": "Agent response"}
    ]
}
```

### 4. S3 Storage Layer
**Bucket:** `road-to-reinvent-redteam`

**Directory Structure:**
```
road-to-reinvent-redteam/
├── {sessionId}/
│   ├── conversation_response/
│   │   └── debate_synthesis.md
│   └── audio_response/
│       └── debate_synthesis.mp3
```

**Markdown Document Contents:**
- Problem statement
- Complete debate transcript (all 3 rounds)
- Final synthesis combining all perspectives
- Mermaid architecture diagram
- Trade-offs analysis

### 5. Lambda Function (Audio Converter)
**Trigger:** S3 Event Notification on markdown file upload

**Process Flow:**
1. Triggered when markdown file uploaded to `{sessionId}/conversation_response/`
2. Reads markdown content from S3
3. Converts markdown to plain text (strips formatting)
4. Calls Amazon Polly to synthesize speech
5. Uploads MP3 file to `{sessionId}/audio_response/`
6. Updates metadata/status (optional)

**Technology:**
- Python 3.11+ runtime
- boto3 for S3 and Polly integration
- Markdown parsing library (e.g., markdown2, mistune)

**Polly Configuration:**
- Voice: Neural voice (e.g., Matthew, Joanna, or Ruth)
- Engine: Neural
- Output format: MP3
- Sample rate: 24000 Hz

## System Flow Diagram

```mermaid
graph TB
    User[User/API] -->|Problem Statement| Orchestrator[Orchestrator Agent<br/>AgentCore Runtime]
    
    Orchestrator -->|Round 1-3| Jeff[Jeff Barr Agent<br/>Serverless Expert]
    Orchestrator -->|Round 1-3| Swami[Swami Agent<br/>AI/ML Expert]
    Orchestrator -->|Round 1-3| Werner[Werner Vogels Agent<br/>Scale Expert]
    
    Jeff -->|Store Response| Memory[(AgentCore Memory)]
    Swami -->|Store Response| Memory
    Werner -->|Store Response| Memory
    
    Memory -->|Retrieve Context| Jeff
    Memory -->|Retrieve Context| Swami
    Memory -->|Retrieve Context| Werner
    
    Orchestrator -->|Get Full Context| Memory
    Orchestrator -->|Generate Synthesis| Synthesis[Synthesis Process]
    
    Synthesis -->|Upload MD| S3[S3 Bucket<br/>road-to-reinvent-redteam/<br/>{sessionId}/conversation_response/]
    
    S3 -->|S3 Event Trigger| Lambda[Lambda Function<br/>Audio Converter]
    
    Lambda -->|Read MD| S3
    Lambda -->|Convert to Speech| Polly[Amazon Polly<br/>Neural Voice]
    Polly -->|Audio Stream| Lambda
    Lambda -->|Upload MP3| S3Audio[S3 Bucket<br/>road-to-reinvent-redteam/<br/>{sessionId}/audio_response/]
    
    Orchestrator -->|Return| Response[Response<br/>sessionId, status, s3Paths]
    
    subgraph "AgentCore Runtime"
        Orchestrator
        Jeff
        Swami
        Werner
    end
    
    subgraph "Storage Layer"
        Memory
        S3
        S3Audio
    end
    
    subgraph "Post-Processing"
        Lambda
        Polly
    end
```

## Detailed Component Interactions

### Phase 1: Debate Orchestration

**Input:**
```json
{
    "problem": "Design a serverless architecture for real-time analytics",
    "problemId": "optional-predefined-id",
    "actor_id": "orchestrator"
}
```

**Process:**
1. **Session Creation**
   - Generate unique session ID: `debate_<hash>_<timestamp>`
   - Create session in AgentCore Memory
   - Initialize context for each expert agent

2. **Round 1: Initial Positions (Debate)**
   - Orchestrator invokes Jeff → stores response in Memory
   - Orchestrator invokes Swami → stores response in Memory
   - Orchestrator invokes Werner → stores response in Memory
   - Each agent sees cumulative context from previous responses

3. **Round 2: Rebuttals (Debate)**
   - Each agent retrieves full context from Round 1
   - Agents respond to each other's positions
   - Responses stored in Memory with round metadata

4. **Round 3: Consensus Building**
   - Each agent retrieves full context from Rounds 1-2
   - Agents work toward agreement and synthesis
   - Final positions stored in Memory

### Phase 2: Synthesis Generation

**Process:**
1. Orchestrator retrieves complete debate transcript from Memory
2. Synthesis agent processes all responses
3. Generates comprehensive markdown document:
   - Architecture overview
   - Core components from all perspectives
   - Mermaid diagram showing unified architecture
   - Trade-offs analysis

**Markdown Structure:**
```markdown
# Debate Synthesis: {Problem Statement}

## Session Information
- Session ID: {sessionId}
- Date: {timestamp}
- Participants: Jeff Barr, Swami Sivasubramanian, Werner Vogels

## Problem Statement
{original problem}

## Debate Transcript

### Round 1: Initial Positions
**Jeff Barr (Serverless Advocate):**
{response}

**Swami Sivasubramanian (AI/ML Innovator):**
{response}

**Werner Vogels (Scale Architect):**
{response}

### Round 2: Rebuttals
...

### Round 3: Consensus
...

## Unified Architecture

### Overview
{synthesis of all perspectives}

### Core Components
{combined architecture elements}

### Mermaid Diagram
```mermaid
{architecture diagram}
```

### Trade-offs
{analysis of competing concerns}
```

### Phase 3: S3 Storage

**Upload Process:**
1. Orchestrator uploads markdown to S3:
   - Bucket: `road-to-reinvent-redteam`
   - Key: `{sessionId}/conversation_response/debate_synthesis.md`
   - Metadata: session_id, timestamp, status

2. S3 Event Notification triggers Lambda function

**S3 Configuration:**
```python
s3_client.put_object(
    Bucket='road-to-reinvent-redteam',
    Key=f'{session_id}/conversation_response/debate_synthesis.md',
    Body=markdown_content,
    ContentType='text/markdown',
    Metadata={
        'session-id': session_id,
        'timestamp': timestamp,
        'status': 'complete'
    }
)
```

### Phase 4: Audio Conversion (Lambda)

**Lambda Function Flow:**

```python
def lambda_handler(event, context):
    # 1. Extract S3 event details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # 2. Read markdown from S3
    markdown_content = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
    
    # 3. Convert markdown to plain text
    plain_text = markdown_to_text(markdown_content)
    
    # 4. Split text into chunks (Polly has 3000 character limit per request)
    chunks = split_text(plain_text, max_length=3000)
    
    # 5. Convert each chunk to audio using Polly
    audio_segments = []
    for chunk in chunks:
        response = polly_client.synthesize_speech(
            Text=chunk,
            OutputFormat='mp3',
            VoiceId='Matthew',
            Engine='neural',
            SampleRate='24000'
        )
        audio_segments.append(response['AudioStream'].read())
    
    # 6. Combine audio segments
    combined_audio = combine_audio_segments(audio_segments)
    
    # 7. Upload MP3 to S3
    session_id = extract_session_id(key)
    output_key = f'{session_id}/audio_response/debate_synthesis.mp3'
    
    s3_client.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=combined_audio,
        ContentType='audio/mpeg',
        Metadata={
            'session-id': session_id,
            'source-markdown': key,
            'duration': str(calculate_duration(combined_audio))
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Audio conversion complete',
            'output_key': output_key
        })
    }
```

**Lambda Configuration:**
- Memory: 512 MB (sufficient for audio processing)
- Timeout: 5 minutes (handles long debates)
- Environment Variables:
  - `BUCKET_NAME`: road-to-reinvent-redteam
  - `POLLY_VOICE_ID`: Matthew (or configurable)
  - `POLLY_ENGINE`: neural

**IAM Permissions:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::road-to-reinvent-redteam/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "polly:SynthesizeSpeech"
            ],
            "Resource": "*"
        }
    ]
}
```

## Orchestrator Response Structure

**Success Response:**
```json
{
    "status": "complete",
    "sessionId": "debate_abc123_1701234567",
    "actor_id": "orchestrator",
    "synthesis": "Full synthesis text...",
    "mermaidDiagram": "graph TB\n  ...",
    "s3Paths": {
        "markdown": "road-to-reinvent-redteam/debate_abc123_1701234567/conversation_response/debate_synthesis.md",
        "audio": "road-to-reinvent-redteam/debate_abc123_1701234567/audio_response/debate_synthesis.mp3"
    },
    "audioStatus": "processing"
}
```

**Error Response:**
```json
{
    "status": "error",
    "error": "Error message",
    "sessionId": "debate_abc123_1701234567",
    "actor_id": "orchestrator"
}
```

## Environment Configuration

### Orchestrator Agent (AgentCore Runtime)
```bash
MEMORY_ID=<agentcore-memory-resource-id>
MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
AWS_REGION=us-east-1
S3_BUCKET=road-to-reinvent-redteam
```

### Lambda Function
```bash
BUCKET_NAME=road-to-reinvent-redteam
POLLY_VOICE_ID=Matthew
POLLY_ENGINE=neural
POLLY_SAMPLE_RATE=24000
```

## Deployment Architecture

### Infrastructure Components

1. **AgentCore Runtime**
   - Hosts orchestrator and expert agents
   - Serverless, auto-scaling
   - Integrated with AgentCore Memory

2. **AgentCore Memory**
   - Managed memory service
   - Session-based storage
   - Actor-based context retrieval

3. **S3 Bucket**
   - Versioning enabled
   - Event notifications configured
   - Lifecycle policies for old sessions

4. **Lambda Function**
   - Event-driven execution
   - Triggered by S3 uploads
   - Integrated with Polly

5. **Amazon Polly**
   - Neural voice synthesis
   - High-quality audio output
   - Supports long-form content

### Deployment Steps

1. **Deploy AgentCore Memory**
   ```bash
   # Create memory resource
   aws bedrock-agent create-memory \
     --memory-name disagree-and-commit-memory \
     --region us-east-1
   ```

2. **Deploy Orchestrator to AgentCore Runtime**
   ```bash
   agentcore configure \
     --entrypoint orchestrator/app.py \
     --agent-name disagree-and-commit-orchestrator \
     --region us-east-1
   
   agentcore launch \
     --env MEMORY_ID=<memory-id> \
     --env S3_BUCKET=road-to-reinvent-redteam
   ```

3. **Create S3 Bucket and Configure Events**
   ```bash
   # Create bucket
   aws s3 mb s3://road-to-reinvent-redteam
   
   # Enable versioning
   aws s3api put-bucket-versioning \
     --bucket road-to-reinvent-redteam \
     --versioning-configuration Status=Enabled
   
   # Configure event notification (after Lambda is deployed)
   aws s3api put-bucket-notification-configuration \
     --bucket road-to-reinvent-redteam \
     --notification-configuration file://s3-event-config.json
   ```

4. **Deploy Lambda Function**
   ```bash
   # Package Lambda
   cd lambda
   pip install -r requirements.txt -t .
   zip -r function.zip .
   
   # Deploy
   aws lambda create-function \
     --function-name debate-audio-converter \
     --runtime python3.11 \
     --handler lambda_function.lambda_handler \
     --zip-file fileb://function.zip \
     --role arn:aws:iam::ACCOUNT:role/lambda-execution-role \
     --timeout 300 \
     --memory-size 512 \
     --environment Variables="{BUCKET_NAME=road-to-reinvent-redteam,POLLY_VOICE_ID=Matthew}"
   ```

## Monitoring and Observability

### CloudWatch Metrics
- Agent invocation count and duration
- Memory operation success/failure rates
- S3 upload success rates
- Lambda execution duration and errors
- Polly API call count and errors

### CloudWatch Logs
- Orchestrator execution logs
- Expert agent response logs
- Memory operation logs
- Lambda function logs
- S3 event processing logs

### X-Ray Tracing
- End-to-end request tracing
- Agent invocation timing
- Memory operation latency
- S3 upload performance
- Lambda execution breakdown

## Cost Optimization

### AgentCore Runtime
- Pay per invocation
- No idle costs
- Auto-scaling included

### AgentCore Memory
- Pay per storage and retrieval
- Optimize by limiting context window
- Clean up old sessions periodically

### Bedrock (Claude Sonnet 4)
- Pay per token (input + output)
- ~200 words per response = ~300 tokens
- 3 agents × 3 rounds = 9 invocations per debate
- Plus 1 synthesis invocation

### S3 Storage
- Standard storage for active sessions
- Intelligent-Tiering for older sessions
- Lifecycle policy to archive after 90 days

### Lambda + Polly
- Lambda: Pay per execution time
- Polly: Pay per character synthesized
- Neural voices cost more but higher quality

## Security Considerations

### IAM Roles and Policies
- Least privilege access for all components
- Separate roles for orchestrator, Lambda, and S3
- Service-to-service authentication

### Data Encryption
- S3: Server-side encryption (SSE-S3 or SSE-KMS)
- AgentCore Memory: Encrypted at rest
- Polly: Audio streams encrypted in transit

### Access Control
- S3 bucket policies restrict public access
- AgentCore Runtime authentication required
- Lambda execution role scoped to specific bucket

### Audit Logging
- CloudTrail for all API calls
- S3 access logs enabled
- AgentCore audit logs

## Future Enhancements

1. **Multi-Voice Audio**
   - Use different Polly voices for each expert
   - Add speaker labels in audio
   - Generate podcast-style conversations

2. **Real-Time Streaming**
   - Stream debate responses as they're generated
   - WebSocket integration for live updates
   - Progressive audio generation

3. **Video Generation**
   - Convert to video with avatars
   - Add visual diagrams and charts
   - YouTube/social media ready format

4. **Interactive Playback**
   - Web UI for browsing debates
   - Synchronized audio and text
   - Jump to specific rounds or speakers

5. **Analytics Dashboard**
   - Debate metrics and insights
   - Popular topics and patterns
   - Expert agreement/disagreement analysis
