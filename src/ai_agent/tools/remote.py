from typing import Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import resolve_safe_path, run_powershell_safe, make_ps_cred_prefix


def invoke_remote_command(computer_name: str, command: str, username: str, password: str) -> ToolResult:
    try:
        cred_prefix = make_ps_cred_prefix(username, password)
        cred_arg = " -Credential $cred" if (username and password) else ""
        ps = f"{cred_prefix}Invoke-Command -ComputerName '{computer_name}'{cred_arg} -ScriptBlock {{ {command} }}"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def create_pssession(computer_name: str, username: Optional[str] = None, password: Optional[str] = None) -> ToolResult:
    try:
        cred_prefix = make_ps_cred_prefix(username, password)
        cred_arg = " -Credential $cred" if (username and password) else ""
        ps = f"{cred_prefix}$s = New-PSSession -ComputerName '{computer_name}'{cred_arg}; Get-PSSession; Remove-PSSession $s"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def copy_to_remote(computer_name: str, source: str, destination: str, username: str, password: str) -> ToolResult:
    try:
        safe_src = resolve_safe_path(source)
        cred_prefix = make_ps_cred_prefix(username, password)
        cred_arg = " -Credential $cred" if (username and password) else ""
        ps = f"{cred_prefix}$s = New-PSSession -ComputerName '{computer_name}'{cred_arg}; Copy-Item -Path '{safe_src}' -Destination '{destination}' -ToSession $s -Recurse -Force; Remove-PSSession $s"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def copy_from_remote(computer_name: str, source: str, destination: str, username: str, password: str) -> ToolResult:
    try:
        safe_dest = resolve_safe_path(destination)
        cred_prefix = make_ps_cred_prefix(username, password)
        cred_arg = " -Credential $cred" if (username and password) else ""
        ps = f"{cred_prefix}$s = New-PSSession -ComputerName '{computer_name}'{cred_arg}; Copy-Item -Path '{source}' -Destination '{safe_dest}' -FromSession $s -Recurse -Force; Remove-PSSession $s"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def test_connection(computer_name: str, username: Optional[str] = None, password: Optional[str] = None) -> ToolResult:
    try:
        if username and password:
            cred_prefix = make_ps_cred_prefix(username, password)
            ps = f"{cred_prefix}Test-WSMan -ComputerName '{computer_name}' -Credential $cred"
        else:
            ps = f"Test-NetConnection -ComputerName '{computer_name}' | Select-Object ComputerName, RemoteAddress, PingSucceeded, TcpTestSucceeded | Format-List"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
