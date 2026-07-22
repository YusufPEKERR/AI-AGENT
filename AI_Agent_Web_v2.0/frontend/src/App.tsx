import React from 'react';
import { io } from 'socket.io-client';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { MessageBubble } from './components/chat/MessageBubble';
import { ChatInput } from './components/chat/ChatInput';
import { ArtifactPanel } from './components/artifacts/ArtifactPanel';
import { useChatStore } from './stores/chatStore';

const socket = io('http://localhost:8000', {
  path: '/ws/socket.io',
  autoConnect: true,
});

export const App: React.FC = () => {
  const { messages, addMessage, appendToLastMessage, isStreaming, setIsStreaming } = useChatStore();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    socket.on('chat:token', (token: str) => {
      appendToLastMessage(token);
    });

    socket.on('chat:tool_call', (tc: any) => {
      addMessage({
        id: String(Date.now()),
        role: 'tool_call',
        toolCall: tc,
      });
    });

    socket.on('chat:tool_result', (tr: any) => {
      addMessage({
        id: String(Date.now()),
        role: 'tool_result',
        toolResult: tr.result,
      });
    });

    socket.on('chat:done', () => {
      setIsStreaming(false);
    });

    return () => {
      socket.off('chat:token');
      socket.off('chat:tool_call');
      socket.off('chat:tool_result');
      socket.off('chat:done');
    };
  }, []);

  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (text: string) => {
    const userMsg = { id: String(Date.now()), role: 'user' as const, content: text };
    addMessage(userMsg);
    setIsStreaming(true);

    socket.emit('chat:message', {
      sessionId: 'default',
      content: text,
    });
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-background overflow-hidden">
      <Header />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <main className="flex-1 flex flex-col bg-background/50 overflow-hidden">
          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 text-muted">
                <div className="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-3">
                  🚀
                </div>
                <h2 className="text-lg font-semibold text-foreground mb-1">AI Agent Web Arayüzüne Hoş Geldiniz</h2>
                <p className="text-sm max-w-md">
                  31 adet tam yetkili araç (Git, Docker, Shell, WinRM, Registry, WMI, SQLite) hizmetinizdedir. Başlamak için aşağıdan bir komut yazın.
                </p>
              </div>
            ) : (
              messages.map((msg) => <MessageBubble key={msg.id} message={msg} />)
            )}
            <div ref={messagesEndRef} />
          </div>

          <ChatInput onSend={handleSendMessage} disabled={isStreaming} />
        </main>

        <ArtifactPanel />
      </div>
    </div>
  );
};

export default App;
