import React, { useState, useEffect } from 'react';
import { Search, Wrench, Play, CheckCircle, AlertCircle, Cpu, Shield, Folder, Globe, Bot } from 'lucide-react';
import { useAppStore } from '../../store/useAppStore';
import { Tool } from '../../types';
import { API_BASE_URL } from '../../services/api';

export const ToolCatalog: React.FC = () => {
  const { tools, setTools } = useAppStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [activeTool, setActiveTool] = useState<Tool | null>(null);
  const [paramInputs, setParamInputs] = useState<Record<string, string>>({});
  const [executionResult, setExecutionResult] = useState<any>(null);
  const [isExecuting, setIsExecuting] = useState(false);

  useEffect(() => {
    // Fetch tool catalog from REST endpoint
    fetch(`${API_BASE_URL}/tools/`)
      .then(res => res.json())
      .then(data => {
        if (data.tools) setTools(data.tools);
      })
      .catch(err => console.error('Failed to fetch tools:', err));
  }, [setTools]);

  const categories = [
    'All',
    'Ağ Keşif & Tarama',
    'Zafiyet Tarama & Analiz',
    'Exploitation Frameworks',
    'Kimlik Bilgisi & Exploitation',
    'Kablosuz Ağ Saldırıları',
    'Web Uygulama Saldırıları',
    'Sosyal Mühendislik',
    'Parola Kırma',
    'Privilege Escalation',
    'Tersine Mühendislik',
    'Container & Cloud Security',
    'Adli Bilişim & Anti-Forensics',
    'System Admin',
    'File Ops'
  ];

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'Ağ Keşif & Tarama': return <Globe className="w-4 h-4 text-cyan-400" />;
      case 'Zafiyet Tarama & Analiz': return <Shield className="w-4 h-4 text-amber-400" />;
      case 'Exploitation Frameworks': return <Cpu className="w-4 h-4 text-red-400" />;
      case 'Kimlik Bilgisi & Exploitation': return <Shield className="w-4 h-4 text-purple-400" />;
      case 'Web Uygulama Saldırıları': return <Globe className="w-4 h-4 text-rose-400" />;
      case 'Container & Cloud Security': return <Cpu className="w-4 h-4 text-blue-400" />;
      case 'Adli Bilişim & Anti-Forensics': return <Folder className="w-4 h-4 text-emerald-400" />;
      default: return <Wrench className="w-4 h-4 text-slate-400" />;
    }
  };

  const filteredTools = tools.filter(tool => {
    const matchesSearch = tool.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          tool.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || tool.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleSelectTool = (tool: Tool) => {
    setActiveTool(tool);
    setExecutionResult(null);
    const initialInputs: Record<string, string> = {};
    tool.params.forEach(p => initialInputs[p] = '');
    setParamInputs(initialInputs);
  };

  const handleExecuteTool = async () => {
    if (!activeTool) return;
    setIsExecuting(true);
    setExecutionResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/tools/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tool_id: activeTool.id,
          arguments: paramInputs
        })
      });
      const data = await response.json();
      setExecutionResult(data);
    } catch (err) {
      setExecutionResult({ status: 'error', error: 'Sunucu ile iletişim kurulamadı.' });
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] p-6 space-y-6 overflow-y-auto">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border-cyan-500/20">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Wrench className="w-6 h-6 text-cyan-400" />
            System & Agent Tool Catalog (31 Tools)
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Yapay zeka ajanı tarafından erişilebilen ve anlık çalıştırılabilen tüm sistem araçları.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
          <input
            type="text"
            placeholder="Araç adı veya açıklama ara..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50"
          />
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-2">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              selectedCategory === cat
                ? 'bg-gradient-to-r from-cyan-500 to-purple-600 text-white shadow-md shadow-cyan-500/20'
                : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Tools Grid & Runner Split Container */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Tool Cards Catalog */}
        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredTools.map((tool) => (
            <div
              key={tool.id}
              onClick={() => handleSelectTool(tool)}
              className={`p-4 rounded-xl glass-panel cursor-pointer transition-all duration-200 hover:scale-[1.02] border ${
                activeTool?.id === tool.id
                  ? 'border-cyan-500/60 bg-cyan-950/20 shadow-lg shadow-cyan-500/10'
                  : 'border-slate-800/80 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-cyan-400 font-semibold">{tool.id}</span>
                <div className="flex items-center gap-1 text-[10px] px-2 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-800">
                  {getCategoryIcon(tool.category)}
                  <span>{tool.category}</span>
                </div>
              </div>

              <h3 className="font-semibold text-slate-200 text-sm">{tool.name}</h3>
              <p className="text-xs text-slate-400 mt-1 line-clamp-2">{tool.description}</p>

              <div className="mt-3 pt-2 border-t border-slate-800/60 flex flex-wrap gap-1">
                {tool.params.map(p => (
                  <span key={p} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-950 text-slate-400 border border-slate-800">
                    {p}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Right: Interactive Tool Execution Panel */}
        <div className="glass-panel p-5 rounded-2xl border-slate-800 space-y-4 h-fit sticky top-20">
          {activeTool ? (
            <>
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div>
                  <h3 className="font-bold text-slate-100 text-sm">{activeTool.name} Test Runner</h3>
                  <span className="text-xs font-mono text-cyan-400">{activeTool.id}</span>
                </div>
                <button
                  onClick={handleExecuteTool}
                  disabled={isExecuting}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-semibold text-xs shadow-md shadow-cyan-500/20 hover:opacity-90 active:scale-95 disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5" />
                  <span>{isExecuting ? 'Calışıyor...' : 'Çalıştır'}</span>
                </button>
              </div>

              <p className="text-xs text-slate-400">{activeTool.description}</p>

              {/* Parameter Input Form */}
              <div className="space-y-3">
                <h4 className="text-xs font-semibold text-slate-300">Parametreler:</h4>
                {activeTool.params.length === 0 ? (
                  <p className="text-xs text-slate-500 italic">Bu araç parametre gerektirmez.</p>
                ) : (
                  activeTool.params.map((param) => (
                    <div key={param} className="space-y-1">
                      <label className="text-[11px] font-mono text-slate-400">{param}</label>
                      <input
                        type="text"
                        placeholder={`Değer girin (${param})`}
                        value={paramInputs[param] || ''}
                        onChange={(e) => setParamInputs({ ...paramInputs, [param]: e.target.value })}
                        className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500/50"
                      />
                    </div>
                  ))
                )}
              </div>

              {/* Execution Result Box */}
              {executionResult && (
                <div className="mt-4 pt-3 border-t border-slate-800 space-y-2">
                  <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                    {executionResult.status === 'success' ? (
                      <CheckCircle className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-rose-400" />
                    )}
                    Çıktı Sonucu:
                  </span>
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-cyan-300 overflow-x-auto max-h-48">
                    <pre>{JSON.stringify(executionResult.result || executionResult.error, null, 2)}</pre>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="py-12 text-center text-slate-500 space-y-2">
              <Wrench className="w-8 h-8 mx-auto text-slate-600" />
              <p className="text-xs">Test etmek ve parametrelerini incelemek için sol listeden bir araç seçin.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
