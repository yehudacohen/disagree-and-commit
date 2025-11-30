import { useState, useEffect, useCallback } from 'react';
import './App.css';
import { PanelDisplay } from './components/PanelDisplay';
import { ProblemInput } from './components/ProblemInput';
import { FinaleOverlay } from './components/FinaleOverlay';
import { DebateDisplay } from './components/DebateDisplay';
import { ArchitectureReveal } from './components/ArchitectureReveal';
import AudioPlayer from './components/AudioPlayer';
import { EXPERTS } from './config/experts';
import { webSocketClient } from './services/WebSocketClient';
import { isDemoMode, getDemoAudioUrl, shouldShowDemoBanner, shouldShowFinaleAnimation, getArchitectureDiagramUrl } from './config/demo';
import type { 
  FrustrationLevel, 
  DebateMessage, 
  StreamingMessage,
  CostEstimate,
  AssetsFolder
} from './types';

function App() {
  // Debate state management
  const [debateStatus, setDebateStatus] = useState<'pending' | 'in_progress' | 'completed'>('pending');
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  
  // Expert state
  const [speakingExpertId, setSpeakingExpertId] = useState<string | null>(null);
  const [frustrationLevels, setFrustrationLevels] = useState<Record<string, FrustrationLevel>>({
    jeff: 1,
    swami: 1,
    werner: 1,
  });
  
  // Message state
  const [messages, setMessages] = useState<DebateMessage[]>([]);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState<StreamingMessage | null>(null);
  
  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [isFinaleTriggered, setIsFinaleTriggered] = useState(false);
  const [isArchitectureRevealed, setIsArchitectureRevealed] = useState(false);
  
  // Audio state
  const [currentAudioUrl, setCurrentAudioUrl] = useState<string | null>(null);
  const [currentAudioExpertId, setCurrentAudioExpertId] = useState<string>('');
  
  // Architecture reveal state
  const [finalArchitecture, setFinalArchitecture] = useState<{
    mermaidDiagram: string;
    costEstimate: CostEstimate;
    expertEndorsements: Record<string, string>;
    assetsFolder: AssetsFolder;
  } | null>(null);

  // WebSocket connection and message handling
  useEffect(() => {
    // Skip WebSocket connection in demo mode
    if (isDemoMode()) {
      console.log('[App] Running in DEMO MODE - WebSocket disabled');
      return;
    }

    // Connect to WebSocket when component mounts
    const connectWebSocket = async () => {
      try {
        await webSocketClient.connect(sessionId);
        console.log('[App] WebSocket connected');
      } catch (error) {
        console.error('[App] Failed to connect to WebSocket:', error);
      }
    };

    connectWebSocket();

    // Cleanup on unmount
    return () => {
      webSocketClient.disconnect();
    };
  }, [sessionId]);

  // Set up WebSocket message handlers
  useEffect(() => {
    // Handler for expert_speaking messages
    webSocketClient.onMessageType('expert_speaking', (msg) => {
      console.log('[App] Expert speaking:', msg.expertId);
      setSpeakingExpertId(msg.expertId);
    });

    // Handler for expert_response messages
    webSocketClient.onMessageType('expert_response', (msg) => {
      console.log('[App] Expert response:', msg.expertId, msg.isComplete);
      
      if (msg.isComplete) {
        // Complete message - add to messages array
        const newMessage: DebateMessage = {
          id: `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          expertId: msg.expertId,
          content: msg.content,
          audioUrl: msg.audioUrl,
          timestamp: Date.now(),
          isDisagreement: msg.content.toLowerCase().includes('disagree') || 
                         msg.content.toLowerCase().includes('but') ||
                         msg.content.toLowerCase().includes('however')
        };
        
        setMessages(prev => [...prev, newMessage]);
        setCurrentStreamingMessage(null);
        setSpeakingExpertId(null);
        
        // Play audio if available
        if (msg.audioUrl) {
          setCurrentAudioUrl(msg.audioUrl);
          setCurrentAudioExpertId(msg.expertId);
        }
      } else {
        // Streaming message - update streaming state
        setCurrentStreamingMessage({
          expertId: msg.expertId,
          partialContent: msg.content
        });
      }
    });

    // Handler for frustration_update messages
    webSocketClient.onMessageType('frustration_update', (msg) => {
      console.log('[App] Frustration update:', msg.expertId, msg.level);
      
      setFrustrationLevels(prev => ({
        ...prev,
        [msg.expertId]: msg.level
      }));
      
      // Trigger finale if any expert reaches level 5
      if (msg.level === 5) {
        setIsFinaleTriggered(true);
      }
    });

    // Handler for round_complete messages
    webSocketClient.onMessageType('round_complete', (msg) => {
      console.log('[App] Round complete:', msg.roundNumber);
      // Could add visual separator or round indicator here
    });

    // Handler for disagree_and_commit messages
    webSocketClient.onMessageType('disagree_and_commit', () => {
      console.log('[App] Disagree and commit triggered!');
      setIsFinaleTriggered(true);
    });

    // Handler for architecture_ready messages
    webSocketClient.onMessageType('architecture_ready', (msg) => {
      console.log('[App] Architecture ready');
      
      setFinalArchitecture({
        mermaidDiagram: msg.diagram,
        costEstimate: msg.cost,
        expertEndorsements: msg.endorsements,
        assetsFolder: msg.assets
      });
      
      setDebateStatus('completed');
    });

    // Note: We don't need to clean up handlers since we're using the singleton
    // and it will be cleaned up when the component unmounts via disconnect()
  }, []);

  // Detect when any expert reaches frustration level 5 and trigger finale
  useEffect(() => {
    if (isFinaleTriggered) {
      console.log('[App] Finale triggered! An expert reached frustration level 5');
      
      // Add dramatic body effect
      document.body.classList.add('finale-active');
      
      // Remove after animation completes
      const timer = setTimeout(() => {
        document.body.classList.remove('finale-active');
      }, 1000);
      
      return () => {
        clearTimeout(timer);
        document.body.classList.remove('finale-active');
      };
    }
  }, [isFinaleTriggered]);

  // Handle finale animation complete
  const handleFinaleComplete = useCallback(() => {
    console.log('[App] Finale animation complete');
    setIsArchitectureRevealed(true);
  }, []);

  // Simulate demo debate with pre-recorded audio - 4 rounds
  const simulateDemoDebate = useCallback(() => {
    const expertIds = ['jeff', 'swami', 'werner'];
    const rounds = [
      {
        name: 'Initial Opinions',
        getContent: (expertId: string) => {
          const opinions = {
            jeff: "Let me share my initial thoughts on this problem. We need to keep things simple and maintainable. I'd recommend starting with a straightforward approach that we can iterate on.",
            swami: "From my perspective, speed is critical here. We should leverage the latest technologies to ensure we can deliver results quickly and efficiently.",
            werner: "I think we need to consider scale from day one. This solution needs to handle growth, and we should architect it with distributed systems in mind."
          };
          return opinions[expertId as keyof typeof opinions];
        }
      },
      {
        name: 'Disagreements',
        getContent: (expertId: string) => {
          const disagreements = {
            jeff: "I have to disagree with the complexity being proposed here. Werner, your distributed approach is overkill for this use case. And Swami, chasing the latest tech isn't always the answer.",
            swami: "Jeff, simplicity is great, but we can't sacrifice performance. And Werner, your scaling concerns are premature optimization. We need to move fast first.",
            werner: "Both of you are missing the bigger picture. Jeff's simple approach won't scale, and Swami's speed-first mentality will create technical debt we'll regret."
          };
          return disagreements[expertId as keyof typeof disagreements];
        }
      },
      {
        name: 'Personal Callouts',
        getContent: (expertId: string) => {
          const callouts = {
            jeff: "Werner, you always do this! Every problem becomes a distributed systems exercise. And Swami, you're so focused on the latest shiny object that you forget about the developers who have to maintain this.",
            swami: "Jeff, your blog posts are great, but this isn't 2010 anymore. We need modern solutions. And Werner, not everything needs to be a white paper on scalability!",
            werner: "Jeff, your simplicity obsession is holding us back. And Swami, speed without architecture is just creating problems faster. You both need to think bigger!"
          };
          return callouts[expertId as keyof typeof callouts];
        }
      },
      {
        name: 'Disagree and Commit',
        getContent: (expertId: string) => {
          const commits = {
            jeff: "Look, I disagree with parts of this approach, but we need to move forward. I commit to supporting a solution that balances simplicity with the scale Werner wants and the speed Swami needs.",
            swami: "I still think we're overcomplicating this, but I respect your perspectives. I commit to this hybrid approach - we'll start fast but build in the scalability hooks Werner insists on.",
            werner: "Fine. I disagree with cutting corners, but I commit to this pragmatic solution. We'll build it Jeff's way initially, move at Swami's pace, and architect for scale as we grow."
          };
          return commits[expertId as keyof typeof commits];
        }
      }
    ];
    
    let currentRound = 0;
    let currentExpertIndex = 0;
    
    const addDemoMessage = () => {
      // Check if we've completed all rounds
      if (currentRound >= rounds.length) {
        // Set up demo architecture
        const architectureDiagramUrl = getArchitectureDiagramUrl();
        const demoArchitecture = {
          mermaidDiagram: architectureDiagramUrl 
            ? `graph TD\n    A[Demo Architecture]\n    B[See diagram image below]\n    A --> B`
            : `graph TD\n    A[User] -->|Submits Problem| B[API Gateway]\n    B --> C[WebSocket]\n    C --> D[Orchestrator Agent]\n    D --> E[Jeff Agent]\n    D --> F[Swami Agent]\n    D --> G[Werner Agent]\n    E --> H[Synthesis Agent]\n    F --> H\n    G --> H\n    H --> I[Architecture Diagram]\n    I --> J[S3 Assets]\n    J --> K[User Download]`,
          costEstimate: {
            monthly: 847.50,
            satiricalNote: "This is what happens when three experts can't agree on anything.",
            breakdown: [
              { service: 'API Gateway + WebSocket', cost: 50, justification: 'Because Jeff insisted on simplicity' },
              { service: 'Lambda Functions', cost: 120, justification: 'Swami wanted it fast and serverless' },
              { service: 'DynamoDB Global Tables', cost: 350, justification: 'Werner demanded global scale from day one' },
              { service: 'S3 + CloudFront', cost: 75, justification: 'For all those architecture diagrams' },
              { service: 'Bedrock AI Models', cost: 250, justification: 'The agents need to argue somehow' },
              { service: 'CloudWatch Logs', cost: 2.50, justification: 'To debug why they keep disagreeing' }
            ]
          },
          expertEndorsements: {
            jeff: "It's more complex than I wanted, but at least it works.",
            swami: "We shipped it fast, even if Werner made us add unnecessary scaling.",
            werner: "It will scale to millions of users. You're welcome."
          },
          assetsFolder: {
            diagramPngUrl: architectureDiagramUrl || '',
            mermaidSourceUrl: ''
          }
        };
        
        setFinalArchitecture(demoArchitecture);
        
        // Trigger finale after all messages (or skip if disabled)
        setTimeout(() => {
          if (shouldShowFinaleAnimation()) {
            setIsFinaleTriggered(true);
            setTimeout(() => {
              setIsArchitectureRevealed(true);
              setDebateStatus('completed');
            }, 2000);
          } else {
            // Skip finale animation, go straight to architecture
            setIsArchitectureRevealed(true);
            setDebateStatus('completed');
          }
        }, 1000);
        return;
      }
      
      const expertId = expertIds[currentExpertIndex];
      const round = rounds[currentRound];
      const roundNumber = currentRound + 1;
      const audioUrl = getDemoAudioUrl(expertId, roundNumber);
      
      // Simulate expert speaking
      setSpeakingExpertId(expertId);
      
      // Get content for this round and expert
      const demoContent = round.getContent(expertId);
      
      // Simulate streaming message
      setCurrentStreamingMessage({
        expertId,
        partialContent: demoContent
      });
      
      // Complete message after delay
      setTimeout(() => {
        const newMessage: DebateMessage = {
          id: `demo-msg-r${roundNumber}-${expertId}`,
          expertId,
          content: demoContent,
          audioUrl,
          timestamp: Date.now(),
          isDisagreement: currentRound >= 1 // Rounds 2, 3, 4 are disagreements
        };
        
        setMessages(prev => [...prev, newMessage]);
        setCurrentStreamingMessage(null);
        setSpeakingExpertId(null);
        
        // Play audio if available (gracefully ignore missing URLs)
        if (audioUrl) {
          setCurrentAudioUrl(audioUrl);
          setCurrentAudioExpertId(expertId);
        }
        
        // Update frustration level based on round and expert's response
        // Frustration increases as rounds progress
        const baseFrustration = currentRound + 1;
        const frustrationVariation = currentExpertIndex * 0.3; // Slight variation per expert
        const frustrationLevel = Math.min(5, Math.ceil(baseFrustration + frustrationVariation)) as FrustrationLevel;
        
        setFrustrationLevels(prev => ({
          ...prev,
          [expertId]: frustrationLevel
        }));
        
        // Move to next expert
        currentExpertIndex++;
        
        // If all experts have spoken in this round, move to next round
        if (currentExpertIndex >= expertIds.length) {
          currentExpertIndex = 0;
          currentRound++;
        }
        
        // Schedule next message
        // Wait longer if audio is playing, shorter otherwise
        const delay = audioUrl ? 6000 : 3000;
        setTimeout(addDemoMessage, delay);
      }, 2000);
    };
    
    // Start the demo
    addDemoMessage();
  }, []);

  // Handle problem submission
  const handleProblemSubmit = useCallback(async (problem: string) => {
    console.log('[App] Problem submitted:', problem);
    
    setIsLoading(true);
    setDebateStatus('in_progress');
    
    // Reset state for new debate
    setMessages([]);
    setCurrentStreamingMessage(null);
    setSpeakingExpertId(null);
    setFrustrationLevels({
      jeff: 1,
      swami: 1,
      werner: 1,
    });
    setIsFinaleTriggered(false);
    setIsArchitectureRevealed(false);
    setFinalArchitecture(null);
    
    try {
      if (isDemoMode()) {
        // Demo mode: simulate debate with pre-recorded audio
        console.log('[App] Running demo mode debate');
        setIsLoading(false);
        simulateDemoDebate();
      } else {
        // Submit problem via WebSocket
        webSocketClient.submitProblem(problem, sessionId);
        setIsLoading(false);
      }
    } catch (error) {
      console.error('[App] Failed to submit problem:', error);
      setIsLoading(false);
      setDebateStatus('pending');
      // Could show error message to user here
    }
  }, [sessionId, simulateDemoDebate]);

  // Handle audio playback
  const handlePlayAudio = useCallback((audioUrl: string) => {
    setCurrentAudioUrl(audioUrl);
  }, []);

  // Handle audio complete
  const handleAudioComplete = useCallback(() => {
    setCurrentAudioUrl(null);
    setCurrentAudioExpertId('');
  }, []);

  // Handle architecture download
  const handleArchitectureDownload = useCallback((assetType: 'diagram' | 'all') => {
    console.log('[App] Downloading architecture assets:', assetType);
    // The ArchitectureReveal component handles the actual download
  }, []);

  return (
    <div className="app">
      <div className="hero">
        <h1>Disagree and Commit</h1>
        <p className="subtitle">Road to Reinvent Hackathon</p>
        {shouldShowDemoBanner() && (
          <div style={{
            background: 'rgba(255, 165, 0, 0.2)',
            border: '2px solid orange',
            borderRadius: '8px',
            padding: '8px 16px',
            marginTop: '12px',
            fontSize: '14px',
            fontWeight: 'bold',
            color: 'orange'
          }}>
            🎬 DEMO MODE - Using pre-recorded audio
          </div>
        )}
      </div>
      
      <ProblemInput 
        onSubmit={handleProblemSubmit}
        isDebateInProgress={debateStatus === 'in_progress'}
        isLoading={isLoading}
      />
      
      <PanelDisplay 
        experts={EXPERTS}
        speakingExpertId={speakingExpertId}
        frustrationLevels={frustrationLevels}
      />

      {/* Debate Display - show messages during debate */}
      {debateStatus !== 'pending' && (
        <DebateDisplay 
          messages={messages}
          currentStreamingMessage={currentStreamingMessage}
          onPlayAudio={handlePlayAudio}
        />
      )}

      {/* Audio Player - hidden component for audio playback */}
      {currentAudioUrl && (
        <AudioPlayer 
          audioUrl={currentAudioUrl}
          expertId={currentAudioExpertId}
          onComplete={handleAudioComplete}
          autoPlay={true}
        />
      )}

      {/* Finale Overlay */}
      <FinaleOverlay 
        isTriggered={isFinaleTriggered}
        onComplete={handleFinaleComplete}
      />

      {/* Architecture Reveal */}
      {finalArchitecture && (
        <ArchitectureReveal 
          isRevealed={isArchitectureRevealed}
          mermaidDiagram={finalArchitecture.mermaidDiagram}
          costEstimate={finalArchitecture.costEstimate}
          expertEndorsements={finalArchitecture.expertEndorsements}
          assetsFolder={finalArchitecture.assetsFolder}
          onDownload={handleArchitectureDownload}
        />
      )}
    </div>
  );
}

export default App;
