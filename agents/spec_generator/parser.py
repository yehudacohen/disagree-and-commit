"""Input parser for extracting structured data from synthesis output."""

import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Component:
    """A service or module in the architecture."""
    name: str
    service_type: str  # e.g., "Lambda", "DynamoDB", "API Gateway"
    responsibility: str
    relationships: List[str] = field(default_factory=list)


@dataclass
class TradeOff:
    """A trade-off identified in the synthesis."""
    aspect: str
    description: str


@dataclass
class ParsedArchitecture:
    """Structured representation of synthesis output."""
    overview: str
    components: List[Component]
    mermaid_diagram: str
    trade_offs: List[TradeOff]
    original_problem: str
    feature_name: str


class InputParser:
    """Parser for extracting structured data from synthesis output."""
    
    # Common AWS services for detection
    AWS_SERVICES = [
        'Lambda', 'DynamoDB', 'S3', 'API Gateway', 'SQS', 'SNS', 'EventBridge',
        'Step Functions', 'Bedrock', 'SageMaker', 'CloudFront', 'Route 53',
        'ECS', 'EKS', 'Fargate', 'EC2', 'RDS', 'Aurora', 'ElastiCache',
        'Kinesis', 'Cognito', 'IAM', 'CloudWatch', 'X-Ray', 'AppSync',
        'Amplify', 'CodePipeline', 'CodeBuild', 'CodeDeploy', 'CloudFormation',
        'CDK', 'SAM', 'Secrets Manager', 'Parameter Store', 'KMS'
    ]
    
    def parse(self, synthesis_output: str, problem: str) -> ParsedArchitecture:
        """
        Parse synthesis output into structured architecture.
        
        Args:
            synthesis_output: Raw synthesis text from Synthesis Agent
            problem: Original problem statement
            
        Returns:
            ParsedArchitecture with extracted components
            
        Raises:
            ValueError: If required sections are missing
        """
        # Validate required sections
        missing = self._validate_sections(synthesis_output)
        if missing:
            raise ValueError(f"Missing required sections: {', '.join(missing)}")
        
        overview = self._extract_overview(synthesis_output)
        components = self._extract_components(synthesis_output)
        mermaid_diagram = self.extract_mermaid(synthesis_output)
        trade_offs = self._extract_trade_offs(synthesis_output)
        feature_name = self.derive_feature_name(problem)
        
        return ParsedArchitecture(
            overview=overview,
            components=components,
            mermaid_diagram=mermaid_diagram,
            trade_offs=trade_offs,
            original_problem=problem,
            feature_name=feature_name
        )
    
    def _validate_sections(self, text: str) -> List[str]:
        """Check for required sections and return list of missing ones."""
        missing = []
        
        # Check for overview section
        if not re.search(r'##\s*(Architecture\s+)?Overview', text, re.IGNORECASE):
            missing.append('Architecture Overview')
        
        # Check for components section
        if not re.search(r'##\s*(Core\s+)?Components', text, re.IGNORECASE):
            missing.append('Core Components')
        
        # Check for Mermaid diagram
        if not re.search(r'```mermaid', text, re.IGNORECASE):
            missing.append('Mermaid Diagram')
        
        # Check for trade-offs section
        if not re.search(r'##\s*Trade-?offs?', text, re.IGNORECASE):
            missing.append('Trade-offs')
        
        return missing
    
    def _extract_overview(self, text: str) -> str:
        """Extract the Architecture Overview section."""
        pattern = r'##\s*(?:Architecture\s+)?Overview\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def extract_mermaid(self, text: str) -> str:
        """Extract Mermaid diagram from markdown code block."""
        pattern = r'```mermaid\s*\n(.*?)\n```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_components(self, text: str) -> List[Component]:
        """Extract component definitions from Core Components section."""
        components = []
        
        # Extract the Core Components section
        pattern = r'##\s*(?:Core\s+)?Components\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if not match:
            return components
        
        section = match.group(1)
        
        # Find AWS services mentioned
        for service in self.AWS_SERVICES:
            if service.lower() in section.lower():
                # Try to extract context around the service mention
                service_pattern = rf'[-*]\s*\**{re.escape(service)}\**[:\s]*(.*?)(?=\n[-*]|\n\n|\Z)'
                service_match = re.search(service_pattern, section, re.IGNORECASE | re.DOTALL)
                
                responsibility = ""
                if service_match:
                    responsibility = service_match.group(1).strip()[:200]
                
                components.append(Component(
                    name=service,
                    service_type=self._categorize_service(service),
                    responsibility=responsibility or f"Provides {service} functionality"
                ))
        
        # If no components found, create generic ones from bullet points
        if not components:
            bullet_pattern = r'[-*]\s*\**([^:\n]+)\**[:\s]*(.*?)(?=\n[-*]|\n\n|\Z)'
            for match in re.finditer(bullet_pattern, section, re.DOTALL):
                name = match.group(1).strip()
                responsibility = match.group(2).strip()[:200]
                components.append(Component(
                    name=name,
                    service_type="Service",
                    responsibility=responsibility or f"Handles {name} functionality"
                ))
        
        return components[:10]  # Limit to 10 components
    
    def _categorize_service(self, service: str) -> str:
        """Categorize an AWS service by type."""
        compute = ['Lambda', 'ECS', 'EKS', 'Fargate', 'EC2']
        storage = ['S3', 'DynamoDB', 'RDS', 'Aurora', 'ElastiCache']
        messaging = ['SQS', 'SNS', 'EventBridge', 'Kinesis']
        api = ['API Gateway', 'AppSync']
        ml = ['Bedrock', 'SageMaker']
        
        if service in compute:
            return "Compute"
        elif service in storage:
            return "Storage"
        elif service in messaging:
            return "Messaging"
        elif service in api:
            return "API"
        elif service in ml:
            return "AI/ML"
        else:
            return "Service"
    
    def _extract_trade_offs(self, text: str) -> List[TradeOff]:
        """Extract trade-offs from the Trade-offs section."""
        trade_offs = []
        
        pattern = r'##\s*Trade-?offs?\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if not match:
            return trade_offs
        
        section = match.group(1)
        
        # Extract bullet points as trade-offs
        bullet_pattern = r'[-*]\s*\**([^:\n]+)\**[:\s]*(.*?)(?=\n[-*]|\n\n|\Z)'
        for match in re.finditer(bullet_pattern, section, re.DOTALL):
            aspect = match.group(1).strip()
            description = match.group(2).strip()
            trade_offs.append(TradeOff(aspect=aspect, description=description))
        
        # If no bullet points, treat whole section as one trade-off
        if not trade_offs and section.strip():
            trade_offs.append(TradeOff(
                aspect="Architecture Trade-offs",
                description=section.strip()[:500]
            ))
        
        return trade_offs[:5]  # Limit to 5 trade-offs
    
    def derive_feature_name(self, problem: str) -> str:
        """Convert problem statement to kebab-case feature name."""
        # Take first 50 chars of problem
        text = problem[:50].lower()
        
        # Remove special characters, keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Replace spaces with hyphens
        text = re.sub(r'\s+', '-', text.strip())
        
        # Remove leading/trailing hyphens
        text = text.strip('-')
        
        # Limit length
        if len(text) > 30:
            text = text[:30].rsplit('-', 1)[0]
        
        return text or "generated-spec"
