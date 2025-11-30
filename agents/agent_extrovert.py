"""
Personality-driven agent implementation using Strands framework.
Includes agent, avatar, and interactive testing functionality.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import uuid
import re
import time
import json


class TraitType(Enum):
    """Supported personality trait types."""
    ANGRY = "angry"
    EXTROVERT = "extrovert"
    CALM = "calm"
    INTROVERTED = "introverted"
    ENTHUSIASTIC = "enthusiastic"
    SERIOUS = "serious"


@dataclass
class PersonalityTrait:
    """Represents a single personality trait with intensity."""
    trait_type: TraitType
    intensity: float  # 0.0 to 1.0
    behavioral_params: Dict[str, any]
    
    def __post_init__(self):
        if not 0.0 <= self.intensity <= 1.0:
            raise ValueError("Intensity must be between 0.0 and 1.0")


@dataclass
class PersonalityContext:
    """Configuration data defining an agent's personality."""
    agent_id: str
    traits: List[PersonalityTrait]
    system_prompt_modifier: str
    animation_intensity_multiplier: float
    
    def get_dominant_trait(self) -> PersonalityTrait:
        """Get the trait with highest intensity."""
        return max(self.traits, key=lambda t: t.intensity)


# Behavioral mappings for each trait type
TRAIT_BEHAVIORS = {
    TraitType.ANGRY: {
        "tone_keywords": ["assertive", "direct", "intense"],
        "language_style": "short sentences, strong verbs, exclamation points",
        "animation_intensity": 1.2,
        "mouth_speed_multiplier": 1.3
    },
    TraitType.EXTROVERT: {
        "tone_keywords": ["enthusiastic", "engaging", "expressive"],
        "language_style": "conversational, exclamations, questions",
        "animation_intensity": 1.4,
        "mouth_speed_multiplier": 1.2
    },
    TraitType.CALM: {
        "tone_keywords": ["measured", "thoughtful", "gentle"],
        "language_style": "longer sentences, soothing words, periods",
        "animation_intensity": 0.7,
        "mouth_speed_multiplier": 0.9
    },
    TraitType.INTROVERTED: {
        "tone_keywords": ["reserved", "precise", "considerate"],
        "language_style": "careful word choice, complete thoughts",
        "animation_intensity": 0.6,
        "mouth_speed_multiplier": 0.85
    }
}


class PersonalityAgentError(Exception):
    """Base exception for personality agent system."""
    pass


class InvalidPersonalityConfigError(PersonalityAgentError):
    """Raised when personality configuration is invalid."""
    pass


class AgentProcessingError(PersonalityAgentError):
    """Raised when agent fails to process query."""
    pass


class PersonalityManager:
    """Manages personality configurations for agents."""
    
    def __init__(self):
        self._personalities: Dict[str, PersonalityContext] = {}
    
    def create_personality(self, agent_id: str, traits: List[PersonalityTrait]) -> PersonalityContext:
        """Create a new personality configuration."""
        for trait in traits:
            self._validate_trait(trait)
        
        system_prompt_modifier = self.generate_system_prompt_modifier(traits)
        animation_intensity = self._calculate_animation_intensity(traits)
        
        context = PersonalityContext(
            agent_id=agent_id,
            traits=traits,
            system_prompt_modifier=system_prompt_modifier,
            animation_intensity_multiplier=animation_intensity
        )
        
        self._personalities[agent_id] = context
        return context
    
    def get_personality(self, agent_id: str) -> PersonalityContext:
        """Retrieve personality configuration for an agent."""
        if agent_id not in self._personalities:
            raise InvalidPersonalityConfigError(f"No personality found for agent: {agent_id}")
        return self._personalities[agent_id]
    
    def update_personality(self, agent_id: str, traits: List[PersonalityTrait]) -> PersonalityContext:
        """Update personality configuration for an agent."""
        return self.create_personality(agent_id, traits)
    
    def generate_system_prompt_modifier(self, traits: List[PersonalityTrait]) -> str:
        """Generate system prompt modifier based on traits."""
        if not traits:
            return ""
        
        dominant_trait = max(traits, key=lambda t: t.intensity)
        behavior = TRAIT_BEHAVIORS.get(dominant_trait.trait_type, {})
        
        tone_keywords = ", ".join(behavior.get("tone_keywords", []))
        language_style = behavior.get("language_style", "")
        
        return f"Respond in a {tone_keywords} manner. Use {language_style}."
    
    def _validate_trait(self, trait: PersonalityTrait) -> None:
        """Validate a personality trait."""
        if trait.trait_type not in TraitType:
            raise InvalidPersonalityConfigError(
                f"Invalid trait type: {trait.trait_type}. "
                f"Must be one of: {[t.value for t in TraitType]}"
            )
        
        if not 0.0 <= trait.intensity <= 1.0:
            raise InvalidPersonalityConfigError(
                f"Intensity must be between 0.0 and 1.0, got: {trait.intensity}"
            )
    
    def _calculate_animation_intensity(self, traits: List[PersonalityTrait]) -> float:
        """Calculate animation intensity multiplier from traits."""
        if not traits:
            return 1.0
        
        dominant_trait = max(traits, key=lambda t: t.intensity)
        behavior = TRAIT_BEHAVIORS.get(dominant_trait.trait_type, {})
        return behavior.get("animation_intensity", 1.0)


class PersonalityAgent:
    """Agent that processes queries with personality influence."""
    
    def __init__(self, personality_context: PersonalityContext):
        self.personality = personality_context
        self.agent = self._create_strands_agent()
    
    def _create_strands_agent(self):
        """Create Strands agent with personality-modified system prompt."""
        from strands import Agent
        
        system_prompt = self._build_system_prompt()
        return Agent(
            model="openai.gpt-oss-120b-1:0",
            system_prompt=system_prompt
        )
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with personality modifiers."""
        base_prompt = "You are a helpful AI assistant that provides advice."
        return f"{base_prompt}\n\n{self.personality.system_prompt_modifier}"
    
    def process_query(self, user_query: str) -> str:
        """Process user query and return advice."""
        if not user_query or not user_query.strip():
            raise AgentProcessingError("Query cannot be empty")
        
        if len(user_query) > 10000:
            raise AgentProcessingError("Query exceeds maximum length")
        
        # Process through Strands agent
        response = self.agent(user_query)
        
        # Handle different response types from Strands
        if isinstance(response, dict):
            # Extract text from Bedrock response structure
            content = response.get('content', [])
            if isinstance(content, list):
                # Find the text content (skip reasoning)
                for item in content:
                    if isinstance(item, dict) and 'text' in item:
                        return item['text']
            # Fallback to other common keys
            return response.get('message', str(response))
        elif hasattr(response, 'message'):
            return response.message
        elif hasattr(response, 'content'):
            return response.content
        else:
            # Fallback: convert to string
            return str(response)


class AgentService:
    """Service for managing agent lifecycle."""
    
    def __init__(self):
        self.personality_manager = PersonalityManager()
        self._agents: Dict[str, PersonalityAgent] = {}
    
    def initialize_agent(self, agent_id: str, traits: List[PersonalityTrait]) -> PersonalityAgent:
        """Initialize a new agent with personality."""
        personality = self.personality_manager.create_personality(agent_id, traits)
        agent = PersonalityAgent(personality)
        self._agents[agent_id] = agent
        return agent
    
    def get_agent(self, agent_id: str) -> PersonalityAgent:
        """Get an existing agent."""
        if agent_id not in self._agents:
            raise AgentProcessingError(f"Agent not found: {agent_id}")
        return self._agents[agent_id]
    
    def process_query(self, agent_id: str, query: str) -> str:
        """Process a query through an agent."""
        agent = self.get_agent(agent_id)
        return agent.process_query(query)


# ============================================================================
# AVATAR COMPONENTS
# ============================================================================

@dataclass
class AvatarConfig:
    """Configuration for avatar appearance and animation."""
    agent_id: str
    visual_style: str
    animation_intensity: float
    base_mouth_speed: float  # words per second


@dataclass
class AnimationFrame:
    """Single frame of avatar animation."""
    mouth_position: str  # "closed", "open", "wide", "smile"
    timestamp: float
    duration: float
    intensity: float


class AvatarRenderingError(Exception):
    """Raised when avatar fails to render."""
    pass


class AvatarRenderer:
    """Renders avatar with personality-influenced animations."""
    
    def __init__(self):
        self._avatars = {}
    
    def initialize_avatar(self, config: AvatarConfig):
        """Initialize an avatar with configuration."""
        self._avatars[config.agent_id] = config
        return config
    
    def animate_speech(self, text: str, personality_context) -> List[AnimationFrame]:
        """Generate animation frames for speech output."""
        # Ensure text is a string
        if isinstance(text, dict):
            text = text.get('message', text.get('content', str(text)))
        
        text = str(text) if text else ""
        
        if not text or not text.strip():
            return []
        
        frames = []
        words = self._extract_words(text)
        
        if not words:
            return []
        
        # Calculate timing based on text length and personality
        animation_intensity = personality_context.animation_intensity_multiplier
        base_duration = 0.15  # seconds per word
        
        current_time = 0.0
        
        for i, word in enumerate(words):
            # Determine mouth position based on word characteristics
            mouth_position = self._calculate_mouth_position(word, animation_intensity)
            
            # Calculate duration based on word length
            duration = len(word) * 0.05 * (1.0 / animation_intensity)
            
            frame = AnimationFrame(
                mouth_position=mouth_position,
                timestamp=current_time,
                duration=duration,
                intensity=animation_intensity
            )
            
            frames.append(frame)
            current_time += duration
        
        return frames
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text."""
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def _calculate_mouth_position(self, word: str, intensity: float) -> str:
        """Calculate mouth position based on word and intensity."""
        # Simple heuristic: longer words or higher intensity = more open mouth
        word_length = len(word)
        
        if intensity > 1.2:
            return "wide" if word_length > 5 else "open"
        elif intensity < 0.8:
            return "open" if word_length > 6 else "closed"
        else:
            return "open" if word_length > 4 else "closed"
    
    def set_idle_state(self, agent_id: str) -> AnimationFrame:
        """Return idle state animation frame."""
        return AnimationFrame(
            mouth_position="closed",
            timestamp=0.0,
            duration=0.0,
            intensity=0.0
        )
    
    def render_frame(self, agent_id: str, frame: AnimationFrame) -> None:
        """Render a single animation frame (placeholder)."""
        # This would integrate with actual rendering library (Lottie, Canvas, etc.)
        pass


@dataclass
class InteractionResult:
    """Result of a complete user interaction."""
    agent_id: str
    query: str
    advice: str
    animation_frames: List[AnimationFrame]
    personality_applied: any  # PersonalityContext
    processing_time: float = 0.0


class InteractionCoordinator:
    """Coordinates between agent and avatar components."""
    
    def __init__(self, agent_service: Optional[AgentService] = None):
        self.agent_service = agent_service or AgentService()
        self.avatar_renderer = AvatarRenderer()
    
    def handle_user_query(self, agent_id: str, query: str) -> InteractionResult:
        """Handle a complete user query interaction."""
        start_time = time.time()
        
        # Get agent and process query
        agent = self.agent_service.get_agent(agent_id)
        advice = agent.process_query(query)
        
        # Generate avatar animations
        animation_frames = self.avatar_renderer.animate_speech(
            advice, 
            agent.personality
        )
        
        processing_time = time.time() - start_time
        
        return InteractionResult(
            agent_id=agent_id,
            query=query,
            advice=advice,
            animation_frames=animation_frames,
            personality_applied=agent.personality,
            processing_time=processing_time
        )


# ============================================================================
# INTERACTIVE TEST MODE
# ============================================================================

def run_interactive():
    """Run interactive agent test."""
    
    # Initialize agent service
    service = AgentService()
    
    # Create an extrovert agent
    traits = [
        PersonalityTrait(
            trait_type=TraitType.EXTROVERT,
            intensity=0.8,
            behavioral_params={}
        )
    ]
    
    agent_id = "helpful_extrovert"
    service.initialize_agent(agent_id, traits)
    
    # Initialize coordinator
    coordinator = InteractionCoordinator(agent_service=service)
    
    print("🤖 Personality Avatar Agent - Interactive Mode")
    print(f"Agent: {agent_id} (Extrovert personality)")
    print("Type 'salir', 'exit', or 'q' to quit\n")
    
    # 💬 Loop interactivo (dueño puede seguir preguntando)
    while True:
        q = input("\n💬 Pregunta del user: ")
        
        if q.lower() in ["salir", "exit", "q"]:
            print("👋 Hasta luego!")
            break
        
        try:
            # Process query through coordinator
            result = coordinator.handle_user_query(agent_id, q)
            
            print(f"\n🤖 {result.advice}")
            print(f"\n📊 Animation frames: {len(result.animation_frames)}")
            print(f"⏱️  Processing time: {result.processing_time:.2f}s\n")
            
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    run_interactive()

