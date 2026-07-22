import { create } from 'zustand';
import { Message } from '../types/chat';

interface ChatStore {
  activeSessionId: string | null;
  messages: Message[];
  isStreaming: boolean;
  setActiveSessionId: (id: string | null) => void;
  setMessages: (messages: Message[]) => void;
  addMessage: (message: Message) => void;
  appendToLastMessage: (content: string) => void;
  setIsStreaming: (streaming: boolean) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  activeSessionId: null,
  messages: [],
  isStreaming: false,
  setActiveSessionId: (id) => set({ activeSessionId: id }),
  setMessages: (messages) => set({ messages }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  appendToLastMessage: (content) => set((state) => {
    const last = state.messages[state.messages.length - 1];
    if (last && last.role === 'assistant') {
      return {
        messages: [
          ...state.messages.slice(0, -1),
          { ...last, content: (last.content || '') + content }
        ]
      };
    }
    return {
      messages: [
        ...state.messages,
        { id: String(Date.now()), role: 'assistant', content }
      ]
    };
  }),
  setIsStreaming: (streaming) => set({ isStreaming: streaming }),
}));
