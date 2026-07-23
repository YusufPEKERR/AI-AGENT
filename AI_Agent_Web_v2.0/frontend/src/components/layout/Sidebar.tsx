import React, { useState } from 'react';
import { MessageSquare, Wrench, Activity, FolderTree, Plus, Trash2, MessageCircle, CloudSun, Pencil, Check, X } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { TabType } from '../../types';

export const Sidebar: React.FC = () => {
  const { 
    activeTab, 
    setActiveTab, 
    sessions, 
    activeSessionId, 
    setActiveSessionId, 
    createNewSession, 
    deleteSession,
    updateSessionTitle
  } = useAppStore();

  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editTitleText, setEditTitleText] = useState('');

  const navItems: { id: TabType; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'chat', label: 'AI Agent Chat', icon: <MessageSquare className="w-5 h-5" /> },
    { id: 'tools', label: 'Tool Catalog', icon: <Wrench className="w-5 h-5" />, badge: '100+' },
    { id: 'monitor', label: 'System Monitor', icon: <Activity className="w-5 h-5" /> },
    { id: 'workspace', label: 'Workspace Explorer', icon: <FolderTree className="w-5 h-5" /> },
    { id: 'widgets', label: 'Hava & Widgets', icon: <CloudSun className="w-5 h-5" />, badge: 'Yeni' },
  ];

  const handleStartEdit = (e: React.MouseEvent, id: string, currentTitle: string) => {
    e.stopPropagation();
    setEditingSessionId(id);
    setEditTitleText(currentTitle);
  };

  const handleSaveEdit = async (e: React.SyntheticEvent, id: string) => {
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }
    const trimmed = editTitleText.trim();
    if (trimmed) {
      await updateSessionTitle(id, trimmed);
    }
    setEditingSessionId(null);
  };

  const handleCancelEdit = (e: React.SyntheticEvent) => {
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }
    setEditingSessionId(null);
  };

  return (
    <aside className="w-64 h-full shrink-0 border-r border-slate-800/80 glass-panel flex flex-col justify-between p-4 z-10 select-none overflow-hidden">
      <div className="space-y-5 flex-1 flex flex-col min-h-0">
        {/* New Chat Button */}
        <button
          onClick={() => {
            createNewSession();
            setActiveTab('chat');
          }}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-medium shadow-lg shadow-cyan-500/20 transition-all duration-200 active:scale-[0.98]"
        >
          <Plus className="w-5 h-5" />
          <span>Yeni Sohbet</span>
        </button>

        {/* Core Navigation */}
        <div>
          <div className="px-2 mb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
            Modüller
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-xl font-medium text-xs transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-cyan-500/15 to-purple-500/15 border border-cyan-500/30 text-cyan-300 shadow-md'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <div className={`${isActive ? 'text-cyan-400' : 'text-slate-400'}`}>
                      {item.icon}
                    </div>
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                      isActive
                        ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40'
                        : 'bg-slate-800 text-slate-400'
                    }`}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Chat History Section */}
        <div className="flex-1 flex flex-col min-h-0 pt-2 border-t border-slate-800/60">
          <div className="px-2 mb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500 flex items-center justify-between">
            <span>Sohbetlerim</span>
            <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400 font-mono">
              {sessions.length}
            </span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-1 pr-1 custom-scrollbar">
            {sessions.length === 0 ? (
              <div className="text-xs text-slate-500 italic px-2 py-3 text-center">
                Henüz kayıtlı sohbet bulunmuyor.
              </div>
            ) : (
              sessions.map((sess) => {
                const isSelected = activeSessionId === sess.id;
                const isEditing = editingSessionId === sess.id;

                return (
                  <div
                    key={sess.id}
                    onClick={() => {
                      if (!isEditing) {
                        setActiveSessionId(sess.id);
                        setActiveTab('chat');
                      }
                    }}
                    className={`group relative flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer text-xs transition-all duration-150 ${
                      isSelected
                        ? 'bg-slate-800/90 text-cyan-300 border border-cyan-500/30 font-medium'
                        : 'text-slate-400 hover:bg-slate-800/40 hover:text-slate-200 border border-transparent'
                    }`}
                  >
                    <div className="flex items-center gap-2 overflow-hidden flex-1 mr-2">
                      <MessageCircle className={`w-3.5 h-3.5 shrink-0 ${isSelected ? 'text-cyan-400' : 'text-slate-500'}`} />

                      {isEditing ? (
                        <form
                          onSubmit={(e) => handleSaveEdit(e, sess.id)}
                          onClick={(e) => e.stopPropagation()}
                          className="flex items-center gap-1 w-full"
                        >
                          <input
                            type="text"
                            value={editTitleText}
                            onChange={(e) => setEditTitleText(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Escape') setEditingSessionId(null);
                            }}
                            autoFocus
                            className="w-full bg-slate-950 border border-cyan-500/50 rounded px-1.5 py-0.5 text-xs text-slate-100 focus:outline-none"
                          />
                          <button
                            type="submit"
                            onMouseDown={(e) => e.preventDefault()}
                            className="p-1 text-emerald-400 hover:bg-emerald-500/20 rounded"
                            title="Kaydet"
                          >
                            <Check className="w-3.5 h-3.5" />
                          </button>
                          <button
                            type="button"
                            onMouseDown={(e) => e.preventDefault()}
                            onClick={handleCancelEdit}
                            className="p-1 text-slate-400 hover:bg-slate-700/50 rounded"
                            title="İptal"
                          >
                            <X className="w-3.5 h-3.5" />
                          </button>
                        </form>
                      ) : (
                        <span className="truncate">{sess.title || 'Yeni Sohbet'}</span>
                      )}
                    </div>

                    {!isEditing && (
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all shrink-0">
                        <button
                          onClick={(e) => handleStartEdit(e, sess.id, sess.title || 'Yeni Sohbet')}
                          className="p-1 hover:bg-cyan-500/20 hover:text-cyan-400 rounded text-slate-500 transition-all"
                          title="Sohbet Adını Değiştir"
                        >
                          <Pencil className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteSession(sess.id);
                          }}
                          className="p-1 hover:bg-red-500/20 hover:text-red-400 rounded text-slate-500 transition-all"
                          title="Sohbeti Sil"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* Footer Info Box */}
      <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80 text-xs space-y-2 mt-4">
        <div className="flex items-center justify-between text-slate-400">
          <span>Engine Status</span>
          <span className="text-emerald-400 font-semibold">Active</span>
        </div>
        <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
          <div className="bg-gradient-to-r from-cyan-400 to-purple-500 h-full w-full animate-pulse" />
        </div>
        <p className="text-[11px] text-slate-500">OpenPlexus — SysAdmin & DevSecOps Suite</p>
      </div>
    </aside>
  );
};

export default Sidebar;
