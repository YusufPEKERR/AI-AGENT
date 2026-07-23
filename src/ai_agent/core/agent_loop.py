import json
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ai_agent.config import settings
from ai_agent.core.llm_client import LLMClient
from ai_agent.core.system_prompt import get_system_prompt
from ai_agent.tools import tool_registry

console = Console()


class AgentLoop:
    def __init__(self) -> None:
        self.llm_client = LLMClient()
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": get_system_prompt()}
        ]

    def process_user_request(self, user_input: str) -> None:
        self.messages.append({"role": "user", "content": user_input})

        for iteration in range(settings.max_tool_iterations):
            tool_calls_accumulator: dict[int, dict[str, Any]] = {}
            assistant_response = ""
            has_reasoning = False
            has_started_content = False

            try:
                chunks = self.llm_client.stream_chat_completion(
                    messages=self.messages,
                    tools=tool_registry.schemas
                )

                for chunk in chunks:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta

                    reasoning = getattr(delta, "reasoning_content", None)
                    if reasoning:
                        if not has_reasoning:
                            console.print("\n[bold cyan][Düşünce Süreci]:[/bold cyan]")
                            has_reasoning = True
                        console.print(reasoning, end="", style="dim cyan")

                    if delta.tool_calls:
                        for tc in delta.tool_calls:
                            idx = tc.index
                            if idx not in tool_calls_accumulator:
                                tool_calls_accumulator[idx] = {
                                    "id": tc.id or "",
                                    "name": tc.function.name if tc.function and tc.function.name else "",
                                    "arguments": tc.function.arguments if tc.function and tc.function.arguments else ""
                                }
                            else:
                                if tc.id:
                                    tool_calls_accumulator[idx]["id"] += tc.id
                                if tc.function:
                                    if tc.function.name:
                                        tool_calls_accumulator[idx]["name"] += tc.function.name
                                    if tc.function.arguments:
                                        tool_calls_accumulator[idx]["arguments"] += tc.function.arguments

                    if delta.content is not None:
                        if not has_started_content:
                            if has_reasoning:
                                console.print("\n\n[bold green][Cevap]:[/bold green]")
                            else:
                                console.print("\n[bold green][Cevap]:[/bold green]")
                            has_started_content = True
                        console.print(delta.content, end="")
                        assistant_response += delta.content

                console.print()

            except Exception as e:
                console.print(f"\n[bold red]Hata:[bold red] {e}")
                if self.messages and self.messages[-1]["role"] == "user":
                    self.messages.pop()
                break

            if tool_calls_accumulator:
                tool_calls_list = []
                for idx in sorted(tool_calls_accumulator.keys()):
                    tc_info = tool_calls_accumulator[idx]
                    tool_calls_list.append({
                        "id": tc_info["id"],
                        "type": "function",
                        "function": {
                            "name": tc_info["name"],
                            "arguments": tc_info["arguments"]
                        }
                    })

                self.messages.append({
                    "role": "assistant",
                    "content": assistant_response if assistant_response else None,
                    "tool_calls": tool_calls_list
                })

                for tc_info in tool_calls_list:
                    func_name = tc_info["function"]["name"]
                    try:
                        func_args = json.loads(tc_info["function"]["arguments"])
                    except Exception:
                        func_args = {}

                    console.print(f"\n[bold yellow]🛠 Araç Çalıştırılıyor:[/bold yellow] [bold white]{func_name}[/bold white] (Args: {func_args})")
                    result_obj = tool_registry.execute(func_name, func_args)
                    result_text = result_obj.to_output_str()

                    status_style = "bold green" if result_obj.success else "bold red"
                    console.print(f"[{status_style}]📥 Araç Sonucu:[/{status_style}] {result_text[:500]}")

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tc_info["id"],
                        "content": result_text
                    })

                continue
            else:
                if assistant_response:
                    self.messages.append({"role": "assistant", "content": assistant_response})
                break
