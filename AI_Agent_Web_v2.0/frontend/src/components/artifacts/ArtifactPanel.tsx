import React from 'react';
import { X, Code, FileText } from 'lucide-react';
import { useUIStore } from '../../stores/uiStore';

export const ArtifactPanel: React.FC = () => {
  const { isArtifactPanelOpen, activeArtifact, toggleArtifactPanel } = useUIStore();

  if (!isArtifactPanelOpen || !activeArtifact) return null;

  return (
    <div className="w-96 border-l border-border bg-card flex flex-col shrink-0">
      <div className="h-12 border-b border-border px-4 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-medium">
          <Code className="w-4 h-4 text-blue-500" />
          <span>{activeArtifact.title}</span>
        </div>
        <button onClick={toggleArtifactPanel} className="p-1 rounded hover:bg-secondary text-muted">
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="flex-1 p-4 overflow-y-auto font-mono text-xs bg-slate-950 text-slate-100">
        <pre>{activeArtifact.content}</pre>
      </div>
    </div>
  );
};
