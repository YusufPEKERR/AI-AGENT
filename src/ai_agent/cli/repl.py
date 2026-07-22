import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from ai_agent.core.agent_loop import AgentLoop
from ai_agent.logging_conf import setup_logging

console = Console()


def start_repl() -> None:
    setup_logging()
    desktop_folder = Path.home() / "Desktop"

    banner = (
        "[bold cyan]==========================================================[/bold cyan]\n"
        "[bold green]🚀 AI SysAdmin & DevSecOps Agent (31-Tool Architecture)[/bold green]\n"
        "✅ [white]Git, LSP, Test, Docker, K8s, DB, Patch, Format & WinRM Aktif![/white]\n"
        f"📁 [yellow]Masaüstü Yolu:[yellow] [white]{desktop_folder}[/white]\n"
        "🚪 [dim]Çıkmak için 'exit' veya 'quit' yazabilirsiniz.[/dim]\n"
        "[bold cyan]==========================================================[/bold cyan]\n"
    )
    console.print(banner)

    history_file = Path.home() / ".ai_agent_history"
    session = PromptSession(history=FileHistory(str(history_file)))
    agent = AgentLoop()

    while True:
        try:
            user_input = session.prompt("\nSiz > ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow]Sohbet sonlandırıldı.[/bold yellow]")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold yellow]Sohbet sonlandırıldı.[/bold yellow]")
            break

        agent.process_user_request(user_input)
