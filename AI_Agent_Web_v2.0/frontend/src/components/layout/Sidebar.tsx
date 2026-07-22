import React from 'react';
import { Plus, MessageSquare, Settings, HardDrive, Terminal } from 'lucide-react';
import { useUIStore } from '../../stores/uiStore';
import { useChatStore } from '../../stores/chatStore';

export const Sidebar: React.FC = () => {
  const { isSidebarOpen } = useUIStore();
  const { setMessages } = useChatStore();

  if (!isSidebarOpen) return null;

  const handleNewChat = () => {
    setMessages([]);
  };

  return (
    <aside className="w-64 border-r border-border bg-card flex flex-col shrink-0">
      <div className="p-3">
        <button 
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-xl bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity shadow-sm"
        >
          <Plus className="w-4 h-4" /> Yeni Sohbet
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        <div className="px-3 py-1.5 text-[11px] font-semibold uppercase text-muted tracking-wider">
          Aktif Oturumlar
        </div>

        <button className="w-full flex items-center gap-2 px-3 py-2 text-sm rounded-lg bg-secondary text-foreground font-medium">
          <MessageSquare className="w-4 h-4 text-blue-500" /> Varsayılan Oturum
        </button>
      </div>

      <div className="p-3 border-t border-border space-y-1">
        <button className="w-full flex items-center gap-2 px-3 py-2 text-xs rounded-lg hover:bg-secondary text-muted hover:text-foreground">
          <HardDrive className="w-4 h-4" /> Dosya Gezgini
        </button>
        <button className="w-full flex items-center gap-2 px-3 py-2 text-xs rounded-lg hover:bg-secondary text-muted hover:text-foreground">
          <Settings className="w-4 h-4" /> Ayarlar & İzinler
        </button>
      </div>
    </aside>
  );
};
