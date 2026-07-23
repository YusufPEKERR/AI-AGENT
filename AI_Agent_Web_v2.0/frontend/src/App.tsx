import React, { useEffect } from 'react';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { ChatInterface } from './components/chat/ChatInterface';
import { ToolCatalog } from './components/tools/ToolCatalog';
import { SystemMonitor } from './components/monitor/SystemMonitor';
import { WorkspaceExplorer } from './components/workspace/WorkspaceExplorer';
import { WidgetsDashboard } from './components/widgets/WidgetsDashboard';
import { useAppStore } from './store/useAppStore';
import { socketService } from './services/socketService';
import { Login } from './components/auth/Login';

export const App: React.FC = () => {
  const { activeTab, fetchSessions, token } = useAppStore();

  useEffect(() => {
    if (token) {
      // Automatically connect Socket.IO on app mount only if authenticated
      socketService.connect();
      fetchSessions();
    }

    return () => {
      socketService.disconnect();
    };
  }, [token]);

  if (!token) {
    return <Login />;
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
