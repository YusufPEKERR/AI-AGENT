import os
import re
import subprocess
from pathlib import Path
from typing import Optional
from ai_agent.config import settings
from ai_agent.exceptions import SecurityError


def resolve_safe_path(user_path: Optional[str]) -> Path:
    """Path traversal guard preventing unauthorized directory traversal."""
    if not user_path:
        return Path.cwd()

    expanded = os.path.expanduser(user_path)
    path_obj = Path(expanded).resolve()

    desktop_path = Path.home() / "Desktop"
    if "masaüstü" in user_path.lower() or "masaustu" in user_path.lower() or "desktop" in user_path.lower():
        filename = path_obj.name if path_obj.name not in ["masaüstü", "masaustu", "desktop"] else "yeni_dosya.txt"
        return desktop_path / filename

    # Verify against allowed base paths
    is_allowed = any(
        path_obj == allowed or allowed in path_obj.parents
        for allowed in settings.allowed_paths
    )

    if not is_allowed:
        # Fallback check for workspace / home directory access
        if Path.cwd() in path_obj.parents or path_obj == Path.cwd():
            return path_obj
        raise SecurityError(f"Erişim Engellendi: '{path_obj}' izin verilen dizinler dışında.")

    return path_obj


def make_ps_cred_prefix(username: Optional[str], password: Optional[str]) -> str:
    """Escapes credentials safely for PowerShell PSCredential objects."""
    if username and password:
        clean_user = username.replace("'", "''")
        clean_pass = password.replace("'", "''")
        return (
            f"$secstr = ConvertTo-SecureString '{clean_pass}' -AsPlainText -Force; "
            f"$cred = New-Object System.Management.Automation.PSCredential('{clean_user}', $secstr); "
        )
    return ""


def run_powershell_safe(ps_code: str, timeout: int = 60) -> str:
    """Runs a PowerShell command with UTF-8 encoding and timeout protection."""
    try:
        full_cmd = f"[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; {ps_code}"
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", full_cmd],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )
        output = result.stdout.strip() if result.stdout else ""
        error = result.stderr.strip() if result.stderr else ""
        if error and not output:
            return f"Hata: {error}"
        elif error:
            return f"Çıktı:\n{output}\n\nUyarı/Hata:\n{error}"
        return output if output else "İşlem başarıyla tamamlandı (Çıktı yok)."
    except subprocess.TimeoutExpired:
        return f"Hata: Komut zaman aşımına uğradı ({timeout} saniye)."
    except Exception as e:
        return f"Sistem hatası: {str(e)}"


def scrub_secrets(text: str) -> str:
    """Scrubs sensitive API keys or passwords from log strings."""
    pattern = r"(nvapi-[A-Za-z0-9_\-]+|password=['\"]?[^'\"]+['\"]?)"
    return re.sub(pattern, "***REDACTED***", text)
