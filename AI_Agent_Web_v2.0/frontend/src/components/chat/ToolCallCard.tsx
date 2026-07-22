import React, { useState } from 'react';
import { ChevronDown, Code, Terminal, CheckCircle, Clock } from 'lucide-react';
import { cn } from '../../utils/cn';

interface ToolCallCardProps {
  name: string;
  args: Record<string, any>;
  result?: any;
  isExecuting?: boolean;
}

export const ToolCallCard: React.FC<ToolCallCardProps> = ({ name, args, result, isExecuting }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="my-2 rounded-lg border border-blue-200 bg-blue-50/50 dark:border-blue-900/40 dark:bg-blue-950/20 text-xs overflow-hidden transition-all shadow-sm">
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 px-3 py-2 cursor-pointer hover:bg-blue-100/50 dark:hover:bg-blue-900/30 transition-colors"
      >
        <Terminal className="w-4 h-4 text-blue-600 dark:text-blue-400" />
        <span className="font-mono font-semibold text-blue-900 dark:text-blue-300">{name}</span>
        
        {isExecuting ? (
          <span className="flex items-center gap-1 ml-auto text-amber-600 dark:text-amber-400 font-medium">
            <Clock className="w-3.5 h-3.5 animate-spin" /> Çalıştırılıyor...
          </span>
        ) : (
          <span className="flex items-center gap-1 ml-auto text-emerald-600 dark:text-emerald-400 font-medium">
            <CheckCircle className="w-3.5 h-3.5" /> Tamamlandı
          </span>
        )}

        <ChevronDown className={cn("w-4 h-4 text-blue-600 transition-transform duration-200", isExpanded && "rotate-180")} />
      </div>

      {isExpanded && (
        <div className="p-3 border-t border-blue-200 dark:border-blue-900/40 space-y-2 bg-white/50 dark:bg-black/20">
          <div>
            <div className="font-semibold text-slate-500 dark:text-slate-400 mb-1">Parametreler:</div>
            <pre className="p-2 rounded bg-slate-900 text-slate-100 font-mono overflow-x-auto text-[11px]">
              {JSON.stringify(args, null, 2)}
            </pre>
          </div>

          {result && (
            <div>
              <div className="font-semibold text-slate-500 dark:text-slate-400 mb-1">Çıktı:</div>
              <pre className="p-2 rounded bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 font-mono overflow-x-auto text-[11px] whitespace-pre-wrap max-h-60 overflow-y-auto">
                {typeof result === 'string' ? result : JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
