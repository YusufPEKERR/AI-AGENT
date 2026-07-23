import React, { useEffect, useState } from 'react';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { ChatInterface } from './components/chat/ChatInterface';
import { ToolCatalog } from './components/tools/ToolCatalog';
import { SystemMonitor } from './components/monitor/SystemMonitor';
import { WorkspaceExplorer } from './components/workspace/WorkspaceExplorer';
import { WidgetsDashboard } from './components/widgets/WidgetsDashboard';
import { useAppStore } from './store/useAppStore';
import { useAuthStore } from './store/useAuthStore';
import { socketService } from './services/socketService';
import { LoginPage } from './components/auth/LoginPage';
import { RegisterPage } from './components/auth/RegisterPage';

export const App: React.FC = () => {
  const { activeTab, fetchSessions } = useAppStore();
  const { isAuthenticated } = useAuthStore();
  const [authPage, setAuthPage] = useState<'login' | 'register'>('login');

  // useEffect her zaman çağrılmalı — React hooks kuralı
  useEffect(() => {
    if (!isAuthenticated) return;

    socketService.connect();
    fetchSessions();

    return () => {
      socketService.disconnect();
    };
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    if (authPage === 'register') {
      return (
        <RegisterPage
          onSwitchToLogin={() => setAuthPage('login')}
        />
      );
    }
    return (
      <LoginPage
        onSwitchToRegister={() => setAuthPage('register')}
      />
    );
  }

  return (
    <div className="h-screen w-screen overflow-hidden bg-[#090d16] text-slate-100 flex flex-col antialiased selection:bg-cyan-500/30 selection:text-cyan-200">
      <Header />

      <div className="flex flex-1 overflow-hidden h-[calc(100vh-4rem)]">
        <Sidebar />

        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950/20">
          {activeTab === 'chat' && <ChatInterface />}
          {activeTab === 'tools' && <ToolCatalog />}
          {activeTab === 'monitor' && <SystemMonitor />}
          {activeTab === 'workspace' && <WorkspaceExplorer />}
          {activeTab === 'widgets' && <WidgetsDashboard />}
        </main>
      </div>
    </div>
  );
};

export default App;

