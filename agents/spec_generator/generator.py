"""Spec generator agent for creating Kiro spec packages from synthesis output."""

import re
import json
from dataclasses import dataclass
from typing import Optional

from strands import Agent
from strands.models import BedrockModel

from .parser import InputParser, ParsedArchitecture
from .packager import ZipPackager, SpecPackage, PackageResult


@dataclass
class SpecResult:
    """Result of spec generation."""
    download_url: Optional[str]
    feature_name: str
    status: str  # "complete", "failed"
    error: Optional[str] = None
    local_path: Optional[str] = None


# Create the spec generator agent following existing patterns
spec_generator_agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    system_prompt="""You are a Kiro spec generator that transforms synthesized architecture designs into structured specification documents.

Your task is to generate THREE separate markdown documents from the provided architecture synthesis:

1. **requirements.md** - Requirements document with:
   - Introduction summarizing the architecture
   - Glossary of AWS services and technical terms
   - Numbered requirements with user stories ("As a [role], I want [feature], so that [benefit]")
   - Acceptance criteria using EARS patterns (WHEN/THEN, WHILE, IF/THEN)

2. **design.md** - Design document with:
   - Overview explaining the architecture philosophy
   - Architecture section with the Mermaid diagram (preserve exactly as provided)
   - Components and Interfaces with TypeScript or Python interface definitions
   - Data Models section
   - Correctness Properties using "*For any* [input], [condition] SHALL [outcome]" format
   - Error Handling section
   - Testing Strategy section

3. **tasks.md** - Implementation plan with:
   - Numbered checkbox tasks (- [ ] format)
   - Sub-tasks with decimal notation (2.1, 2.2)
   - Requirements references (_Requirements: X.Y_)
   - Optional property test tasks marked with * (- [ ]*)
   - Checkpoint tasks for test verification

IMPORTANT RULES:
- Preserve the satirical over-engineering humor while maintaining technical validity
- Use proper markdown formatting
- Each acceptance criterion must use an EARS pattern
- Each correctness property must start with "*For any*" and contain "SHALL"
- Reference requirements in tasks using "_Requirements: X.Y_" format

OUTPUT FORMAT:
Return a JSON object with three keys: "requirements", "design", "tasks"
Each value should be the complete markdown content for that document."""
)

# Set the agent name after initialization (following existing pattern)
spec_generator_agent.name = "spec_generator"


def generate_spec_package(
    problem: str,
    synthesis_output: str,
    mermaid_diagram: str,
    session_id: str = "",
    s3_bucket: Optional[str] = None,
    local_only: bool = False
) -> SpecResult:
    """
    Generate a complete Kiro spec package from synthesis output.
    
    Args:
        problem: Original problem statement
        synthesis_output: Full synthesis text from Synthesis Agent
        mermaid_diagram: Extracted Mermaid diagram code
        session_id: Optional session ID for tracking
        s3_bucket: Optional S3 bucket for upload
        local_only: If True, save locally instead of S3
        
    Returns:
        SpecResult with download URL or local path
    """
    try:
        # Parse the synthesis output
        parser = InputParser()
        
        try:
            architecture = parser.parse(synthesis_output, problem)
        except ValueError as e:
            return SpecResult(
                download_url=None,
                feature_name="",
                status="failed",
                error=f"Parse error: {str(e)}"
            )
        
        # Build the prompt for the agent
        prompt = _build_generation_prompt(architecture, mermaid_diagram)
        
        # Invoke the spec generator agent
        response = spec_generator_agent(prompt)
        response_text = str(response)
        
        # Parse the agent's response
        try:
            docs = _parse_agent_response(response_text)
        except Exception as e:
            return SpecResult(
                download_url=None,
                feature_name=architecture.feature_name,
                status="failed",
                error=f"Failed to parse agent response: {str(e)}"
            )
        
        # Create the spec package
        spec = SpecPackage(
            feature_name=architecture.feature_name,
            requirements_md=docs['requirements'],
            design_md=docs['design'],
            tasks_md=docs['tasks']
        )
        
        # Package and upload
        if local_only:
            packager = ZipPackager(s3_bucket)
            local_path = packager.create_local_zip(spec)
            return SpecResult(
                download_url=None,
                feature_name=architecture.feature_name,
                status="complete",
                local_path=local_path
            )
        else:
            packager = ZipPackager(s3_bucket)
            try:
                result = packager.package(spec, session_id)
                return SpecResult(
                    download_url=result.download_url,
                    feature_name=result.feature_name,
                    status="complete"
                )
            except Exception as e:
                # Fall back to local if S3 fails
                local_path = packager.create_local_zip(spec)
                return SpecResult(
                    download_url=None,
                    feature_name=architecture.feature_name,
                    status="complete",
                    error=f"S3 upload failed, saved locally: {str(e)}",
                    local_path=local_path
                )
    
    except Exception as e:
        return SpecResult(
            download_url=None,
            feature_name="",
            status="failed",
            error=f"Spec generation failed: {str(e)}"
        )


def _build_generation_prompt(architecture: ParsedArchitecture, mermaid_diagram: str) -> str:
    """Build the prompt for the spec generator agent."""
    components_list = "\n".join([
        f"- **{c.name}** ({c.service_type}): {c.responsibility}"
        for c in architecture.components
    ])
    
    trade_offs_list = "\n".join([
        f"- **{t.aspect}**: {t.description}"
        for t in architecture.trade_offs
    ])
    
    return f"""Generate a complete Kiro spec package for the following architecture:

## Original Problem
{architecture.original_problem}

## Feature Name
{architecture.feature_name}

## Architecture Overview
{architecture.overview}

## Core Components
{components_list}

## Mermaid Diagram (preserve exactly)
```mermaid
{mermaid_diagram}
```

## Trade-offs
{trade_offs_list}

Please generate the three spec documents (requirements.md, design.md, tasks.md) as a JSON object.
Remember to:
1. Use EARS patterns for acceptance criteria
2. Use "*For any*" format for correctness properties
3. Mark property test tasks as optional with "*"
4. Include checkpoint tasks
5. Preserve the satirical over-engineering humor"""


def _parse_agent_response(response_text: str) -> dict:
    """Parse the agent's JSON response into document contents."""
    # Try to extract JSON from the response
    import re
    
    # Look for JSON block
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{[\s\S]*"requirements"[\s\S]*"design"[\s\S]*"tasks"[\s\S]*\}', response_text)
        if json_match:
            json_str = json_match.group(0)
        else:
            # Fall back to generating basic docs from the response
            return _generate_fallback_docs(response_text)
    
    try:
        docs = json.loads(json_str)
        if all(k in docs for k in ['requirements', 'design', 'tasks']):
            return docs
    except json.JSONDecodeError:
        pass
    
    return _generate_fallback_docs(response_text)


def _generate_fallback_docs(response_text: str) -> dict:
    """Generate basic docs if JSON parsing fails."""
    # Split response by document markers if present
    sections = {
        'requirements': '',
        'design': '',
        'tasks': ''
    }
    
    # Try to find sections by headers
    req_match = re.search(r'#\s*Requirements.*?(?=#\s*Design|#\s*Tasks|\Z)', response_text, re.DOTALL | re.IGNORECASE)
    design_match = re.search(r'#\s*Design.*?(?=#\s*Tasks|#\s*Implementation|\Z)', response_text, re.DOTALL | re.IGNORECASE)
    tasks_match = re.search(r'#\s*(Tasks|Implementation).*', response_text, re.DOTALL | re.IGNORECASE)
    
    if req_match:
        sections['requirements'] = req_match.group(0).strip()
    if design_match:
        sections['design'] = design_match.group(0).strip()
    if tasks_match:
        sections['tasks'] = tasks_match.group(0).strip()
    
    # If still empty, use the whole response for each
    if not any(sections.values()):
        sections['requirements'] = f"# Requirements Document\n\n{response_text[:3000]}"
        sections['design'] = f"# Design Document\n\n{response_text}"
        sections['tasks'] = "# Implementation Plan\n\n- [ ] 1. Review generated architecture\n- [ ] 2. Implement core components\n- [ ] 3. Add tests"
    
    return sections
