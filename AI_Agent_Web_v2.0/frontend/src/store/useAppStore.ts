import { create } from 'zustand';
import { TabType, SocketStatus, Message, Tool, SystemMetrics, FileNode } from '../types';
import { Session } from '../types/session';
import { apiService } from '../services/api';

interface AppState {
  activeTab: TabType;
  socketStatus: SocketStatus;
  messages: Message[];
  sessions: Session[];
  activeSessionId: string | null;
  tools: Tool[];
  selectedCategory: string;
  selectedTool: Tool | null;
  systemMetrics: SystemMetrics | null;
  workspaceFiles: FileNode[];
  selectedFile: FileNode | null;
  activeModel: string;

  // Auth State & Actions
  user: { username: string } | null;
  token: string | null;
  login: (token: string, username: string) => void;
  logout: () => void;

  setActiveTab: (tab: TabType) => void;
  setSocketStatus: (status: SocketStatus) => void;
  addMessage: (msg: Message) => void;
  updateLastAgentMessage: (token: string) => void;
  addToolCallToLastMessage: (toolCall: any) => void;
  updateToolResultInLastMessage: (callId: string, result: string) => void;
  finishStreaming: () => void;
  setTools: (tools: Tool[]) => void;
  setSelectedCategory: (cat: string) => void;
  setSelectedTool: (tool: Tool | null) => void;
  setSystemMetrics: (metrics: SystemMetrics) => void;
  setWorkspaceFiles: (files: FileNode[]) => void;
  setSelectedFile: (file: FileNode | null) => void;
  setActiveModel: (model: string) => void;
  clearMessages: () => void;

  // Session & Persistence methods
  fetchSessions: () => Promise<void>;
  setActiveSessionId: (id: string) => Promise<void>;
  createNewSession: () => Promise<void>;
  deleteSession: (id: string) => Promise<void>;
  updateSessionTitle: (id: string, newTitle: string) => Promise<void>;
}

const DEFAULT_WELCOME_MSG: Message = {
  id: 'welcome-1',
  sender: 'agent',
  content: '👋 **Merhaba! Ben OpenPlexus — Yusuf PEKER tarafından geliştirilen açık kaynak kodlu AI SysAdmin & DevSecOps Ajanıyım.**\n\n100+ gelişmiş sistem, ağ keşif, zafiyet tarama ve kodlama aracı ile sunucularınızı yönetebilir, güvenlik denetimleri yapabilir ve kod tabanınızı optimize edebilirim.\n\n🔗 **GitHub Proje Deposu:**\nhttps://github.com/YusufPEKERR/AI-AGENT\n\nAşağıdaki hızlı talimatları veya kendi özel isteklerinizi yazarak hemen başlayabilirsiniz! 🚀',
  timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
};

export const useAppStore = create<AppState>((set, get) => ({
  activeTab: 'chat',
  socketStatus: 'disconnected',
  messages: [DEFAULT_WELCOME_MSG],
  sessions: [],
  activeSessionId: localStorage.getItem('activeSessionId') || null,
  tools: [],
  selectedCategory: 'All',
  selectedTool: null,
  systemMetrics: null,
  workspaceFiles: [],
  selectedFile: null,
  activeModel: 'DeepSeek V4 Pro',

  // Auth initialization
  user: localStorage.getItem('username') ? { username: localStorage.getItem('username')! } : null,
  token: localStorage.getItem('token') || null,
  login: (token, username) => {
    localStorage.setItem('token', token);
    localStorage.setItem('username', username);
    set({ token, user: { username } });
  },
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('activeSessionId');
    set({ token: null, user: null, messages: [DEFAULT_WELCOME_MSG], activeSessionId: null, sessions: [] });
  },

  setActiveTab: (tab) => set({ activeTab: tab }),
  setSocketStatus: (status) => set({ socketStatus: status }),

  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),

  updateLastAgentMessage: (token) => set((state) => {
    const msgs = [...state.messages];
    const last = msgs[msgs.length - 1];
    if (last && last.sender === 'agent' && last.isStreaming) {
      last.content += token;
    } else {
      msgs.push({
        id: `msg-${Date.now()}`,
        sender: 'agent',
        content: token,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isStreaming: true,
        toolCalls: []
      });
    }
    return { messages: msgs };
  }),

  addToolCallToLastMessage: (toolCall) => set((state) => {
    const msgs = [...state.messages];
    const last = msgs[msgs.length - 1];
    if (last && last.sender === 'agent') {
      const calls = last.toolCalls || [];
      last.toolCalls = [...calls, { ...toolCall, status: 'running' }];
    }
    return { messages: msgs };
  }),

  updateToolResultInLastMessage: (callId, result) => set((state) => {
    const msgs = [...state.messages];
    const last = msgs[msgs.length - 1];
    if (last && last.toolCalls) {
      last.toolCalls = last.toolCalls.map(tc => tc.id === callId ? { ...tc, result, status: 'completed' } : tc);
    }
    return { messages: msgs };
  }),

  finishStreaming: () => set((state) => {
    const msgs = [...state.messages];
    const last = msgs[msgs.length - 1];
    if (last && last.sender === 'agent') {
      last.isStreaming = false;
    }
    // Refresh session titles after streaming ends
    get().fetchSessions();
    return { messages: msgs };
  }),

  setTools: (tools) => set({ tools }),
  setSelectedCategory: (cat) => set({ selectedCategory: cat }),
  setSelectedTool: (tool) => set({ selectedTool: tool }),
  setSystemMetrics: (metrics) => set({ systemMetrics: metrics }),
  setWorkspaceFiles: (files) => set({ workspaceFiles: files }),
  setSelectedFile: (file) => set({ selectedFile: file }),
  setActiveModel: (model) => set({ activeModel: model }),
  clearMessages: () => set({ messages: [] }),

  fetchSessions: async () => {
    try {
      const storedId = localStorage.getItem('activeSessionId');
      if (storedId) {
        // Pre-fetch messages for the stored active session immediately
        get().setActiveSessionId(storedId);
      }

      const sessions = await apiService.getSessions();
      set({ sessions });

      let currentId = get().activeSessionId || localStorage.getItem('activeSessionId');
      if (sessions.length > 0) {
        if (!currentId || !sessions.find(s => s.id === currentId)) {
          currentId = sessions[0].id;
        }
        await get().setActiveSessionId(currentId);
      } else {
        await get().createNewSession();
      }
    } catch (err) {
      console.error('Error fetching sessions:', err);
    }
  },

  setActiveSessionId: async (id: string) => {
    localStorage.setItem('activeSessionId', id);
    set({ activeSessionId: id });
    try {
      const msgs = await apiService.getSessionMessages(id);
      if (msgs.length === 0) {
        set({ messages: [DEFAULT_WELCOME_MSG] });
      } else {
        set({ messages: msgs });
      }
    } catch (err) {
      console.error('Error loading session messages:', err);
    }
  },

  createNewSession: async () => {
    try {
      const newSess = await apiService.createSession('Yeni Sohbet');
      const sessions = [newSess, ...get().sessions];
      set({ sessions, activeSessionId: newSess.id, messages: [DEFAULT_WELCOME_MSG] });
      localStorage.setItem('activeSessionId', newSess.id);
    } catch (err) {
      console.error('Error creating new session:', err);
    }
  },

  deleteSession: async (id: string) => {
    try {
      await apiService.deleteSession(id);
      const remaining = get().sessions.filter(s => s.id !== id);
      set({ sessions: remaining });
      if (get().activeSessionId === id) {
        if (remaining.length > 0) {
          await get().setActiveSessionId(remaining[0].id);
        } else {
          await get().createNewSession();
        }
      }
    } catch (err) {
      console.error('Error deleting session:', err);
    }
  },

  updateSessionTitle: async (id: string, newTitle: string) => {
    try {
      const updated = await apiService.updateSessionTitle(id, newTitle);
      set((state) => ({
        sessions: state.sessions.map((s) => (s.id === id ? { ...s, title: updated.title } : s))
      }));
    } catch (err) {
      console.error('Error updating session title:', err);
    }
  }
}));
