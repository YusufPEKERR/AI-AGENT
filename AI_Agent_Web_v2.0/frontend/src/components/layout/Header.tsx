import React from 'react';
import { Bot, Cpu, ShieldCheck, Zap, Server } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';

export const Header: React.FC = () => {
  const { socketStatus, activeModel, setActiveModel, user, logout } = useAppStore();

  return (
    <header className="h-16 shrink-0 border-b border-slate-800/80 glass-panel px-6 flex items-center justify-between z-20 sticky top-0">
      {/* Brand & Model Title */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-purple-600 p-0.5 flex items-center justify-center shadow-lg shadow-cyan-500/20">
          <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
            <Bot className="w-5 h-5 text-cyan-400 animate-pulse-glow" />
          </div>
        </div>

        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-slate-100 text-lg tracking-tight">OpenPlexus</h1>
            <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/50">
              v2.0 Pro
            </span>
          </div>
          <p className="text-xs text-slate-400 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            31 Active Tools • Real-time Socket Engine
          </p>
        </div>
      </div>

      {/* Model Selector & Status Badges */}
      <div className="flex items-center gap-4">
        {/* Model Switcher */}
        <div className="flex items-center gap-2 bg-slate-900/80 border border-slate-800 rounded-lg p-1">
          <Zap className="w-4 h-4 text-purple-400 ml-2" />
          <select
            value={activeModel}
            onChange={(e) => setActiveModel(e.target.value)}
            className="bg-transparent text-xs text-slate-200 font-medium focus:outline-none cursor-pointer pr-2"
          >
            <option value="DeepSeek V4 Pro" className="bg-slate-900 text-slate-100">DeepSeek V4 Pro</option>
            <option value="Antigravity Agent" className="bg-slate-900 text-slate-100">Antigravity Agent</option>
          </select>
        </div>

        {/* System Health Badge */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/60 border border-slate-800 text-xs text-slate-300">
          <Server className="w-3.5 h-3.5 text-cyan-400" />
          <span>Local Engine</span>
        </div>

        {/* WebSocket Connection Status Badge */}
        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-medium transition-all ${
          socketStatus === 'connected'
            ? 'bg-emerald-950/50 border-emerald-500/30 text-emerald-400'
            : socketStatus === 'connecting'
            ? 'bg-amber-950/50 border-amber-500/30 text-amber-400'
            : 'bg-rose-950/50 border-rose-500/30 text-rose-400'
        }`}>
          <span className={`w-2 h-2 rounded-full ${
            socketStatus === 'connected'
              ? 'bg-emerald-400 animate-ping'
              : socketStatus === 'connecting'
              ? 'bg-amber-400 animate-pulse'
              : 'bg-rose-400'
          }`} />
          <span className="capitalize">{socketStatus}</span>
        </div>

        {/* User Info & Logout Button */}
        {user && (
          <div className="flex items-center gap-3 pl-3 border-l border-slate-800">
            <div className="flex flex-col items-end hidden sm:flex">
              <span className="text-xs font-semibold text-slate-200">{user.username}</span>
              <span className="text-[9px] text-slate-500">Oturum Açık</span>
            </div>
            <button
              onClick={logout}
              className="px-2.5 py-1 text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800/80 rounded-lg border border-slate-800/85 transition-all"
            >
              Çıkış
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
