import { create } from 'zustand';

interface UIStore {
  isSidebarOpen: boolean;
  isArtifactPanelOpen: boolean;
  activeArtifact: { type: string; title: string; content: string } | null;
  toggleSidebar: () => void;
  toggleArtifactPanel: () => void;
  setActiveArtifact: (artifact: { type: string; title: string; content: string } | null) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  isSidebarOpen: true,
  isArtifactPanelOpen: false,
  activeArtifact: null,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  toggleArtifactPanel: () => set((state) => ({ isArtifactPanelOpen: !state.isArtifactPanelOpen })),
  setActiveArtifact: (artifact) => set({ activeArtifact: artifact, isArtifactPanelOpen: !!artifact }),
}));
