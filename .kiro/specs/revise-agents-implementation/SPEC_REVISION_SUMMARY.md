# Spec Revision Summary

## Overview

The spec files have been revised to reflect the new architecture with S3 storage and Lambda-triggered audio conversion using Amazon Polly.

## Key Changes

### Architecture Evolution

**Before:**
- 4 agents (orchestrator + 3 experts)
- AgentCore Memory for storage
- Direct response with synthesis

**After:**
- 4 agents (orchestrator + 3 experts)
- AgentCore Memory for conversation history
- S3 storage for markdown transcripts
- Lambda function for audio conversion
- Amazon Polly for text-to-speech
- Event-driven architecture with S3 triggers

### New Components Added

1. **S3 Storage Layer**
   - Bucket: `road-to-reinvent-redteam`
   - Path structure: `{sessionId}/conversation_response/` and `{sessionId}/audio_response/`
   - Stores markdown transcripts and MP3 audio files

2. **Lambda Audio Converter**
   - Triggered by S3 ObjectCreated events
   - Converts markdown to plain text
   - Uses Amazon Polly for speech synthesis
   - Handles chunking for Polly's 3000 character limit
   - Uploads MP3 to S3

3. **Amazon Polly Integration**
   - Neural voice engine
   - Configurable voice (default: Matthew)
   - High-quality audio output

## Requirements Document Changes

### New Requirements Added

- **Requirement 1**: Orchestrator Agent (expanded from previous Requirement 1)
  - Added S3 upload requirement
  - Added s3Paths in response structure

- **Requirement 2**: Expert Persona Agents (consolidated from previous Requirements 1 & 5)
  - Clarified three distinct personas
  - Specified response length (~200 words)

- **Requirement 4**: Synthesis Generation (new)
  - Detailed synthesis document structure
  - Mermaid diagram generation
  - Trade-offs analysis

- **Requirement 5**: S3 Storage Integration (new)
  - Bucket and path structure
  - Metadata requirements
  - Error handling

- **Requirement 6**: Lambda Audio Converter (new)
  - S3 event trigger
  - Polly integration
  - Audio file upload

- **Requirement 10**: Monitoring and Observability (new)
  - Comprehensive logging requirements
  - Operation tracking

### Requirements Reorganized

- Previous Requirements 2-10 consolidated and reorganized
- Focus shifted from "refactoring" to "building complete system"
- Added end-to-end flow requirements

## Design Document Changes

### Architecture Section

**Added:**
- System flow diagram with S3 and Lambda
- S3 storage structure
- Event-driven architecture principles
- Complete system flow (4 phases)

**Updated:**
- Component structure to include Lambda
- Key design principles

### Components Section

**Added:**
- Orchestrator Agent with complete interface
- S3 Storage Component with upload patterns
- Lambda Audio Converter with complete implementation
- Polly configuration details

**Updated:**
- All agent interfaces to show correct patterns
- Response structures to include s3Paths

### Data Models Section

**Added:**
- Markdown document structure
- S3 event structure
- Audio metadata structure

**Updated:**
- Orchestrator response to include s3Paths and audioStatus

### Correctness Properties

**Revised all 10 properties:**
1. Debate Completeness (3 rounds, 9 invocations)
2. Memory Storage Round Trip
3. Session ID Format
4. Agent Response Structure
5. S3 Path Structure (new)
6. Synthesis Completeness
7. Error Handling Preservation
8. Audio Conversion Trigger (new)
9. Orchestrator Response Completeness
10. Context Accumulation (new)

### Deployment Section

**Completely rewritten with 5 steps:**
1. Deploy AgentCore Memory
2. Create and Configure S3 Bucket
3. Deploy Lambda Function
4. Configure S3 Event Notification
5. Deploy Orchestrator to AgentCore Runtime

**Added:**
- S3 event configuration JSON
- Lambda IAM permissions
- Local testing examples
- End-to-end testing procedures

## Tasks Document

The tasks.md file will need to be updated to reflect:

1. **New tasks for S3 integration**
   - Implement S3 upload in orchestrator
   - Add s3Paths to response structure
   - Handle S3 upload errors

2. **New tasks for Lambda function**
   - Create Lambda function structure
   - Implement markdown to text conversion
   - Implement Polly integration
   - Implement audio chunking and combining
   - Add error handling and logging

3. **New tasks for deployment**
   - Create S3 bucket and configure
   - Deploy Lambda function
   - Configure S3 event notifications
   - Test end-to-end flow

4. **Updated synthesis tasks**
   - Generate complete markdown document
   - Include session metadata
   - Format debate transcript

## Glossary Updates

**Added terms:**
- Orchestrator Agent
- Expert Persona Agents
- Synthesis
- Session
- S3 Bucket
- Lambda Function
- Amazon Polly

**Removed terms:**
- MemoryClient (not directly used)
- BedrockAgentCoreApp (implementation detail)

## Next Steps

1. **Update tasks.md** with new implementation tasks
2. **Create Lambda function** code structure
3. **Update orchestrator** to include S3 upload
4. **Add S3 and Polly** to requirements.txt
5. **Create deployment scripts** for infrastructure
6. **Update tests** to cover S3 and Lambda integration

## Benefits of New Architecture

1. **Persistent Storage**: Debates stored permanently in S3
2. **Audio Output**: Automatic conversion to audio format
3. **Event-Driven**: Asynchronous processing doesn't block orchestrator
4. **Scalable**: Lambda scales automatically with demand
5. **Cost-Effective**: Pay only for what you use
6. **Accessible**: Multiple output formats (markdown + audio)
7. **Auditable**: Complete history in S3 with versioning
