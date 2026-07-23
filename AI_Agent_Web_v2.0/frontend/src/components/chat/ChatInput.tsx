import React, { useState, useRef, useEffect } from 'react';
import { Send, Terminal, ShieldAlert, Cpu, Sparkles, Mic, MicOff } from 'lucide-react';
import { socketService } from '../../services/socketService';
import { useAppStore } from '../../store/useAppStore';

export const ChatInput: React.FC = () => {
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const { socketStatus } = useAppStore();
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'tr-TR';

      recognition.onstart = () => setIsRecording(true);
      recognition.onend = () => setIsRecording(false);
      recognition.onerror = () => setIsRecording(false);

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setInput((prev) => (prev ? prev + ' ' + transcript : transcript));
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const toggleRecording = () => {
    if (!recognitionRef.current) {
      alert('Tarayıcınız sesli komut özelliğini desteklemiyor.');
      return;
    }
    if (isRecording) {
      recognitionRef.current.stop();
    } else {
      recognitionRef.current.start();
    }
  };

  const handleSend = () => {
    if (!input.trim()) return;
    socketService.sendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickPrompts = [
    { label: 'Sistem Sağlığını Kontrol Et', icon: <Cpu className="w-3.5 h-3.5 text-cyan-400" />, prompt: 'Doctor teşhis modülünü çalıştırıp sistem kaynak durumunu raporla.' },
    { label: 'Proje Dizinini Listele', icon: <Terminal className="w-3.5 h-3.5 text-purple-400" />, prompt: 'Proje ana dizinindeki tüm dosya ve klasörleri listele.' },
    { label: 'Güvenlik Taraması Başlat', icon: <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />, prompt: 'Kod tabanında güvenlik zafiyeti ve açık port taraması yap.' },
  ];

  return (
    <div className="p-4 border-t border-slate-800/80 glass-panel space-y-3">
      {/* Quick Action Pills */}
      <div className="flex flex-wrap gap-2">
        {quickPrompts.map((item, index) => (
          <button
            key={index}
            onClick={() => {
              setInput(item.prompt);
            }}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-slate-800 border border-slate-800/80 text-xs text-slate-300 transition-all hover:border-cyan-500/40"
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </div>

      {/* Main Input Field */}
      <div className="relative flex items-center">
        <textarea
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={isRecording ? "Dinleniyor..." : "Ajana talimat verin (örn: 'Sistem loglarını incele ve güvenlik durumunu bildir')..."}
          className={`w-full bg-slate-950/80 border ${isRecording ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'border-slate-800'} rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 resize-none pr-28 transition-all`}
        />

        <div className="absolute right-3 flex items-center gap-2">
          <button
            onClick={toggleRecording}
            className={`p-2.5 rounded-lg transition-all ${isRecording
                ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30 animate-pulse'
                : 'bg-slate-800/80 text-slate-400 hover:text-cyan-400 hover:bg-slate-800'
              }`}
            title="Sesle Yaz"
          >
            {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>
          <button
            onClick={handleSend}
            disabled={!input.trim() || socketStatus !== 'connected'}
            className={`p-2.5 rounded-lg bg-gradient-to-r from-cyan-500 to-purple-600 text-white shadow-md shadow-cyan-500/20 transition-all ${!input.trim() || socketStatus !== 'connected'
                ? 'opacity-40 cursor-not-allowed'
                : 'hover:opacity-95 hover:scale-105 active:scale-95'
              }`}
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between text-[11px] text-slate-500 px-1">
        <span>Enter ile gönder • Shift+Enter ile alt satıra geç</span>
        <span className="flex items-center gap-1 text-cyan-400 font-medium">
          <Sparkles className="w-3 h-3" /> DeepSeek V4 Pro Engine
        </span>
      </div>
    </div>
  );
};
