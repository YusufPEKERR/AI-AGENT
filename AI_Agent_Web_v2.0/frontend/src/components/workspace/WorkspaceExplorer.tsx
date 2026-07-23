import React, { useState, useEffect } from 'react';
import { FolderTree, FileText, Folder, Terminal, Code2, RefreshCw, FolderOpen } from 'lucide-react';
import { FileNode } from '../../types';

export const WorkspaceExplorer: React.FC = () => {
  const [currentPath, setCurrentPath] = useState<string>(() => {
    return localStorage.getItem('workspacePath') || '.';
  });
  const [files, setFiles] = useState<FileNode[]>([]);
  const [selectedFile, setSelectedFile] = useState<FileNode | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    localStorage.setItem('workspacePath', currentPath);
  }, [currentPath]);

  const fetchWorkspace = () => {
    fetch('http://localhost:8000/api/tools/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tool_id: 'list_dir', arguments: { DirectoryPath: currentPath } })
    })
      .then(res => res.json())
      .then(data => {
        if (data.result) {
          const nodes: FileNode[] = data.result.map((item: any) => ({
            name: item.name,
            path: item.name,
            isDir: item.isDir
          }));
          setFiles(nodes);
        }
      })
      .catch(err => console.error('Failed to list workspace:', err));
  };

  useEffect(() => {
    fetchWorkspace();
  }, [currentPath]);

  const handleSelectFolder = () => {
    const defaultPath = currentPath === '.' ? 'C:\\' : currentPath;
    const path = window.prompt('Lütfen proje klasörünün tam yolunu (Örn: C:\\Projeler\\Uygulama) girin:', defaultPath);
    
    if (path && path.trim() !== '') {
      setCurrentPath(path.trim());
      setSelectedFile(null);
      setFileContent('');
    }
  };

  const handleSelectFile = (file: FileNode) => {
    setSelectedFile(file);
    if (file.isDir) {
      setFileContent(`[Klasör] ${file.name} dizini seçildi.`);
      return;
    }

    setLoading(true);
    setFileContent('Dosya içeriği yükleniyor...');
    
    const absolutePath = currentPath === '.' ? file.name : `${currentPath}/${file.name}`;

    fetch('http://localhost:8000/api/tools/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tool_id: 'view_file', arguments: { AbsolutePath: absolutePath } })
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setFileContent(data.result);
        } else {
          setFileContent(`Hata: ${data.error}`);
        }
      })
      .catch(err => {
        setFileContent(`Dosya yüklenirken hata oluştu: ${err}`);
      })
      .finally(() => setLoading(false));
  };

  return (
    <div className="flex-1 flex h-[calc(100vh-4rem)] p-6 gap-6 overflow-hidden">
      {/* File Tree Left Sidebar */}
      <div className="w-80 glass-panel p-5 rounded-2xl border-slate-800 flex flex-col space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <h3 className="font-bold text-slate-100 text-sm flex items-center gap-2">
            <FolderTree className="w-4 h-4 text-cyan-400" />
            Project Files
          </h3>
          <div className="flex gap-1.5">
            <button
              onClick={handleSelectFolder}
              className="p-1 rounded bg-slate-900 text-slate-400 hover:text-cyan-400 transition-all"
              title="Klasör Seç"
            >
              <FolderOpen className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={fetchWorkspace}
              className="p-1 rounded bg-slate-900 text-slate-400 hover:text-cyan-400 transition-all"
              title="Yenile"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {currentPath !== '.' && (
          <div className="text-[10px] text-slate-500 truncate" title={currentPath}>
            {currentPath}
          </div>
        )}

        <div className="flex-1 overflow-y-auto space-y-1">
          {files.map((file) => (
            <button
              key={file.path}
              onClick={() => handleSelectFile(file)}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-mono transition-all ${
                selectedFile?.path === file.path
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30'
                  : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200 border border-transparent'
              }`}
            >
              {file.isDir ? (
                <Folder className="w-4 h-4 text-amber-400 shrink-0" />
              ) : (
                <FileText className="w-4 h-4 text-purple-400 shrink-0" />
              )}
              <span className="truncate">{file.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Code Editor / Diff Viewer Main View */}
      <div className="flex-1 glass-panel rounded-2xl border-slate-800 flex flex-col overflow-hidden">
        {/* Editor Tab Header */}
        <div className="h-12 bg-slate-950/80 border-b border-slate-800/80 px-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 font-semibold">
            <Code2 className="w-4 h-4" />
            <span>{selectedFile ? selectedFile.name : 'Dosya seçilmedi'}</span>
          </div>

          <div className="flex items-center gap-2 text-[11px] text-slate-500 font-mono">
            <span>UTF-8</span>
            <span>•</span>
            <span>TypeScript / Python</span>
          </div>
        </div>

        {/* Code Content Area */}
        <div className="flex-1 overflow-auto p-6 font-mono text-xs text-slate-300 bg-slate-950/60 leading-relaxed">
          {selectedFile ? (
            <pre className="whitespace-pre-wrap">{fileContent}</pre>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-2">
              <Terminal className="w-10 h-10 text-slate-600" />
              <p className="text-xs">İçeriğini görüntülemek için sol menüden bir dosya seçin.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
