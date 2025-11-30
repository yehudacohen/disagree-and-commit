# Troubleshooting Guide

Common issues and their solutions when running the AWS Executive Panel Discussion.

## Setup Issues

### "No module named 'boto3'"

**Problem**: Python can't find the boto3 library.

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install boto3
pip install boto3

# Verify installation
python -c "import boto3; print(boto3.__version__)"
```

### "python: command not found" or "python3: command not found"

**Problem**: Python is not installed or not in PATH.

**Solution**:
```bash
# Check Python installation
which python3

# Install Python (macOS)
brew install python3

# Or download from python.org
```

### Virtual Environment Won't Activate

**Problem**: `source venv/bin/activate` doesn't work.

**Solution**:
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# Verify activation (should show venv in prompt)
which python
```

## AWS Credential Issues

### "Unable to locate credentials"

**Problem**: AWS credentials are not configured.

**Solution**:
```bash
# Option 1: Configure AWS profile
aws configure --profile scratchspace
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Option 2: Set environment variables
export AWS_PROFILE=scratchspace
export AWS_DEFAULT_REGION=us-east-1

# Option 3: Use default profile
# Edit panel_discussion.py and change profile_name to 'default'

# Verify credentials
aws sts get-caller-identity --profile scratchspace
```

### "The config profile (scratchspace) could not be found"

**Problem**: AWS profile doesn't exist.

**Solution**:
```bash
# List existing profiles
aws configure list-profiles

# Create the profile
aws configure --profile scratchspace

# Or edit ~/.aws/credentials manually
nano ~/.aws/credentials

# Add:
[scratchspace]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

### "An error occurred (ExpiredToken)"

**Problem**: AWS credentials have expired.

**Solution**:
```bash
# If using temporary credentials, refresh them
aws sts get-session-token --profile scratchspace

# Or reconfigure with new credentials
aws configure --profile scratchspace
```

## Bedrock Access Issues

### "AccessDeniedException" when calling Bedrock

**Problem**: IAM user/role doesn't have Bedrock permissions.

**Solution**:
1. Go to AWS Console → IAM
2. Find your user/role
3. Add policy with these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

### "Model not found" or "ValidationException"

**Problem**: Claude Sonnet 4.5 model is not available.

**Solution**:
1. Go to AWS Console → Bedrock
2. Navigate to "Model access" in left sidebar
3. Click "Manage model access"
4. Find "Claude Sonnet 4" and enable it
5. Wait 2-5 minutes for activation
6. Verify:
```bash
aws bedrock list-foundation-models \
  --profile scratchspace \
  --region us-east-1 \
  --query 'modelSummaries[?contains(modelId, `claude-sonnet-4`)].modelId'
```

### "Bedrock is not available in this region"

**Problem**: Bedrock is not enabled in your region.

**Solution**:
```bash
# Use us-east-1 (default in the code)
# Or edit panel_discussion.py to change region:
# self.bedrock = self.session.client('bedrock-runtime', region_name='us-west-2')

# Check available regions
aws bedrock list-foundation-models --region us-east-1
```

## Runtime Issues

### "FileNotFoundError: [Errno 2] No such file or directory"

**Problem**: Persona prompt files are missing.

**Solution**:
```bash
# Check if files exist
ls -la *.md

# Should see:
# jeff-barr-agent-prompt.md
# swami-sivasubramanian-agent-prompt.md
# werner_vogels_agent_prompt.md

# If missing, you're in the wrong directory
cd /path/to/panel-discussion
```

### Program Hangs or Takes Too Long

**Problem**: API calls are slow or timing out.

**Solution**:
```bash
# Check network connectivity
ping bedrock-runtime.us-east-1.amazonaws.com

# Check AWS service status
# Visit: https://status.aws.amazon.com/

# Reduce max_tokens in panel_discussion.py
# Change: "max_tokens": 2000
# To: "max_tokens": 1000

# Check for rate limiting
# Wait a few minutes and try again
```

### "ThrottlingException" or "Rate exceeded"

**Problem**: Too many API calls too quickly.

**Solution**:
```bash
# Wait 1-2 minutes between runs

# Or add retry logic (edit panel_discussion.py):
import time
from botocore.exceptions import ClientError

def _call_claude_with_retry(self, system_prompt, user_message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return self._call_claude(system_prompt, user_message)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
            raise
```

### Responses Are Cut Off or Incomplete

**Problem**: Responses exceed max_tokens limit.

**Solution**:
```python
# Edit panel_discussion.py
# Increase max_tokens:
"max_tokens": 3000  # or higher

# Or adjust temperature for more concise responses:
"temperature": 0.5  # lower = more focused
```

### Personas Don't Sound Authentic

**Problem**: Responses don't match expected personalities.

**Solution**:
```bash
# Check persona files are loaded correctly
python -c "
from panel_discussion import PanelDiscussion
p = PanelDiscussion('scratchspace')
print(f'Loaded {len(p.panelists)} panelists')
for panelist in p.panelists:
    print(f'{panelist.name}: {len(panelist.persona_prompt)} chars')
"

# Adjust temperature for more personality:
"temperature": 0.8  # higher = more creative

# Or edit persona prompts to be more specific
```

## Output Issues

### Output Is Garbled or Has Encoding Issues

**Problem**: Terminal encoding doesn't support special characters.

**Solution**:
```bash
# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Or redirect to file
python panel_discussion.py "Problem" > output.txt

# View with proper encoding
cat output.txt
```

### Want to Save Output to File

**Problem**: Output only goes to console.

**Solution**:
```bash
# Save to file
python panel_discussion.py "Problem" > discussion.txt

# Save with timestamp
python panel_discussion.py "Problem" | tee "discussion_$(date +%Y%m%d_%H%M%S).txt"

# Save and view simultaneously
python panel_discussion.py "Problem" | tee output.txt
```

## Testing Issues

### test_credentials.py Fails

**Problem**: Credential test script reports errors.

**Solution**:
```bash
# Run with verbose output
python test_credentials.py

# Check each step:
# 1. Profile exists → aws configure list-profiles
# 2. Credentials valid → aws sts get-caller-identity --profile scratchspace
# 3. Bedrock access → aws bedrock list-foundation-models --profile scratchspace --region us-east-1
# 4. Claude model → Check Bedrock console for model access

# Fix the first failing step
```

## Cost Issues

### Unexpected AWS Charges

**Problem**: Running the panel discussion costs more than expected.

**Solution**:
```bash
# Check current pricing
# Visit: https://aws.amazon.com/bedrock/pricing/

# Monitor token usage
# Add to panel_discussion.py:
def _call_claude(self, system_prompt, user_message):
    # ... existing code ...
    response_body = json.loads(response['body'].read())
    
    # Log token usage
    usage = response_body.get('usage', {})
    print(f"Tokens - Input: {usage.get('input_tokens')}, Output: {usage.get('output_tokens')}")
    
    return response_body['content'][0]['text']

# Set up billing alerts in AWS Console
# AWS Console → Billing → Budgets → Create budget
```

### Want to Reduce Costs

**Problem**: Need to minimize API costs.

**Solution**:
```python
# Edit panel_discussion.py

# 1. Reduce max_tokens
"max_tokens": 1000  # instead of 2000

# 2. Reduce context passed to later rounds
def _format_discussion_context(self, round_num, round_name):
    # Only include previous round, not all rounds
    if not self.discussion_history:
        return ""
    
    # Get only last 3 responses
    recent = self.discussion_history[-3:]
    context = f"\n\n=== PREVIOUS ROUND ===\n"
    for entry in recent:
        context += f"\n{entry['panelist']}: {entry['response'][:200]}...\n"
    return context

# 3. Use cheaper model for testing
# self.model_id = "anthropic.claude-instant-v1"  # if available
```

## Performance Issues

### Program Is Too Slow

**Problem**: Takes too long to complete discussion.

**Solution**:
```python
# Option 1: Reduce max_tokens
"max_tokens": 1000

# Option 2: Implement parallel API calls
import concurrent.futures

def round_1_initial_opinions_parallel(self, problem):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for panelist in self.panelists:
            future = executor.submit(
                self._call_claude,
                panelist.persona_prompt,
                f"Problem: {problem}\n\nShare your opinion..."
            )
            futures.append((panelist, future))
        
        for panelist, future in futures:
            response = future.result()
            print(f"\n{panelist.name}:\n{response}")

# Option 3: Use streaming (requires code changes)
```

## Debug Mode

### Need More Information About What's Happening

**Problem**: Want to see detailed execution information.

**Solution**:
```python
# Add debug mode to panel_discussion.py

import logging

# At top of file
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In methods
def _call_claude(self, system_prompt, user_message):
    logger.debug(f"Calling Claude with {len(system_prompt)} char prompt")
    logger.debug(f"User message: {user_message[:100]}...")
    
    # ... existing code ...
    
    logger.debug(f"Response received: {len(response_body['content'][0]['text'])} chars")
    return response_body['content'][0]['text']

# Run with debug output
python panel_discussion.py "Problem" 2>&1 | tee debug.log
```

## Getting Help

### Still Having Issues?

1. **Run the test script**:
   ```bash
   python test_credentials.py
   ```

2. **Check AWS service health**:
   - Visit: https://status.aws.amazon.com/

3. **Verify your setup**:
   ```bash
   # Python version
   python3 --version  # Should be 3.8+
   
   # boto3 version
   python3 -c "import boto3; print(boto3.__version__)"
   
   # AWS CLI version
   aws --version
   
   # AWS credentials
   aws sts get-caller-identity --profile scratchspace
   
   # Bedrock access
   aws bedrock list-foundation-models --profile scratchspace --region us-east-1
   ```

4. **Check the logs**:
   ```bash
   # Run with full error output
   python panel_discussion.py "Problem" 2>&1 | tee error.log
   
   # Review error.log for details
   ```

5. **Simplify the problem**:
   ```bash
   # Try a very simple problem
   python panel_discussion.py "Should we use Python or JavaScript?"
   ```

6. **Test individual components**:
   ```python
   # Test Bedrock connection
   python3 << EOF
   import boto3
   session = boto3.Session(profile_name='scratchspace')
   bedrock = session.client('bedrock-runtime', region_name='us-east-1')
   print("Bedrock client created successfully")
   EOF
   ```

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| `ModuleNotFoundError: No module named 'boto3'` | boto3 not installed | `pip install boto3` |
| `Unable to locate credentials` | AWS not configured | `aws configure --profile scratchspace` |
| `AccessDeniedException` | No Bedrock permissions | Add IAM permissions |
| `ValidationException` | Model not available | Enable model in Bedrock console |
| `ThrottlingException` | Rate limit exceeded | Wait and retry |
| `FileNotFoundError` | Wrong directory | `cd` to project directory |
| `ConnectionError` | Network issue | Check internet connection |
| `TimeoutError` | API timeout | Reduce max_tokens or check network |

## Prevention Tips

1. **Always activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Test credentials before running**:
   ```bash
   python test_credentials.py
   ```

3. **Start with simple problems**:
   - Test with short, simple problem statements first
   - Gradually increase complexity

4. **Monitor costs**:
   - Set up AWS billing alerts
   - Track token usage
   - Use test mode for development

5. **Keep dependencies updated**:
   ```bash
   pip install --upgrade boto3
   ```

6. **Use version control**:
   ```bash
   git init
   git add .
   git commit -m "Initial setup"
   # Easy to revert if something breaks
   ```
