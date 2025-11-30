// Core type definitions for Disagree and Commit UI

export type FrustrationLevel = 1 | 2 | 3 | 4 | 5;

export interface Expert {
  id: 'jeff' | 'swami' | 'werner';
  name: string;
  title: string;
  color: string; // 'orange' | 'blue' | 'purple'
  catchphrase: string;
  badge: string;
  avatarImage: string; // Static fallback image
  lottieAnimations: {
    idle: string;      // Lottie JSON URL
    speaking: string;  // Lottie JSON URL
    frustrated: Record<FrustrationLevel, string>; // Lottie JSON URLs per level
  };
}

export interface DebateMessage {
  id: string;
  expertId: string;
  content: string;
  audioUrl?: string;  // Nova Sonic generated audio URL from S3
  reactionImageUrl?: string; // Nova Canvas generated image URL
  timestamp: number;
  isDisagreement: boolean;
}

export interface StreamingMessage {
  expertId: string;
  partialContent: string;
}

export interface ServiceCost {
  service: string;
  cost: number;
  justification: string; // e.g., "47 Lambda functions for 'flexibility'"
}

export interface CostEstimate {
  monthly: number;
  breakdown: ServiceCost[];
  satiricalNote: string; // e.g., "This is actually cheaper than your current Kubernetes cluster"
}

export interface AssetsFolder {
  diagramPngUrl: string;
  mermaidSourceUrl: string;
}

export interface FinalArchitecture {
  mermaidDiagram: string;
  costEstimate: CostEstimate;
  expertEndorsements: Record<string, string>;
  assetsFolder: AssetsFolder;
  generatedAt: number;
}

// WebSocket message types

// Messages sent TO backend (action field for route selection)
export interface ClientMessage {
  action: 'submitProblem';
  problem: string;
  sessionId: string;
}

// Messages received FROM backend
export type WebSocketMessage =
  | { type: 'expert_speaking'; expertId: string }
  | { type: 'expert_response'; expertId: string; content: string; audioUrl?: string; isComplete: boolean }
  | { type: 'frustration_update'; expertId: string; level: FrustrationLevel; reactionImageUrl?: string }
  | { type: 'round_complete'; roundNumber: number }
  | { type: 'disagree_and_commit' }
  | { type: 'architecture_ready'; diagram: string; cost: CostEstimate; endorsements: Record<string, string>; assets: AssetsFolder };

// Debate session state
export interface DebateSession {
  sessionId: string;
  connectionId: string;
  problem: string;
  status: 'pending' | 'in_progress' | 'completed';
  currentRound: number;
  frustrationLevels: Record<string, FrustrationLevel>;
  messages: DebateMessage[];
  finalArchitecture?: FinalArchitecture;
  createdAt: number;
  ttl: number;
}
