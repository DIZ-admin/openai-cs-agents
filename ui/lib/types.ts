// Tool-related types (defined first for use in Message interface)
export interface ToolCall {
  id: string
  type: string
  function: {
    name: string
    arguments: string
  }
}

export interface ToolResult {
  tool_call_id: string
  output: string
}

export interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  agent?: string
  timestamp: Date
  tool_calls?: ToolCall[]
  tool_results?: ToolResult[]
}

export interface Agent {
  name: string
  description: string
  handoffs: string[]
  tools: string[]
  /** List of input guardrail identifiers for this agent */
  input_guardrails: string[]
  /** List of output guardrail identifiers for this agent */
  output_guardrails: string[]
}

export type EventType = "message" | "handoff" | "tool_call" | "tool_output" | "context_update"

// Event metadata types
export interface HandoffMetadata {
  source_agent: string
  target_agent: string
}

export interface ToolCallMetadata {
  tool_name: string
  tool_args: Record<string, unknown>
}

export interface ToolResultMetadata {
  tool_name: string
  tool_result: string | Record<string, unknown>
}

export interface ContextUpdateMetadata {
  context_key: string
  context_value: string | number | boolean | null
  changes?: Record<string, unknown>
}

export type EventMetadata =
  | HandoffMetadata
  | ToolCallMetadata
  | ToolResultMetadata
  | ContextUpdateMetadata
  | Record<string, unknown>

export interface AgentEvent {
  id: string
  type: EventType
  agent: string
  content: string
  timestamp: Date
  metadata?: EventMetadata
}

export interface GuardrailCheck {
  id: string
  name: string
  input: string
  reasoning: string
  passed: boolean | null
  timestamp: Date
}
