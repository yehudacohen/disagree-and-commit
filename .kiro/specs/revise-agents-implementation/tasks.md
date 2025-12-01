# Implementation Plan

- [x] 1. Update expert agent files with correct Strands patterns
  - Update BedrockModel initialization with correct model_id format
  - Update Agent initialization to pass name parameter
  - Update import statements to use correct modules
  - _Requirements: 1.1, 1.2, 1.5, 5.1, 5.2, 5.3_

- [x] 1.1 Update jeff_barr.py with correct patterns
  - Change import from `strands.models` to `strands.models.bedrock`
  - Update BedrockModel with full model_id: "us.anthropic.claude-sonnet-4-20250514-v1:0"
  - Add temperature=0.7 and max_tokens=2048 to BedrockModel
  - Pass name="jeff_barr" to Agent constructor
  - Remove the `agent.name = "jeff_barr"` line after initialization
  - _Requirements: 1.1, 1.2, 1.5, 5.1, 5.2, 5.3_

- [x] 1.2 Update swami.py with correct patterns
  - Change import from `strands.models` to `strands.models.bedrock`
  - Update BedrockModel with full model_id: "us.anthropic.claude-sonnet-4-20250514-v1:0"
  - Add temperature=0.7 and max_tokens=2048 to BedrockModel
  - Pass name="swami" to Agent constructor
  - Remove the `agent.name = "swami"` line after initialization
  - _Requirements: 1.1, 1.2, 1.5, 5.1, 5.2, 5.3_

- [x] 1.3 Update werner_vogels.py with correct patterns
  - Change import from `strands.models` to `strands.models.bedrock`
  - Update BedrockModel with full model_id: "us.anthropic.claude-sonnet-4-20250514-v1:0"
  - Add temperature=0.7 and max_tokens=2048 to BedrockModel
  - Pass name="werner_vogels" to Agent constructor
  - Remove the `agent.name = "werner_vogels"` line after initialization
  - _Requirements: 1.1, 1.2, 1.5, 5.1, 5.2, 5.3_

- [x] 2. Refactor MemoryManager to use correct AgentCore Memory APIs
  - Update to use bedrock-agent-runtime client instead of custom methods
  - Implement create_event for storing responses
  - Implement retrieve_memory for getting context
  - Update session ID generation to meet minimum length requirements
  - Add region parameter to initialization
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.6, 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 2.1 Update MemoryManager initialization
  - Add region parameter with default 'us-east-1'
  - Initialize boto3 client with 'bedrock-agent-runtime' service
  - Pass region_name to client initialization
  - Keep memory_id parameter
  - Add logging configuration
  - _Requirements: 2.1, 6.4, 9.3, 9.4, 9.5_

- [x] 2.2 Update create_session method
  - Update session ID format to ensure minimum 33 character length
  - Add actor_id parameter
  - Remove create_memory_session API call (sessions are implicit)
  - Return session ID in correct format
  - _Requirements: 2.6, 6.3_

- [x] 2.3 Update store_response method
  - Replace put_memory with create_event API call
  - Format messages as list with role and text fields
  - Use actorId parameter instead of userId
  - Add proper error handling and logging
  - Keep retry logic
  - _Requirements: 2.3, 6.1, 6.5_

- [x] 2.4 Update get_context method
  - Replace get_memory with retrieve_memory API call
  - Add actorId parameter
  - Update response parsing to extract text from content structure
  - Format context string from memories list
  - Add error handling
  - _Requirements: 2.4, 6.2, 6.5_

- [x] 2.5 Update get_full_context method
  - Update to use new retrieve_memory pattern
  - Ensure it retrieves all memories for the session
  - Format complete debate transcript
  - _Requirements: 2.4, 6.2_

- [x] 3. Update orchestrator to use correct agent invocation patterns
  - Update agent invocation from agent.run() to agent()
  - Update response extraction to use response.message['content'][0]['text']
  - Update memory manager initialization with region
  - Add environment variable handling for MEMORY_ID
  - Update error handling for new patterns
  - _Requirements: 1.3, 1.4, 3.1, 3.2, 3.3, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 3.1 Update imports and initialization
  - Add os import for environment variables
  - Add logging configuration
  - Initialize MemoryManager with memory_id from environment
  - Add REGION environment variable with default
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 3.2 Update agent invocation in debate loop
  - Change from `response = agent.run(prompt)` to `response = agent(prompt)`
  - Change from `response_text = response.message` to `response_text = response.message['content'][0]['text']`
  - Add try-except block with proper error handling
  - Add logging for agent invocations
  - _Requirements: 1.3, 1.4, 5.4, 5.5, 7.1, 7.4_

- [x] 3.3 Update memory storage calls
  - Add actor_id parameter to store_response calls
  - Use consistent actor naming (e.g., agent.name)
  - Update error handling for memory operations
  - _Requirements: 2.3, 6.1, 7.3_

- [x] 3.4 Update context retrieval calls
  - Add actor_id parameter to get_context calls
  - Update get_full_context call for synthesis
  - Handle empty context gracefully
  - _Requirements: 2.4, 6.2, 7.2_

- [x] 3.5 Update response structure
  - Ensure return dictionary includes all required fields
  - Add actor_id to response
  - Add session_id from context if available
  - Update error response format
  - _Requirements: 3.3, 7.5_

- [x] 4. Update synthesis agent with correct patterns
  - Update BedrockModel initialization
  - Update agent invocation pattern
  - Update response extraction
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 8.1, 8.2, 8.3_

- [x] 4.1 Update synthesis agent definition
  - Change import from `strands.models` to `strands.models.bedrock`
  - Update BedrockModel with full model_id
  - Add temperature and max_tokens parameters
  - Pass name="synthesis" to Agent constructor
  - Remove post-initialization name assignment
  - _Requirements: 1.1, 1.2, 1.5, 8.1_

- [x] 4.2 Update synthesis invocation in orchestrator
  - Change from `synthesis_result = synthesis_agent.run(prompt)` to `synthesis_result = synthesis_agent(prompt)`
  - Change from `synthesis_text = synthesis_result.message` to `synthesis_text = synthesis_result.message['content'][0]['text']`
  - Add error handling for synthesis failures
  - _Requirements: 1.3, 1.4, 8.1, 8.2, 8.3_

- [x] 5. Update tests to match new patterns
  - Update test mocks for new response structure
  - Update test assertions for new invocation patterns
  - Update memory operation tests
  - Add tests for error handling
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 5.1 Update test_experts.py
  - Mock agent responses with correct structure: `{"message": {"content": [{"text": "..."}]}}`
  - Update assertions to check response.message['content'][0]['text']
  - Test BedrockModel initialization with correct parameters
  - _Requirements: 10.1, 10.2_

- [x] 5.2 Update test_memory_manager.py
  - Mock boto3 bedrock-agent-runtime client
  - Update tests for create_event API
  - Update tests for retrieve_memory API
  - Test session ID format and length
  - Test error handling and retry logic
  - _Requirements: 10.2, 10.3_

- [x] 5.3 Update test_orchestrator.py
  - Mock expert agents with correct response structure
  - Mock memory manager with new methods
  - Test complete debate flow
  - Test error handling for agent failures
  - Test response structure validation
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 5.4 Update test_synthesis_integration.py
  - Mock synthesis agent with correct response structure
  - Test Mermaid extraction from various formats
  - Test synthesis error handling
  - _Requirements: 10.1, 10.2, 10.4_

- [x] 6. Add configuration and environment variable handling
  - Add environment variable reading with defaults
  - Add logging configuration
  - Add validation for required environment variables
  - Document environment variables in README
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 6.1 Add environment variable handling to orchestrator
  - Read MEMORY_ID from environment
  - Read MODEL_ID from environment with default
  - Read AWS_REGION from environment with default
  - Add validation and warnings for missing variables
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 6.2 Add logging configuration
  - Configure logging format and level
  - Add logger instances to all modules
  - Add informative log messages for key operations
  - Add error logging for failures
  - _Requirements: 9.5_

- [x] 6.3 Update README with configuration instructions
  - Document required environment variables
  - Document default values
  - Add deployment instructions
  - Add local testing instructions
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
