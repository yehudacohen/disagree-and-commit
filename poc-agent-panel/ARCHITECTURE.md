# Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Input                               │
│                  "Problem Statement"                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   panel_discussion.py                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         PanelDiscussion Class                             │  │
│  │                                                            │  │
│  │  • Load persona prompts                                   │  │
│  │  • Initialize AWS Bedrock client                          │  │
│  │  • Manage discussion history                              │  │
│  │  • Orchestrate 4 rounds                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Load Persona Prompts                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Jeff Barr   │  │    Swami     │  │   Werner     │         │
│  │  Persona     │  │   Persona    │  │   Persona    │         │
│  │  (.md file)  │  │  (.md file)  │  │  (.md file)  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Round 1: Initial Opinions                 │
│                                                                   │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │   Jeff      │      │   Swami     │      │  Werner     │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Bedrock API │      │ Bedrock API │      │ Bedrock API │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Response    │      │ Response    │      │ Response    │    │
│  └─────────────┘      └─────────────┘      └─────────────┘    │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                              │                                   │
│                              ▼                                   │
│                    Store in discussion_history                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Round 2: Disagreements                        │
│                    (with Round 1 context)                        │
│                                                                   │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │   Jeff      │      │   Swami     │      │  Werner     │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Bedrock API │      │ Bedrock API │      │ Bedrock API │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Response    │      │ Response    │      │ Response    │    │
│  └─────────────┘      └─────────────┘      └─────────────┘    │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                              │                                   │
│                              ▼                                   │
│                    Store in discussion_history                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Round 3: Personal Callouts                      │
│                  (with Rounds 1-2 context)                       │
│                                                                   │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │   Jeff      │      │   Swami     │      │  Werner     │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Bedrock API │      │ Bedrock API │      │ Bedrock API │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Response    │      │ Response    │      │ Response    │    │
│  └─────────────┘      └─────────────┘      └─────────────┘    │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                              │                                   │
│                              ▼                                   │
│                    Store in discussion_history                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                Round 4: Disagree and Commit                      │
│                   (with full context)                            │
│                                                                   │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐    │
│  │   Jeff      │      │   Swami     │      │  Werner     │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Bedrock API │      │ Bedrock API │      │ Bedrock API │    │
│  │   ↓         │      │   ↓         │      │   ↓         │    │
│  │ Response    │      │ Response    │      │ Response    │    │
│  └─────────────┘      └─────────────┘      └─────────────┘    │
│         │                    │                    │             │
│         └────────────────────┴────────────────────┘             │
│                              │                                   │
│                              ▼                                   │
│                    Store in discussion_history                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output to Console                           │
│                                                                   │
│  • All 12 responses printed in real-time                        │
│  • Formatted with clear round/panelist headers                  │
│  • Discussion history available for analysis                    │
└─────────────────────────────────────────────────────────────────┘
```

## AWS Bedrock Integration

```
┌──────────────────────────────────────────────────────────────┐
│                    Python Application                         │
│                  (panel_discussion.py)                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ boto3.Session(profile='scratchspace')
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    AWS Credentials                            │
│                                                               │
│  • Profile: scratchspace                                     │
│  • Region: us-east-1                                         │
│  • IAM Permissions: bedrock:InvokeModel                      │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ bedrock-runtime.invoke_model()
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   Amazon Bedrock                              │
│                                                               │
│  Model: us.anthropic.claude-sonnet-4-20250514               │
│  API Version: bedrock-2023-05-31                            │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ Anthropic Messages API
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                Claude Sonnet 4.5                              │
│                                                               │
│  Input:                                                       │
│  • System: Persona prompt (Jeff/Swami/Werner)               │
│  • User: Problem + Discussion context                        │
│  • Temperature: 0.7                                          │
│  • Max tokens: 2000                                          │
│                                                               │
│  Output:                                                      │
│  • Text response in character                                │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         │ JSON response
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                Response Processing                            │
│                                                               │
│  • Extract text from response                                │
│  • Print to console                                          │
│  • Store in discussion_history                               │
│  • Pass as context to next round                             │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

```
Problem Statement
      │
      ▼
┌─────────────────┐
│ Round 1         │
│ Context: None   │
└────────┬────────┘
         │
         ▼
    [3 responses]
         │
         ▼
┌─────────────────┐
│ Round 2         │
│ Context: R1     │
└────────┬────────┘
         │
         ▼
    [3 responses]
         │
         ▼
┌─────────────────┐
│ Round 3         │
│ Context: R1+R2  │
└────────┬────────┘
         │
         ▼
    [3 responses]
         │
         ▼
┌─────────────────┐
│ Round 4         │
│ Context: R1+R2+R3│
└────────┬────────┘
         │
         ▼
    [3 responses]
         │
         ▼
   Final Output
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                      User Layer                              │
│                                                              │
│  • Command line interface                                   │
│  • Provides problem statement                               │
│  • Receives formatted output                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                           │
│                                                              │
│  PanelDiscussion Class:                                     │
│  • run_discussion()      - Main orchestrator                │
│  • round_1_*()          - Round implementations             │
│  • round_2_*()                                              │
│  • round_3_*()                                              │
│  • round_4_*()                                              │
│  • _call_claude()       - API wrapper                       │
│  • _format_context()    - Context builder                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│                                                              │
│  • Persona prompts (markdown files)                         │
│  • Discussion history (in-memory list)                      │
│  • Configuration (hardcoded constants)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Integration Layer                           │
│                                                              │
│  • boto3 SDK                                                │
│  • AWS Bedrock API                                          │
│  • Claude Sonnet 4.5 model                                  │
└─────────────────────────────────────────────────────────────┘
```

## File Dependencies

```
panel_discussion.py
    │
    ├─→ jeff-barr-agent-prompt.md
    ├─→ swami-sivasubramanian-agent-prompt.md
    └─→ werner_vogels_agent_prompt.md
    │
    └─→ boto3 (external dependency)
         │
         └─→ AWS Bedrock (cloud service)
              │
              └─→ Claude Sonnet 4.5 (AI model)
```

## Execution Flow

```
1. main()
   │
   ├─→ Parse command line arguments
   │
   └─→ PanelDiscussion.__init__()
       │
       ├─→ Create boto3 session
       ├─→ Create bedrock-runtime client
       └─→ _load_panelists()
           │
           └─→ Read 3 persona files
   │
   └─→ run_discussion(problem)
       │
       ├─→ round_1_initial_opinions()
       │   │
       │   └─→ For each panelist:
       │       ├─→ Build user message
       │       ├─→ _call_claude(persona, message)
       │       ├─→ Print response
       │       └─→ Store in history
       │
       ├─→ round_2_disagreements()
       │   │
       │   └─→ For each panelist:
       │       ├─→ _format_discussion_context()
       │       ├─→ Build user message with context
       │       ├─→ _call_claude(persona, message)
       │       ├─→ Print response
       │       └─→ Store in history
       │
       ├─→ round_3_personal_callouts()
       │   │
       │   └─→ [Same pattern as Round 2]
       │
       └─→ round_4_disagree_and_commit()
           │
           └─→ [Same pattern as Round 2]
```

## Error Handling Flow

```
User Input
    │
    ▼
Try: PanelDiscussion()
    │
    ├─→ ProfileNotFound
    │   └─→ Error: AWS profile not configured
    │
    ├─→ NoCredentialsError
    │   └─→ Error: AWS credentials not found
    │
    └─→ Success
        │
        ▼
    Try: run_discussion()
        │
        ├─→ FileNotFoundError
        │   └─→ Error: Persona file missing
        │
        ├─→ ClientError (Bedrock)
        │   ├─→ AccessDeniedException
        │   │   └─→ Error: No Bedrock access
        │   │
        │   ├─→ ModelNotFoundException
        │   │   └─→ Error: Model not available
        │   │
        │   └─→ ThrottlingException
        │       └─→ Error: Rate limit exceeded
        │
        └─→ Success
            └─→ Print all responses
```

## Scalability Considerations

```
Current: Sequential Processing
┌──────┐    ┌──────┐    ┌──────┐
│ Jeff │ → │ Swami│ → │Werner│
└──────┘    └──────┘    └──────┘
  ~2s         ~2s         ~2s
Total: ~6s per round × 4 rounds = ~24s

Future: Parallel Processing
┌──────┐
│ Jeff │
├──────┤
│ Swami│  → All complete in ~2s
├──────┤
│Werner│
└──────┘
Total: ~2s per round × 4 rounds = ~8s
```

## Extension Points

```
Current Architecture
    │
    ├─→ Add Panelists
    │   └─→ Create new persona file
    │       └─→ Add to _load_panelists()
    │
    ├─→ Add Rounds
    │   └─→ Create round_5_*() method
    │       └─→ Add to run_discussion()
    │
    ├─→ Change Output
    │   └─→ Modify print statements
    │       └─→ Add file/JSON/HTML output
    │
    ├─→ Different Model
    │   └─→ Change model_id
    │       └─→ Adjust parameters
    │
    └─→ Add Features
        ├─→ Streaming responses
        ├─→ Token tracking
        ├─→ Cost calculation
        └─→ Interactive mode
```
