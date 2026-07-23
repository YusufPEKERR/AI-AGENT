import { io, Socket } from 'socket.io-client';
import { useAppStore } from '../store/useAppStore';
import { BACKEND_URL } from './api';

class SocketService {
  private socket: Socket | null = null;

  connect() {
    if (this.socket && this.socket.connected) return;

    useAppStore.getState().setSocketStatus('connecting');

    this.socket = io(BACKEND_URL, {
      path: '/ws/socket.io',
      transports: ['websocket', 'polling'],
      reconnectionAttempts: 10,
      reconnectionDelay: 1000
    });

    this.socket.on('connect', () => {
      console.log('Connected to backend WebSocket:', this.socket?.id);
      useAppStore.getState().setSocketStatus('connected');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from backend WebSocket');
      useAppStore.getState().setSocketStatus('disconnected');
    });

    this.socket.on('chat:token', (token: string) => {
      useAppStore.getState().updateLastAgentMessage(token);
    });

    this.socket.on('chat:tool_call', (toolCall: any) => {
      useAppStore.getState().addToolCallToLastMessage(toolCall);
    });

    this.socket.on('chat:tool_result', (data: { callId: string; result: string }) => {
      useAppStore.getState().updateToolResultInLastMessage(data.callId, data.result);
    });

    this.socket.on('chat:done', () => {
      useAppStore.getState().finishStreaming();
    });
  }

  sendMessage(content: string) {
    if (!this.socket || !this.socket.connected) {
      this.connect();
    }

    // Add user message to store
    useAppStore.getState().addMessage({
      id: `usr-${Date.now()}`,
      sender: 'user',
      content,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });

    const workspace = localStorage.getItem('workspacePath') || '.';
    const activeSessionId = useAppStore.getState().activeSessionId || 'default';

    this.socket?.emit('chat:message', {
      content,
      sessionId: activeSessionId,
      workspace
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
}

export const socketService = new SocketService();
