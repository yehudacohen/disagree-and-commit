/**
 * WebSocketClient - Manages real-time communication with API Gateway WebSocket
 * 
 * Usage Example:
 * ```typescript
 * import { webSocketClient } from './services/WebSocketClient';
 * 
 * // Connect to WebSocket
 * await webSocketClient.connect(sessionId);
 * 
 * // Listen for specific message types
 * webSocketClient.onMessageType('expert_speaking', (msg) => {
 *   console.log(`${msg.expertId} is speaking`);
 * });
 * 
 * webSocketClient.onMessageType('frustration_update', (msg) => {
 *   console.log(`${msg.expertId} frustration: ${msg.level}`);
 * });
 * 
 * // Submit a problem
 * webSocketClient.submitProblem('Build a todo app', sessionId);
 * 
 * // Disconnect when done
 * webSocketClient.disconnect();
 * ```
 */

import type { WebSocketMessage, ClientMessage } from '../types';

type MessageHandler = (message: WebSocketMessage) => void;
type TypedMessageHandler<T extends WebSocketMessage['type']> = (
  message: Extract<WebSocketMessage, { type: T }>
) => void;

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private messageHandlers: MessageHandler[] = [];
  private typedHandlers: Map<WebSocketMessage['type'], MessageHandler[]> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 3;
  private reconnectDelay = 1000;
  private isIntentionalClose = false;

  /**
   * Connect to the API Gateway WebSocket endpoint
   * @param sessionId - Unique session identifier
   */
  async connect(sessionId: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        // Get WebSocket URL from environment variable or use default
        const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:3001';
        
        this.ws = new WebSocket(wsUrl);
        this.isIntentionalClose = false;

        this.ws.onopen = () => {
          console.log('[WebSocketClient] Connected to WebSocket');
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onerror = (error) => {
          console.error('[WebSocketClient] WebSocket error:', error);
          reject(new Error('WebSocket connection failed'));
        };

        this.ws.onclose = (event) => {
          console.log('[WebSocketClient] WebSocket closed:', event.code, event.reason);
          
          // Attempt reconnection if not intentional close
          if (!this.isIntentionalClose && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`[WebSocketClient] Reconnecting... Attempt ${this.reconnectAttempts}`);
            setTimeout(() => {
              this.connect(sessionId).catch(console.error);
            }, this.reconnectDelay * this.reconnectAttempts);
          }
        };

        this.ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data) as WebSocketMessage;
            console.log('[WebSocketClient] Received message:', message);
            
            // Route to type-specific handlers first
            const typeHandlers = this.typedHandlers.get(message.type);
            if (typeHandlers) {
              typeHandlers.forEach(handler => handler(message));
            }
            
            // Then notify all general handlers
            this.messageHandlers.forEach(handler => handler(message));
          } catch (error) {
            console.error('[WebSocketClient] Failed to parse message:', error);
          }
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the WebSocket
   */
  disconnect(): void {
    if (this.ws) {
      this.isIntentionalClose = true;
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
      this.messageHandlers = [];
      this.typedHandlers.clear();
      console.log('[WebSocketClient] Disconnected');
    }
  }

  /**
   * Check if WebSocket is currently connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }

  /**
   * Send a message to the backend with action routing
   * @param action - The action type for route selection
   * @param payload - The message payload
   */
  sendMessage(action: string, payload: Record<string, unknown>): void {
    if (!this.isConnected()) {
      console.error('[WebSocketClient] Cannot send message: not connected');
      throw new Error('WebSocket is not connected');
    }

    const message = {
      action,
      ...payload
    };

    this.ws!.send(JSON.stringify(message));
    console.log('[WebSocketClient] Sent message:', message);
  }

  /**
   * Register a handler for incoming messages
   * @param handler - Function to handle incoming messages
   */
  onMessage(handler: MessageHandler): void {
    this.messageHandlers.push(handler);
  }

  /**
   * Remove a message handler
   * @param handler - The handler to remove
   */
  offMessage(handler: MessageHandler): void {
    this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
  }

  /**
   * Submit a problem to the panel for debate
   * @param problem - The engineering problem to debate
   * @param sessionId - The session identifier
   */
  submitProblem(problem: string, sessionId: string): void {
    const payload: ClientMessage = {
      action: 'submitProblem',
      problem,
      sessionId
    };

    // Send with action field for API Gateway route selection
    this.sendMessage(payload.action, { problem, sessionId });
  }

  /**
   * Register a handler for a specific message type
   * @param type - The message type to listen for
   * @param handler - Function to handle messages of this type
   */
  onMessageType<T extends WebSocketMessage['type']>(
    type: T,
    handler: TypedMessageHandler<T>
  ): void {
    const handlers = this.typedHandlers.get(type) || [];
    handlers.push(handler as MessageHandler);
    this.typedHandlers.set(type, handlers);
  }

  /**
   * Remove a handler for a specific message type
   * @param type - The message type
   * @param handler - The handler to remove
   */
  offMessageType<T extends WebSocketMessage['type']>(
    type: T,
    handler: TypedMessageHandler<T>
  ): void {
    const handlers = this.typedHandlers.get(type);
    if (handlers) {
      const filtered = handlers.filter(h => h !== handler);
      if (filtered.length > 0) {
        this.typedHandlers.set(type, filtered);
      } else {
        this.typedHandlers.delete(type);
      }
    }
  }
}

// Export a singleton instance
export const webSocketClient = new WebSocketClient();
