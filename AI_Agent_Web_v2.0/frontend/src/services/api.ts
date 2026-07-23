import { Session } from '../types/session';
import { Message } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const apiService = {
  async getSessions(): Promise<Session[]> {
    const res = await fetch(`${API_BASE_URL}/sessions`);
    if (!res.ok) throw new Error('Failed to fetch sessions');
    return res.json();
  },

  async createSession(title: string = 'Yeni Sohbet'): Promise<Session> {
    const res = await fetch(`${API_BASE_URL}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error('Failed to create session');
    return res.json();
  },

  async deleteSession(sessionId: string): Promise<void> {
    const res = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete session');
  },

  async updateSessionTitle(sessionId: string, title: string): Promise<Session> {
    const res = await fetch(`${API_BASE_URL}/sessions/${sessionId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title }),
    });
    if (!res.ok) throw new Error('Failed to update session title');
    return res.json();
  },

  async getSessionMessages(sessionId: string): Promise<Message[]> {
    const res = await fetch(`${API_BASE_URL}/sessions/${sessionId}/messages`);
    if (!res.ok) throw new Error('Failed to fetch session messages');
    const rawMessages = await res.json();

    // Map backend database MessageModel array into Frontend Message UI state
    const formattedMessages: Message[] = [];
    
    for (const raw of rawMessages) {
      if (raw.role === 'user') {
        formattedMessages.push({
          id: raw.id,
          sender: 'user',
          content: raw.content || '',
          timestamp: new Date(raw.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });
      } else if (raw.role === 'assistant') {
        formattedMessages.push({
          id: raw.id,
          sender: 'agent',
          content: raw.content || '',
          timestamp: new Date(raw.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          toolCalls: []
        });
      } else if (raw.role === 'tool_call') {
        const last = formattedMessages[formattedMessages.length - 1];
        let parsedArgs = {};
        try {
          if (raw.tool_args) parsedArgs = JSON.parse(raw.tool_args);
        } catch (e) {
          parsedArgs = {};
        }

        const toolCallObj = {
          id: raw.id,
          name: raw.tool_name || 'Tool',
          arguments: parsedArgs,
          result: raw.tool_result || '',
          status: 'completed' as const
        };

        if (last && last.sender === 'agent') {
          last.toolCalls = [...(last.toolCalls || []), toolCallObj];
        } else {
          formattedMessages.push({
            id: raw.id,
            sender: 'agent',
            content: '',
            timestamp: new Date(raw.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            toolCalls: [toolCallObj]
          });
        }
      }
    }

    return formattedMessages;
  }
};
