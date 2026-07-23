import React, { useRef, useEffect } from 'react';
import { Bot, User, Wrench, CheckCircle2, Loader2, Sparkles, Terminal } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { ChatInput } from './ChatInput';

export const ChatInterface: React.FC = () => {
  const { messages } = useAppStore();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] bg-slate-950/40 relative">
      {/* Scrollable Messages Stream */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-4 max-w-4xl ${msg.sender === 'user' ? 'ml-auto flex-row-reverse' : ''
              }`}
          >
            {/* Avatar */}
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${msg.sender === 'user'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-500/20'
                : 'bg-cyan-950 text-cyan-400 border border-cyan-800/50 shadow-md shadow-cyan-500/10'
              }`}>
              {msg.sender === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>

            {/* Content Container */}
            <div className={`space-y-3 max-w-2xl ${msg.sender === 'user' ? 'items-end' : 'items-start'
              }`}>
              {/* Header Meta */}
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <span className="font-semibold text-slate-200">
                  {msg.sender === 'user' ? 'Siz' : 'OpenPlexus AI Agent'}
                </span>
                <span>•</span>
                <span>{msg.timestamp}</span>
              </div>

              {/* Message Bubble */}
              <div className={`p-4 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${msg.sender === 'user'
                  ? 'bg-purple-600/90 text-slate-50 rounded-tr-none shadow-lg'
                  : 'glass-panel text-slate-200 rounded-tl-none border-slate-800/80 shadow-lg'
                }`}>
                {msg.content}
                {msg.isStreaming && (
                  <span className="inline-block w-2 h-4 bg-cyan-400 ml-1 animate-pulse" />
                )}
              </div>

              {/* Tool Calls Execution Badges & Cards */}
              {msg.toolCalls && msg.toolCalls.length > 0 && (
                <div className="space-y-2 pt-1 w-full">
                  {msg.toolCalls.map((call) => (
                    <div
                      key={call.id}
                      className="p-3 rounded-xl bg-slate-900/90 border border-cyan-500/30 text-xs font-mono space-y-2 shadow-md"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 text-cyan-400 font-semibold">
                          <Wrench className="w-3.5 h-3.5" />
                          <span>Tool Invocation: {call.name}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-slate-400">
                          {call.status === 'running' ? (
                            <span className="flex items-center gap-1 text-amber-400">
                              <Loader2 className="w-3 h-3 animate-spin" /> Executing...
                            </span>
                          ) : (
                            <span className="flex items-center gap-1 text-emerald-400 font-semibold">
                              <CheckCircle2 className="w-3.5 h-3.5" /> Completed
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Tool Parameters */}
                      {call.arguments && Object.keys(call.arguments).length > 0 && (
                        <div className="p-2 rounded bg-slate-950/80 text-slate-300 border border-slate-800">
                          <span className="text-slate-500 block mb-1">Parameters:</span>
                          <pre className="text-[11px] text-cyan-300">{JSON.stringify(call.arguments, null, 2)}</pre>
                        </div>
                      )}

                      {/* Tool Output Result */}
                      {call.result && (
                        <div className="p-2.5 rounded bg-slate-950 text-emerald-300 border border-emerald-950 space-y-1">
                          <span className="text-emerald-500 text-[10px] uppercase font-bold tracking-wider block">Output Result:</span>
                          <p className="text-xs whitespace-pre-wrap">{call.result}</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Fixed Bottom Input Drawer */}
      <ChatInput />
    </div>
  );
};
