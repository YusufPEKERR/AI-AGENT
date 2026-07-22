import subprocess
from typing import Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import resolve_safe_path, run_powershell_safe, make_ps_cred_prefix


def execute_command(command: str, cwd: Optional[str] = None, shell: str = "powershell") -> ToolResult:
    try:
        safe_cwd = resolve_safe_path(cwd) if cwd else None
        if shell == "cmd":
            cmd_args = ["cmd.exe", "/c", command]
        elif shell == "bash":
            cmd_args = ["bash", "-c", command]
        else:
            cmd_args = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {command}"]

        res = subprocess.run(
            cmd_args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=safe_cwd, timeout=120
        )
        out = res.stdout.strip() if res.stdout else ""
        err = res.stderr.strip() if res.stderr else ""
        return ToolResult(success=True, output=out if out else (err if err else "Komut tamamlandı."))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def get_process_list(filter: Optional[str] = None) -> ToolResult:
    try:
        if filter:
            ps = f"Get-Process -Name '{filter}' -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU, WorkingSet64 | Format-Table -AutoSize"
        else:
            ps = "Get-Process | Select-Object Id, ProcessName, CPU, WorkingSet64 -First 40 | Format-Table -AutoSize"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def kill_process(pid: Optional[int] = None, name: Optional[str] = None, force: bool = True) -> ToolResult:
    try:
        f_flag = "-Force" if force else ""
        if pid:
            ps = f"Stop-Process -Id {pid} {f_flag}"
        elif name:
            ps = f"Stop-Process -Name '{name}' {f_flag}"
        else:
            return ToolResult(success=False, output="", error="PID veya süreç adı (name) belirtilmelidir.")
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def manage_service(
    name: str,
    action: str,
    computer_name: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> ToolResult:
    try:
        if action == "start":
            cmd = f"Start-Service -Name '{name}'"
        elif action == "stop":
            cmd = f"Stop-Service -Name '{name}'"
        elif action == "restart":
            cmd = f"Restart-Service -Name '{name}'"
        elif action == "enable":
            cmd = f"Set-Service -Name '{name}' -StartupType Automatic"
        elif action == "disable":
            cmd = f"Set-Service -Name '{name}' -StartupType Disabled"
        else:
            cmd = f"Get-Service -Name '{name}'"

        if computer_name and computer_name.lower() not in ["localhost", "127.0.0.1", "."]:
            cred_prefix = make_ps_cred_prefix(username, password)
            cred_arg = " -Credential $cred" if (username and password) else ""
            ps = f"{cred_prefix}Invoke-Command -ComputerName '{computer_name}'{cred_arg} -ScriptBlock {{ {cmd} }}"
        else:
            ps = cmd

        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
