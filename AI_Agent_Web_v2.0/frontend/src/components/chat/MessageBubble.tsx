import React from 'react';
import { User, Bot } from 'lucide-react';
import { Message } from '../../types/chat';
import { ToolCallCard } from './ToolCallCard';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  if (message.role === 'tool_call') {
    return (
      <ToolCallCard 
        name={message.toolCall?.name || 'tool'}
        args={message.toolCall?.arguments || {}}
        result={message.toolResult}
        isExecuting={!message.toolResult}
      />
    );
  }

  return (
    <div className={`flex gap-3 my-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`flex items-center justify-center w-8 h-8 rounded-full shrink-0 ${
        isUser ? 'bg-blue-600 text-white' : 'bg-slate-800 text-cyan-400'
      }`}>
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm shadow-sm ${
        isUser 
          ? 'bg-blue-600 text-white rounded-tr-none' 
          : 'bg-card text-card-foreground border border-border rounded-tl-none whitespace-pre-wrap'
      }`}>
        {message.content}
      </div>
    </div>
  );
};
