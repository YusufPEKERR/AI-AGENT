export type TabType = 'chat' | 'tools' | 'monitor' | 'workspace' | 'widgets';

export type SocketStatus = 'connected' | 'connecting' | 'disconnected';

export interface ToolCall {
  id: string;
  name: string;
  arguments: Record<string, any>;
  result?: string;
  status?: 'pending' | 'running' | 'completed' | 'error';
}

export interface Message {
  id: string;
  sender: 'user' | 'agent' | 'system';
  content: string;
  timestamp: string;
  toolCalls?: ToolCall[];
  isStreaming?: boolean;
}

export interface Tool {
  id: string;
  name: string;
  category: string;
  description: string;
  params: string[];
}

export interface ProcessInfo {
  pid: number;
  name: string;
  cpu_percent: number;
  memory_percent: number;
}

export interface SystemMetrics {
  cpu_percent: number;
  memory_percent: number;
  memory_used_mb: number;
  memory_total_mb: number;
  disk_percent: number;
  disk_used_gb: number;
  disk_total_gb: number;
  uptime_seconds: number;
  top_processes: ProcessInfo[];
  python_version: string;
  os_platform: string;
}

export interface FileNode {
  name: string;
  path: string;
  isDir: boolean;
  sizeBytes?: number;
  content?: string;
  children?: FileNode[];
}
