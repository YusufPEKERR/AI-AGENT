import React from 'react';
import { Menu, Sun, Moon, Sparkles, Terminal } from 'lucide-react';
import { useUIStore } from '../../stores/uiStore';

export const Header: React.FC = () => {
  const { toggleSidebar } = useUIStore();
  const [isDark, setIsDark] = React.useState(true);

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <header className="h-14 border-b border-border bg-card px-4 flex items-center justify-between shrink-0">
      <div className="flex items-center gap-3">
        <button onClick={toggleSidebar} className="p-1.5 rounded-lg hover:bg-secondary text-muted hover:text-foreground">
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-blue-600/10 text-blue-500">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-semibold text-sm leading-tight">AI SysAdmin & DevSecOps Agent</h1>
            <span className="text-[10px] text-emerald-500 font-mono font-medium">31 Araç Aktif (Local-First)</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button 
          onClick={toggleTheme}
          className="p-2 rounded-lg hover:bg-secondary text-muted hover:text-foreground transition-colors"
        >
          {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
};
