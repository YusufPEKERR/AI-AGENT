import typer
from rich.console import Console
from ai_agent import __version__
from ai_agent.cli.repl import start_repl
from ai_agent.tools import tool_registry

app = typer.Typer(
    name="ai-agent",
    help="AI SysAdmin & DevSecOps Agent CLI",
    add_completion=False
)
console = Console()


@app.command(name="chat")
def chat_cmd() -> None:
    """Interaktif REPL sohbet modunu başlatır."""
    start_repl()


@app.command(name="run")
def run_cmd(prompt: str = typer.Argument(..., help="Çalıştırılacak komut veya istek")) -> None:
    """Tek bir komut veya isteği çalıştırıp sonlandırır."""
    from ai_agent.core.agent_loop import AgentLoop
    from ai_agent.logging_conf import setup_logging
    setup_logging()
    agent = AgentLoop()
    agent.process_user_request(prompt)


@app.command(name="doctor")
def doctor_cmd() -> None:
    """Sistem ve araç sağlık durumunu kontrol eder."""
    console.print("[bold green]🏥 AI Agent Sağlık Kontrolü[/bold green]\n")
    console.print(f"Versiyon: [cyan]{__version__}[/cyan]")
    console.print(f"Kayıtlı Araç Sayısı: [bold yellow]{len(tool_registry.schemas)}[/bold yellow] adet araç aktif.")
    for tool_name in tool_registry._tools.keys():
        console.print(f"  ✓ {tool_name}")
    console.print("\n[bold green]✅ Tüm sistemler çalışır durumda![/bold green]")


@app.command(name="version")
def version_cmd() -> None:
    """Versiyon bilgisini gösterir."""
    console.print(f"AI Agent Version: [bold green]{__version__}[/bold green]")


def main() -> None:
    app()


if __name__ == "__main__":
    start_repl()
