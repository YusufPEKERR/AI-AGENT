import subprocess
from typing import Optional
from ai_agent.models.messages import ToolResult
from ai_agent.core.security import run_powershell_safe


def docker_manage(
    action: str,
    container_name: Optional[str] = None,
    image_name: Optional[str] = None,
    command: Optional[str] = None
) -> ToolResult:
    try:
        cmd_parts = ["docker"]
        if action == "ps":
            cmd_parts.extend(["ps", "-a"])
        elif action == "images":
            cmd_parts.extend(["images"])
        elif action == "run":
            if not image_name:
                return ToolResult(success=False, output="", error="run işlemi için image_name gereklidir.")
            cmd_parts.extend(["run", "-d"])
            if container_name:
                cmd_parts.extend(["--name", container_name])
            cmd_parts.append(image_name)
        elif action == "stop":
            if not container_name:
                return ToolResult(success=False, output="", error="stop işlemi için container_name gereklidir.")
            cmd_parts.extend(["stop", container_name])
        elif action == "logs":
            if not container_name:
                return ToolResult(success=False, output="", error="logs işlemi için container_name gereklidir.")
            cmd_parts.extend(["logs", "--tail", "50", container_name])
        elif action == "exec":
            if not container_name or not command:
                return ToolResult(success=False, output="", error="exec işlemi için container_name ve command gereklidir.")
            cmd_parts.extend(["exec", container_name] + command.split())
        elif action == "compose_up":
            cmd_parts = ["docker-compose", "up", "-d"]
        elif action == "compose_down":
            cmd_parts = ["docker-compose", "down"]
        else:
            cmd_parts.extend(["ps"])

        res = subprocess.run(cmd_parts, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        out = res.stdout.strip() if res.stdout else ""
        err = res.stderr.strip() if res.stderr else ""
        return ToolResult(success=True, output=out if out else (err if err else "Docker komutu başarıyla çalıştırıldı."))
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))


def k8s_manage(
    action: str = "get",
    resource: str = "pods",
    name: Optional[str] = None,
    namespace: str = "default"
) -> ToolResult:
    try:
        if action == "get":
            cmd = f"kubectl get {resource} -n {namespace} -o wide" if not name else f"kubectl get {resource} {name} -n {namespace} -o yaml"
        elif action == "logs":
            cmd = f"kubectl logs {name} -n {namespace} --tail=100"
        elif action == "describe":
            cmd = f"kubectl describe {resource} {name} -n {namespace}"
        elif action == "delete":
            cmd = f"kubectl delete {resource} {name} -n {namespace}"
        else:
            cmd = f"kubectl get {resource} -n {namespace}"

        res = run_powershell_safe(cmd)
        return ToolResult(success=True, output=res)
    except Exception as e:
        return ToolResult(success=False, output="", error=str(e))
