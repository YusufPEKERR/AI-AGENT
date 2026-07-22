import React, { useState } from 'react';
import { Send, Paperclip } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, disabled }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;
    onSend(input.trim());
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="p-3 bg-card border-t border-border flex items-center gap-2">
      <button 
        type="button" 
        className="p-2 rounded-lg text-muted hover:text-foreground hover:bg-secondary transition-colors"
        title="Dosya Ekle"
      >
        <Paperclip className="w-5 h-5" />
      </button>

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="AI Ajanına bir komut verin (örn: 'git status', 'process list', 'read file')..."
        disabled={disabled}
        className="flex-1 bg-secondary/50 text-foreground placeholder:text-muted rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary border border-border/50"
      />

      <button
        type="submit"
        disabled={!input.trim() || disabled}
        className="p-2.5 rounded-xl bg-primary text-primary-foreground disabled:opacity-50 hover:opacity-90 transition-opacity"
      >
        <Send className="w-4 h-4" />
      </button>
    </form>
  );
};
