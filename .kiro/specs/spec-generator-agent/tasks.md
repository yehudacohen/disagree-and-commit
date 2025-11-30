# Implementation Plan

- [x] 1. Set up project structure following existing patterns
  - Create `agents/spec_generator/` directory (following `agents/synthesis/`, `agents/experts/` pattern)
  - Create `agents/spec_generator/__init__.py` with module exports
  - Create `agents/spec_generator/generator.py` for the Strands agent
  - Create `agents/spec_generator/parser.py` for input parsing utilities
  - Create `agents/spec_generator/packager.py` for ZIP creation and S3 upload
  - No new dependencies needed (uses existing boto3, strands-agents from requirements.txt)
  - _Requirements: 1.1_

- [x] 2. Implement Input Parser
  - [x] 2.1 Create InputParser class with synthesis parsing
    - Implement `parse()` method to extract architecture sections
    - Implement `extract_mermaid()` to find Mermaid code blocks
    - Implement `extract_components()` to parse Core Components section
    - Implement `derive_feature_name()` to convert problem to kebab-case
    - Add validation for required sections (overview, components, diagram, trade-offs)
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ]* 2.2 Write property test for Mermaid round-trip
    - **Property 1: Mermaid diagram round-trip preservation**
    - **Validates: Requirements 1.2, 3.2**

  - [ ]* 2.3 Write property test for component extraction
    - **Property 3: Component extraction accuracy**
    - **Validates: Requirements 1.3**

  - [ ]* 2.4 Write property test for malformed input rejection
    - **Property 4: Malformed input rejection**
    - **Validates: Requirements 1.4**

  - [ ]* 2.5 Write property test for feature name kebab-case
    - **Property 22: Feature name kebab-case**
    - **Validates: Requirements 5.3**

- [x] 3. Implement Requirements Generator
  - [x] 3.1 Create RequirementsGenerator class
    - Implement `generate()` method to produce requirements.md content
    - Implement `create_glossary()` to extract AWS service definitions
    - Implement `create_user_story()` to generate user stories from components
    - Implement `create_acceptance_criteria()` with EARS pattern formatting
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ]* 3.2 Write property test for document structure
    - **Property 5: Document structure completeness**
    - **Validates: Requirements 2.1**

  - [ ]* 3.3 Write property test for glossary completeness
    - **Property 6: Glossary completeness**
    - **Validates: Requirements 2.2**

  - [ ]* 3.4 Write property test for requirements count
    - **Property 7: Requirements count relationship**
    - **Validates: Requirements 2.3, 2.5**

  - [ ]* 3.5 Write property test for EARS compliance
    - **Property 8: EARS pattern compliance**
    - **Validates: Requirements 2.4**

- [ ] 4. Implement Design Generator
  - [x] 4.1 Create DesignGenerator class
    - Implement `generate()` method to produce design.md content
    - Implement `generate_interfaces()` for TypeScript/Python interface definitions
    - Implement `generate_data_models()` for data structure definitions
    - Implement `derive_properties()` to create correctness properties from criteria
    - Include error handling and testing strategy sections
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

  - [ ]* 4.2 Write property test for interface definitions
    - **Property 9: Interface definitions presence**
    - **Validates: Requirements 3.3**

  - [ ]* 4.3 Write property test for data models
    - **Property 10: Data models presence**
    - **Validates: Requirements 3.4**

  - [ ]* 4.4 Write property test for property derivation
    - **Property 11: Correctness property derivation**
    - **Validates: Requirements 3.5**

  - [ ]* 4.5 Write property test for property format
    - **Property 12: Correctness property format**
    - **Validates: Requirements 7.2**

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement Tasks Generator
  - [x] 6.1 Create TasksGenerator class
    - Implement `generate()` method to produce tasks.md content
    - Implement `create_setup_tasks()` for project initialization tasks
    - Implement `create_component_tasks()` for implementation tasks per component
    - Implement `create_property_test_tasks()` for optional test tasks with "*" marking
    - Implement `create_checkpoint_tasks()` for test verification tasks
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ]* 6.2 Write property test for checkbox format
    - **Property 13: Task checkbox format**
    - **Validates: Requirements 4.1**

  - [ ]* 6.3 Write property test for task ordering
    - **Property 14: Task logical ordering**
    - **Validates: Requirements 4.2**

  - [ ]* 6.4 Write property test for sub-task structure
    - **Property 15: Sub-task structure**
    - **Validates: Requirements 4.3**

  - [ ]* 6.5 Write property test for requirement references
    - **Property 16: Task requirement references**
    - **Validates: Requirements 4.4, 7.3**

  - [ ]* 6.6 Write property test for optional marking
    - **Property 17: Optional test task marking**
    - **Validates: Requirements 4.5**

  - [ ]* 6.7 Write property test for checkpoint presence
    - **Property 18: Checkpoint task presence**
    - **Validates: Requirements 4.6**

  - [ ]* 6.8 Write property test for property test task format
    - **Property 19: Property test task format**
    - **Validates: Requirements 7.4**

- [x] 7. Implement ZIP Packager
  - [x] 7.1 Create ZipPackager class
    - Implement `package()` method to orchestrate ZIP creation and upload
    - Implement `create_zip()` to build in-memory ZIP with folder structure
    - Implement `upload_to_s3()` to upload ZIP to assets bucket
    - Implement `generate_presigned_url()` with 24-hour expiration
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 7.2 Write property test for ZIP creation
    - **Property 20: ZIP file creation**
    - **Validates: Requirements 5.1**

  - [ ]* 7.3 Write property test for folder structure
    - **Property 21: ZIP folder structure**
    - **Validates: Requirements 5.2**

  - [ ]* 7.4 Write property test for presigned URL format
    - **Property 23: S3 presigned URL format**
    - **Validates: Requirements 5.4**

- [x] 8. Implement Spec Generator Agent
  - [x] 8.1 Create spec_generator Strands Agent in `agents/spec_generator/generator.py`
    - Define Agent with `BedrockModel(model_id="anthropic.claude-sonnet-4-v1")` (same as other agents)
    - Set `spec_generator_agent.name = "spec_generator"` after initialization (following existing pattern)
    - Write system_prompt for spec generation from synthesis
    - _Requirements: 1.1, 7.1, 7.5_

  - [x] 8.2 Create `generate_spec_package()` function in generator.py
    - Accept problem, synthesis_output, mermaid_diagram, session_id parameters
    - Orchestrate parser → agent generation → packager pipeline
    - Return `SpecResult` with download_url and feature_name
    - Handle errors and return appropriate responses
    - _Requirements: 1.1, 1.4, 6.4_

  - [x] 8.3 Update `agents/spec_generator/__init__.py` with exports
    - Export `spec_generator_agent`, `generate_spec_package`
    - Follow pattern from `agents/synthesis/__init__.py`
    - _Requirements: 1.1_

  - [ ]* 8.4 Write property test for synthesis input completeness
    - **Property 2: Synthesis input completeness**
    - **Validates: Requirements 1.1**

  - [ ]* 8.5 Write property test for markdown formatting
    - **Property 27: Markdown formatting validity**
    - **Validates: Requirements 7.1**

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Integrate with Orchestrator in `agents/orchestrator/app.py`
  - [ ] 10.1 Update `debate_orchestrator()` to invoke Spec Generator
    - Add import: `from spec_generator import generate_spec_package`
    - Call `generate_spec_package()` after synthesis completes (after line ~130)
    - Add `specDownloadUrl` to return dict
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ] 10.2 Add error handling for spec generation failures
    - Wrap spec generation in try/except
    - On failure, still return synthesis result but with `specDownloadUrl: None`
    - Log error but don't fail the entire debate
    - _Requirements: 6.4_

  - [ ]* 10.3 Write property test for orchestrator invocation
    - **Property 24: Orchestrator invocation**
    - **Validates: Requirements 6.1**

  - [ ]* 10.4 Write property test for completion message
    - **Property 25: Completion message with URL**
    - **Validates: Requirements 6.3**

  - [ ]* 10.5 Write property test for error handling
    - **Property 26: Error handling session preservation**
    - **Validates: Requirements 6.4**

- [ ] 11. Add spec generation fields to orchestrator response
  - [ ] 11.1 Update return dict structure in `debate_orchestrator()`
    - Add `specDownloadUrl` field (string or None)
    - Add `specFeatureName` field for the generated feature name
    - Add `specGenerationStatus` field ("complete", "failed", or "skipped")
    - Ensure backward compatibility with existing response format
    - _Requirements: 6.2, 6.3, 6.4_

- [ ]* 12. Create integration tests
  - Write end-to-end test for full spec generation pipeline
  - Test ZIP extraction and folder structure verification
  - Test WebSocket message sequence (started → ready)
  - Test error recovery scenarios

- [ ] 13. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

