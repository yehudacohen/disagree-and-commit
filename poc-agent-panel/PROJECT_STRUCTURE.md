# Project Structure

```
.
├── panel_discussion.py              # Main program - orchestrates the panel discussion
├── test_credentials.py              # Utility to test AWS credentials and Bedrock access
├── example_usage.py                 # Example of programmatic usage
├── setup.sh                         # Quick setup script
│
├── jeff-barr-agent-prompt.md        # Jeff Barr's persona prompt
├── swami-sivasubramanian-agent-prompt.md  # Swami's persona prompt
├── werner_vogels_agent_prompt.md    # Werner's persona prompt
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Main documentation
├── EXAMPLE_OUTPUT.md               # Example of what the output looks like
├── PROJECT_STRUCTURE.md            # This file
└── .gitignore                      # Git ignore rules
```

## Core Components

### panel_discussion.py
The main program that orchestrates the 4-round panel discussion:

**Key Classes:**
- `Panelist`: Data class holding panelist information
- `PanelDiscussion`: Main orchestrator class

**Key Methods:**
- `_load_panelists()`: Loads persona prompts from markdown files
- `_call_claude()`: Invokes Claude Sonnet 4.5 via AWS Bedrock
- `_format_discussion_context()`: Formats discussion history for context
- `round_1_initial_opinions()`: Round 1 - Initial opinions
- `round_2_disagreements()`: Round 2 - Disagreements based on worldview
- `round_3_personal_callouts()`: Round 3 - Personal challenges
- `round_4_disagree_and_commit()`: Round 4 - Commit to solution
- `run_discussion()`: Orchestrates all 4 rounds

### Persona Prompts
Three detailed persona prompts that define each executive's:
- Core identity and background
- Communication style and signature phrases
- Panel discussion behavior patterns
- Technical perspectives and beliefs
- Example interactions

### Utility Scripts

**test_credentials.py**
- Validates AWS profile configuration
- Checks Bedrock access permissions
- Verifies Claude Sonnet 4.5 availability
- Provides helpful error messages

**example_usage.py**
- Shows programmatic usage of PanelDiscussion class
- Demonstrates how to access discussion history
- Provides error handling examples

**setup.sh**
- Creates virtual environment
- Installs dependencies
- Provides usage instructions

## Architecture

### Flow Diagram

```
User Input (Problem Statement)
        ↓
PanelDiscussion.__init__()
        ↓
Load Persona Prompts (3 files)
        ↓
Round 1: Initial Opinions
    ├─→ Jeff Barr (Claude API call)
    ├─→ Swami Sivasubramanian (Claude API call)
    └─→ Werner Vogels (Claude API call)
        ↓
Round 2: Disagreements
    ├─→ Jeff (with context from Round 1)
    ├─→ Swami (with context from Round 1)
    └─→ Werner (with context from Round 1)
        ↓
Round 3: Personal Callouts
    ├─→ Jeff (with context from Rounds 1-2)
    ├─→ Swami (with context from Rounds 1-2)
    └─→ Werner (with context from Rounds 1-2)
        ↓
Round 4: Disagree and Commit
    ├─→ Jeff (with full context)
    ├─→ Swami (with full context)
    └─→ Werner (with full context)
        ↓
Complete Discussion Output
```

### AWS Integration

```
panel_discussion.py
        ↓
boto3.Session(profile_name='scratchspace')
        ↓
bedrock-runtime client (us-east-1)
        ↓
invoke_model(modelId='us.anthropic.claude-sonnet-4-20250514')
        ↓
Claude Sonnet 4.5 API
        ↓
Response (JSON)
        ↓
Extract text content
        ↓
Print to stdout
```

## Data Flow

### Input
- Problem statement (string)
- AWS profile name (default: "scratchspace")

### Processing
1. Load 3 persona prompts from markdown files
2. For each round (1-4):
   - For each panelist (Jeff, Swami, Werner):
     - Build context from previous rounds
     - Create user message with problem + context
     - Call Claude API with persona as system prompt
     - Store response in discussion_history
     - Print response to stdout

### Output
- Formatted console output with all responses
- discussion_history list with all responses and metadata

## Extension Points

### Adding New Panelists
1. Create new persona prompt markdown file
2. Add to `_load_panelists()` method
3. Adjust round methods to handle additional panelists

### Adding New Rounds
1. Create new round method (e.g., `round_5_final_thoughts()`)
2. Add to `run_discussion()` method
3. Update documentation

### Customizing Output
- Modify print statements in round methods
- Add logging or file output
- Create structured output (JSON, CSV, etc.)

### Different Models
- Change `model_id` in `__init__()` method
- Adjust `max_tokens` or `temperature` in `_call_claude()`
- Modify request body structure if needed

## Dependencies

- **boto3**: AWS SDK for Python (Bedrock API access)
- **Python 3.8+**: Core language runtime

## Configuration

### Environment Variables (Optional)
- `AWS_PROFILE`: Override default profile
- `AWS_REGION`: Override default region (us-east-1)

### AWS Requirements
- IAM permissions for Bedrock
- Model access enabled for Claude Sonnet 4.5
- Valid credentials in AWS profile

## Testing

Run the credential test:
```bash
python test_credentials.py
```

Run a sample discussion:
```bash
python panel_discussion.py "Should we use serverless or containers?"
```

Run the example usage:
```bash
python example_usage.py
```
