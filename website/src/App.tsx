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
      // Submit problem via WebSocket
      webSocketClient.submitProblem(problem, sessionId);
      setIsLoading(false);
    } catch (error) {
      console.error('[App] Failed to submit problem:', error);
      setIsLoading(false);
      setDebateStatus('pending');
      // Could show error message to user here
    }
  }, [sessionId]);

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
