from typing import Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import run_powershell_safe, make_ps_cred_prefix


def registry_read_write(
    path: str,
    operation: str,
    value_name: Optional[str] = None,
    value: Optional[str] = None,
    hive: str = "HKLM"
) -> ToolResult:
    try:
        if operation == "read":
            ps = f"(Get-ItemProperty -Path '{hive}:\\{path}').'{value_name}'" if value_name else f"Get-ItemProperty -Path '{hive}:\\{path}'"
        elif operation == "write":
            ps = f"Set-ItemProperty -Path '{hive}:\\{path}' -Name '{value_name}' -Value '{value}' -Force"
        elif operation == "delete":
            ps = f"Remove-ItemProperty -Path '{hive}:\\{path}' -Name '{value_name}' -Force" if value_name else f"Remove-Item -Path '{hive}:\\{path}' -Recurse -Force"
        else:
            ps = f"Get-ChildItem -Path '{hive}:\\{path}'"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def wmi_query(
    query: str,
    namespace: str = "root/cimv2",
    computer_name: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> ToolResult:
    try:
        if computer_name and computer_name.lower() not in ["localhost", "127.0.0.1", "."]:
            cred_prefix = make_ps_cred_prefix(username, password)
            cred_arg = " -Credential $cred" if (username and password) else ""
            ps = f"{cred_prefix}Get-CimInstance -Query \"{query}\" -Namespace '{namespace}' -ComputerName '{computer_name}'{cred_arg} | Format-List"
        else:
            ps = f"Get-CimInstance -Query \"{query}\" -Namespace '{namespace}' | Format-List"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def event_log_query(
    log_name: str = "System",
    max_events: int = 50,
    computer_name: Optional[str] = None
) -> ToolResult:
    try:
        comp_arg = f" -ComputerName '{computer_name}'" if (computer_name and computer_name.lower() not in ["localhost", "127.0.0.1", "."]) else ""
        ps = f"Get-EventLog -LogName '{log_name}' -Newest {max_events}{comp_arg} | Select-Object TimeGenerated, EntryType, Source, EventID, Message | Format-Table -AutoSize"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def scheduled_task_manage(
    task_name: str,
    action: str,
    action_exec: Optional[str] = None,
    action_args: Optional[str] = None
) -> ToolResult:
    try:
        aargs = action_args or ""
        if action == "run":
            ps = f"Start-ScheduledTask -TaskName '{task_name}'"
        elif action == "stop":
            ps = f"Stop-ScheduledTask -TaskName '{task_name}'"
        elif action == "enable":
            ps = f"Enable-ScheduledTask -TaskName '{task_name}'"
        elif action == "disable":
            ps = f"Disable-ScheduledTask -TaskName '{task_name}'"
        elif action == "delete":
            ps = f"Unregister-ScheduledTask -TaskName '{task_name}' -Confirm:$false"
        elif action == "create":
            ps = f"$action = New-ScheduledTaskAction -Execute '{action_exec}' -Argument '{aargs}'; Register-ScheduledTask -TaskName '{task_name}' -Action $action -Force"
        else:
            ps = f"Get-ScheduledTask -TaskName '{task_name}'"
        res = run_powershell_safe(ps)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
