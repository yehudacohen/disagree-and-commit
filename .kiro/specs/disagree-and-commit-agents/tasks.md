# Implementation Plan - Minimal MVP

**Development Tools**: Use MCP servers `bedrock-agentcore-mcp-server` and `strands-agents` for development assistance

- [x] 1. Implement AgentCore Memory Manager
  - Create MemoryManager class using AgentCore Memory SDK (reference bedrock-agentcore-mcp-server for AgentCore Memory APIs)
  - Implement create_session() with format `debate_{hash}_{timestamp}`
  - Implement store_response() with metadata (userId, round, content, timestamp)
  - Implement get_context() to retrieve all previous responses
  - Add basic retry logic for AgentCore Memory API calls
  - _Requirements: 1.1, 1.2, 6.1, 6.4, 6.5_

- [x] 2. Create Expert Agents using Strands framework
  - Define Jeff Barr Agent using Strands Agent with Claude Sonnet 4.1 (reference strands-agents MCP for Strands patterns)
  - Define Swami Agent using Strands Agent with Claude Sonnet 4.1
  - Define Werner Agent using Strands Agent with Claude Sonnet 4.1
  - Configure persona-specific instructions for each agent (~200 word responses)
  - Ensure each agent references previous context in responses
  - _Requirements: 3.1, 3.3, 3.4, 4.1, 4.3, 4.4, 5.1, 5.3, 5.4, 6.3_

- [x] 3. Create Synthesis Agent using Strands framework
  - Define Synthesis Agent using Strands Agent with Claude Sonnet 4.1 (reference strands-agents MCP for agent patterns)
  - Configure instructions to combine all three expert perspectives
  - Add Mermaid diagram generation to synthesis instructions
  - Implement extract_mermaid() utility to parse Mermaid code blocks from synthesis output
  - _Requirements: 7.1, 7.2, 7.4, 7.5_

- [x] 4. Implement Orchestrator with debate flow logic
  - Create debate_orchestrator() entrypoint using Strands framework (reference strands-agents MCP for orchestration patterns)
  - Implement 3-round debate loop (2 debate rounds + 1 consensus round)
  - Invoke experts sequentially (jeff_barr, swami, werner_vogels) in each round
  - Store each response to AgentCore Memory after generation
  - Retrieve cumulative context before each expert invocation
  - Trigger Synthesis Agent after all rounds complete
  - Return final synthesis with Mermaid diagram
  - _Requirements: 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 6.2_

- [x] 5. Configure AgentCore Runtime deployment
  - Create agentcore.yaml with Python 3.11 runtime configuration (reference bedrock-agentcore-mcp-server for deployment patterns)
  - Set memory to 2048 MB and timeout to 600 seconds
  - Configure MEMORY_ID environment variable for AgentCore Memory
  - Add IAM permissions for bedrock:InvokeModel and bedrock-agent-runtime:*
  - Load problem_statements.json for predefined problems
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 11.1, 11.2, 11.4_
