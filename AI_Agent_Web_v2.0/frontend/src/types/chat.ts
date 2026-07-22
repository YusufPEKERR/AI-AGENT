export type MessageRole = 'user' | 'assistant' | 'tool_call' | 'tool_result' | 'system';

export interface ToolCallData {
  id: string;
  name: string;
  arguments: Record<string, any>;
}

export interface Message {
  id: string;
  role: MessageRole;
  content?: string;
  toolCall?: ToolCallData;
  toolResult?: any;
  timestamp?: string;
}
